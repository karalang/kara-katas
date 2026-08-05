#!/usr/bin/env bash
# verify.sh — Cumulus step-1 differential harness.
#
# Generates a synthetic stack, integrates it four ways (two modes x two
# backends), and checks every result against the numpy reference. Fails on the
# first divergence.
#
#   AOT vs interpreter   run-vs-build parity — byte-identical output required
#   kara vs numpy        the differential oracle — EXACT equality required
#
# Requires: karac on PATH or KARAC set; python3 with numpy.
#
# Usage: ./verify.sh [--keep]
set -euo pipefail
cd "$(dirname "$0")"

KARAC="${KARAC:-karac}"
command -v "$KARAC" >/dev/null 2>&1 || {
  echo "error: karac not found — set KARAC=/path/to/karac" >&2
  exit 1
}
python3 -c "import numpy" 2>/dev/null || {
  echo "error: python3 numpy is required for the oracle" >&2
  exit 1
}

WORK="$(mktemp -d)"
[[ "${1:-}" == "--keep" ]] || trap 'rm -rf "$WORK"' EXIT

echo "== generate =="
python3 gen_frames.py "$WORK/in.cstack" --width 96 --height 64 --frames 16 --rays 12

echo "== build =="
"$KARAC" build cumulus.kara -o "$WORK/cumulus"

echo "== generate FITS (same scene, same seed) =="
python3 gen_fits.py "$WORK/fits" --width 96 --height 64 --frames 16 --rays 12

echo "== integrate (AOT) =="
"$WORK/cumulus" "$WORK/mean.cstack" mean "$WORK/in.cstack"
"$WORK/cumulus" "$WORK/clip.cstack" sigmaclip "$WORK/in.cstack"

echo "== integrate (interpreter) =="
"$KARAC" run --interp cumulus.kara -- "$WORK/mean_i.cstack" mean "$WORK/in.cstack"
"$KARAC" run --interp cumulus.kara -- "$WORK/clip_i.cstack" sigmaclip "$WORK/in.cstack"

echo "== integrate from FITS =="
"$WORK/cumulus" "$WORK/mean_f.cstack" mean "$WORK"/fits/sub_*.fits
"$WORK/cumulus" "$WORK/clip_f.cstack" sigmaclip "$WORK"/fits/sub_*.fits

echo "== FITS path equals .cstack path =="
# Same scene and seed, so the two containers must integrate to the same image.
# This is what pins the BZERO round trip: unsigned 16-bit data rides in FITS's
# SIGNED 16-bit format, and a reader that drops BZERO turns stars into holes.
for m in mean clip; do
  if cmp -s "$WORK/$m.cstack" "$WORK/${m}_f.cstack"; then
    echo "  $m: identical"
  else
    echo "  $m: FITS path DIVERGED from the .cstack path" >&2
    exit 1
  fi
done

echo "== run-vs-build parity =="
for m in mean clip; do
  if cmp -s "$WORK/$m.cstack" "$WORK/${m}_i.cstack"; then
    echo "  $m: byte-identical"
  else
    echo "  $m: DIVERGED between AOT and interpreter" >&2
    exit 1
  fi
done

echo "== differential oracle (AOT output) =="
python3 oracle.py "$WORK/in.cstack" "$WORK/mean.cstack" "$WORK/clip.cstack"

echo "== differential oracle (interpreter output) =="
python3 oracle.py "$WORK/in.cstack" "$WORK/mean_i.cstack" "$WORK/clip_i.cstack"

echo "== registration: recover known dithers =="
python3 gen_frames.py "$WORK/dith.cstack" --width 96 --height 64 --frames 16 \
        --rays 12 --dither 3.0 --truth "$WORK/truth.txt"
"$WORK/cumulus" "$WORK/reg.cstack" register "$WORK/dith.cstack" > "$WORK/reg.txt"
python3 check_register.py "$WORK/truth.txt" "$WORK/reg.txt"

echo "== registration parity (interpreter) =="
"$KARAC" run --interp cumulus.kara -- "$WORK/reg_i.cstack" register "$WORK/dith.cstack" \
        > "$WORK/reg_i.txt"
# Compare the OFFSET lines only — the trailing status line names the output
# path, which differs by construction between the two runs.
grep -E '^(frame|ref_stars) ' "$WORK/reg.txt"   > "$WORK/reg.off"
grep -E '^(frame|ref_stars) ' "$WORK/reg_i.txt" > "$WORK/reg_i.off"
if cmp -s "$WORK/reg.off" "$WORK/reg_i.off"; then
  echo "  offsets: byte-identical"
else
  echo "  offsets: DIVERGED between AOT and interpreter" >&2
  diff "$WORK/reg.off" "$WORK/reg_i.off" | head -4 >&2
  exit 1
fi

echo "== registered stack is sharper than an unregistered one =="
# `register` proves the offsets are right; this proves they were USED, and used
# in the RIGHT DIRECTION. A pipeline that measures a correct offset and then
# resamples by its negation passes every other check here and produces a stack
# worse than doing nothing — measured, 0.749x the peak brightness.
"$WORK/cumulus" "$WORK/stack_reg.cstack"   stack     "$WORK/dith.cstack" > /dev/null
"$WORK/cumulus" "$WORK/stack_unreg.cstack" sigmaclip "$WORK/dith.cstack" > /dev/null
python3 check_stack.py "$WORK/stack_reg.cstack" "$WORK/stack_unreg.cstack"

echo "== malformed FITS is refused, not misread =="
# A reader that quietly mishandles BITPIX produces a plausible image, which is
# worse than no image — so the refusals are part of the contract.
python3 - "$WORK" <<'PYEOF'
import struct, sys, os
W = sys.argv[1]; CARD, BLOCK = 80, 2880
def card(k, v): return f"{k:<8}= {str(v):>20}".ljust(CARD).encode()
def hdr(cs):
    h = b"".join(cs); return h + b" " * ((-len(h)) % BLOCK)
open(os.path.join(W, "bad_bitpix.fits"), "wb").write(
    hdr([card("SIMPLE","T"),card("BITPIX",-32),card("NAXIS",2),
         card("NAXIS1",4),card("NAXIS2",4),b"END".ljust(CARD)]) + b"\0"*BLOCK)
open(os.path.join(W, "bad_naxis.fits"), "wb").write(
    hdr([card("SIMPLE","T"),card("BITPIX",16),card("NAXIS",3),card("NAXIS1",4),
         card("NAXIS2",4),card("NAXIS3",3),b"END".ljust(CARD)]) + b"\0"*BLOCK)
open(os.path.join(W, "not_fits.fits"), "wb").write(b"this is not a FITS file" * 200)
PYEOF
for f in bad_bitpix bad_naxis not_fits; do
  msg="$("$WORK/cumulus" "$WORK/junk.cstack" mean "$WORK/$f.fits" 2>&1 | head -1)"
  case "$msg" in
    *"unsupported BITPIX"*|*"unsupported NAXIS"*|*"no END card"*)
      echo "  $f: refused — ${msg##*: }" ;;
    *)
      echo "  $f: expected a refusal, got: $msg" >&2; exit 1 ;;
  esac
done

echo "OK — integration exact, FITS round-trips, dithers recovered, stack sharpened"
