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

echo "== FITS path equals .cstack path (streamed equals resident) =="
# Same scene and seed, so the two containers must integrate to the same image.
# This pins the BZERO round trip — unsigned 16-bit data rides in FITS's SIGNED
# 16-bit format, and a reader that drops BZERO turns stars into holes.
#
# It is now also the STREAMING oracle, for free: FITS input streams off disk a
# strip at a time while a `.cstack` stays resident, so "the two containers agree"
# and "streaming agrees with holding everything in memory" are the same
# assertion. Byte-identical is the bar — streaming may be slower, never
# different.
for m in mean clip; do
  if cmp -s "$WORK/$m.cstack" "$WORK/${m}_f.cstack"; then
    echo "  $m: identical"
  else
    echo "  $m: FITS path DIVERGED from the .cstack path" >&2
    exit 1
  fi
done

echo "== streaming across MULTIPLE strips =="
# The check above runs at 96x64, which is a single 64-row strip — it never
# advances the window, so it cannot see the part of streaming most likely to be
# wrong. This one is 200 rows (4 strips) WITH a dither, so the window has to
# slide, retain its halo across the boundary, and shrink at the last strip.
#
# The two bugs found while writing it were both invisible at one strip: the
# frame slab was indexed by the window's VALID row count instead of its
# allocated stride (so every frame after the first was read a few rows into its
# neighbour), and a zero halo silently turned strip edges into NO DATA. Both
# produce a plausible image.
python3 gen_frames.py "$WORK/tall.cstack" --width 96 --height 200 --frames 12 \
        --rays 12 --dither 3.0 > /dev/null
python3 gen_fits.py "$WORK/tallf" --width 96 --height 200 --frames 12 \
        --rays 12 --dither 3.0 > /dev/null
for m in mean sigmaclip stack; do
  "$WORK/cumulus" "$WORK/tall_res_$m.cstack" "$m" "$WORK/tall.cstack" > /dev/null
  "$WORK/cumulus" "$WORK/tall_str_$m.cstack" "$m" "$WORK"/tallf/sub_*.fits > /dev/null
  if cmp -s "$WORK/tall_res_$m.cstack" "$WORK/tall_str_$m.cstack"; then
    echo "  $m: streamed over 4 strips == resident"
  else
    echo "  $m: STREAMED DIVERGED from resident" >&2
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

echo "== a colour mosaic is refused by the monochrome modes, and vice versa =="
# A CFA frame stacked as if it were grey does not fail — it produces a plausible
# picture with checkerboard texture and colour-biased star positions. Refusing
# is the only way that mistake becomes visible.
python3 gen_cfa.py "$WORK/cfa" --frames 4 --width 192 --height 128 > /dev/null
msg="$("$WORK/cumulus" "$WORK/junk.cstack" stack "$WORK/cfa"/*.fits 2>&1 | head -1)"
case "$msg" in
  *"Bayer mosaic"*) echo "  mosaic into \`stack\`: refused — ${msg##*: }" ;;
  *) echo "  expected a refusal for a mosaic in a mono mode, got: $msg" >&2; exit 1 ;;
esac
msg="$("$WORK/cumulus" "$WORK/junk.cstack" stackcfa "$WORK/fits"/*.fits 2>&1 | head -1)"
case "$msg" in
  *"needs a BAYERPAT"*) echo "  mono into \`stackcfa\`: refused — ${msg##*: }" ;;
  *) echo "  expected a refusal for mono in a CFA mode, got: $msg" >&2; exit 1 ;;
esac

echo "== CFA: exact integration, injected colours, recovered dithers =="
python3 check_cfa.py "$WORK/cumulus"

if command -v node >/dev/null 2>&1 && [[ -f cumulus.wasm ]]; then
  echo "== wasm kernels equal native =="
  "$WORK/cumulus" "$WORK/w_mean.cstack"  mean  "$WORK/dith.cstack" > /dev/null
  "$WORK/cumulus" "$WORK/w_stack.cstack" stack "$WORK/dith.cstack" > /dev/null
  node test_node.mjs "$WORK/dith.cstack" "$WORK/w_mean.cstack" "$WORK/w_stack.cstack"

  if node -e "require('playwright')" 2>/dev/null && [[ -d demo ]]; then
    echo "== the real page in a real browser =="
    "$WORK/cumulus" "$WORK/demo_native.cstack" stack demo/*.fits > /dev/null
    node verify_browser.mjs "$WORK/demo_native.cstack"
  else
    echo "== browser check SKIPPED (no playwright or no demo/) =="
  fi
else
  echo "== wasm checks SKIPPED (no node, or cumulus.wasm not built) =="
fi

echo "OK — integration exact, FITS round-trips, dithers recovered, stack sharpened"
