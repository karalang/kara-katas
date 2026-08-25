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

echo "== rotation: recover a known field rotation =="
# An untracked camera sees the sky turn about the pole, which inside a small
# field is a translation PLUS a field rotation. Translation-only registration
# removes the first and leaves the second, and the residue is zero at the frame
# centre and largest in the corners — so a stack can look perfect in the middle
# and be mush at the edges. Measured on a real 20-frame nightscape sequence
# (Nikon Z5, 24mm, 13s, 4m45s): 0.40 deg, which is 25 px of corner error at
# 6016x4016.
#
# Ground truth, not a differential: gen_frames.py rotates the star field about
# the frame centre by a known amount per frame and writes it to the truth file,
# and check_register.py compares what was recovered. It also refuses to pass a
# build that reports zero rotation while rotation was injected — the shape a
# translation-only regression would take.
python3 gen_frames.py "$WORK/rot.cstack" --width 96 --height 64 --frames 8 \
        --rays 0 --rotate 0.5 --truth "$WORK/rot_truth.txt" > /dev/null
"$WORK/cumulus" "$WORK/rot_reg.cstack" register "$WORK/rot.cstack" > "$WORK/rot_reg.txt"
python3 check_register.py "$WORK/rot_truth.txt" "$WORK/rot_reg.txt"

echo "== rotation is APPLIED, not merely measured =="
# `register` proves the angle is recovered; this proves the resampler uses it.
# A build that measured rotation perfectly and then resampled by translation
# alone passes every check above. Concentration is the discriminating metric —
# rotation error is zero at the frame centre, so PEAK barely moves while the
# flux smears outward, and only a concentration comparison sees that.
python3 gen_frames.py "$WORK/bigrot.cstack" --width 640 --height 480 --frames 10 \
        --rays 6 --rotate 0.4 > /dev/null
"$WORK/cumulus" "$WORK/bigrot_stack.cstack"  stack     "$WORK/bigrot.cstack" > /dev/null
"$WORK/cumulus" "$WORK/bigrot_unreg.cstack"  sigmaclip "$WORK/bigrot.cstack" > /dev/null
python3 check_stack.py "$WORK/bigrot_stack.cstack" "$WORK/bigrot_unreg.cstack"

echo "== registered stack is sharper than an unregistered one =="
# `register` proves the offsets are right; this proves they were USED, and used
# in the RIGHT DIRECTION. A pipeline that measures a correct offset and then
# resamples by its negation passes every other check here and produces a stack
# worse than doing nothing — measured, 0.749x the peak brightness.
"$WORK/cumulus" "$WORK/stack_reg.cstack"   stack     "$WORK/dith.cstack" > /dev/null
"$WORK/cumulus" "$WORK/stack_unreg.cstack" sigmaclip "$WORK/dith.cstack" > /dev/null
python3 check_stack.py "$WORK/stack_reg.cstack" "$WORK/stack_unreg.cstack"

echo "== nightscape: sky and foreground registered SEPARATELY =="
# The problem a deep-sky stacker does not have. On a tripod the sky turns and
# the land does not, so ONE transform cannot serve both: registering on stars
# sharpens the stars and smears the land, and not registering does the reverse.
# `--horizon` splits them and `--feather` ramps the join.
#
# Nothing else in this file can see a smeared foreground — such a stack is still
# byte-identical across backends, still passes the integration oracle, still
# recovers its dithers. So this compares three stacks of the same frames and
# checks the ordering only a working mask produces, and refuses to pass a
# fixture whose foreground was never smeared in the first place.
python3 gen_frames.py "$WORK/ns.cstack" --width 240 --height 180 --frames 10 \
        --rays 0 --rotate 0.35 --foreground 120 > /dev/null
"$WORK/cumulus" "$WORK/ns_none.cstack" sigmaclip "$WORK/ns.cstack" > /dev/null
"$WORK/cumulus" "$WORK/ns_sky.cstack"  stack     "$WORK/ns.cstack" > /dev/null
"$WORK/cumulus" "$WORK/ns_mask.cstack" stack --horizon 120 --feather 8 \
        "$WORK/ns.cstack" > /dev/null
python3 check_nightscape.py "$WORK/ns_none.cstack" "$WORK/ns_sky.cstack" \
        "$WORK/ns_mask.cstack" 120

echo "== a container input survives flags before it =="
# `--horizon`/`--feather` are the third and fourth flags, and the input-shape
# test used to count ARGV rather than inputs — so two flag pairs made a single
# `.cstack` look like a FITS sequence and it died with "no END card in header".
# `--dark d.cstack in.cstack` could already trip it with one pair.
"$WORK/cumulus" "$WORK/flagged.cstack" mean --horizon 40 --feather 4 "$WORK/in.cstack" > /dev/null
if cmp -s "$WORK/flagged.cstack" "$WORK/mean.cstack"; then
  echo "  flags before a .cstack: same result as without them"
else
  echo "  a flag before the input changed the result" >&2
  exit 1
fi

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
    *"unsupported BITPIX"*|*"unsupported NAXIS"*|*"unrecognised file"*)
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

echo "== calibration: darks, flats and bias against a clean-scene truth =="
# The only slice whose correctness cannot be checked by comparing two
# implementations — both would apply the same formula to the same masters. What
# makes it checkable is that gen_cal.py knows the CLEAN scene the defects were
# added to, so there is a ground truth neither implementation authored.
python3 gen_cal.py "$WORK/cal" --frames 12 > /dev/null
python3 check_cal.py "$WORK/cumulus" "$WORK/cal"

echo "== CFA: exact integration, injected colours, recovered dithers =="
python3 check_cfa.py "$WORK/cumulus"

echo "== TIFF input: what a camera session actually produces =="
# FITS is what a telescope writes; TIFF is what RAW becomes after Lightroom,
# ACR or darktable, and it is what SLS and Sequator ingest. The oracle is
# transcription: gen_tiff.py rewrites an EXISTING container as one TIFF per
# frame, so stacking the TIFFs must land on the same bytes as stacking the
# container. Zero tolerance — a stride error, a byte-order slip or an
# off-by-one strip offset cannot survive it.
#
# The 8-bit rows are lossy by construction (high byte only), so `--expect`
# writes the container that round trip should land on: still an equality, not a
# tolerance. The odd rows-per-strip values matter because they make the last
# strip PARTIAL, which is where a strip walk goes wrong if it goes wrong.
for variant in 16:little:64 16:big:64 16:little:8 16:big:7 8:little:64 8:big:5; do
  bits=${variant%%:*}; rest=${variant#*:}; end=${rest%%:*}; rps=${rest##*:}
  rm -rf "$WORK/tif" "$WORK/tif_expect.cstack"
  python3 gen_tiff.py "$WORK/tif" --from-cstack "$WORK/in.cstack" \
          --bits "$bits" --endian "$end" --rows-per-strip "$rps" \
          --expect "$WORK/tif_expect.cstack" > /dev/null
  "$WORK/cumulus" "$WORK/tif_a.cstack" stack "$WORK"/tif/*.tif > /dev/null
  "$WORK/cumulus" "$WORK/tif_b.cstack" stack "$WORK/tif_expect.cstack" > /dev/null
  if cmp -s "$WORK/tif_a.cstack" "$WORK/tif_b.cstack"; then
    echo "  ${bits}-bit ${end}-endian, ${rps} rows/strip: identical to the container"
  else
    echo "  ${bits}-bit ${end}-endian, ${rps} rows/strip: DIFFERS from the container" >&2
    exit 1
  fi
done

echo "== TIFF flavours we do not read are refused BY NAME =="
# Every fixture here is a VALID TIFF that other decoders open — real zlib
# strips, real tiles, a real planar layout. That is what makes a refusal a
# statement about Cumulus rather than about a broken fixture, and it is why
# gen_tiff.py goes to the trouble of writing them properly.
for kind in deflate tiled planar float; do
  rm -rf "$WORK/bad_tif"
  python3 gen_tiff.py "$WORK/bad_tif" --width 96 --height 64 --frames 1 \
          --refuse "$kind" --rows-per-strip 16 > /dev/null
  msg="$("$WORK/cumulus" "$WORK/junk.cstack" mean "$WORK"/bad_tif/*.tif 2>&1 | head -1)"
  case "$msg" in
    *"compression"*|*"tiled TIFF"*|*"PlanarConfiguration"*|*"SampleFormat"*)
      echo "  $kind: refused — ${msg##*: }" ;;
    *)
      echo "  $kind: expected a refusal, got: $msg" >&2; exit 1 ;;
  esac
done
printf '\xff\xd8\xff\xe0not a tiff at all' > "$WORK/jpeg.tif"
msg="$("$WORK/cumulus" "$WORK/junk.cstack" mean "$WORK/jpeg.tif" 2>&1 | head -1)"
case "$msg" in
  *"unrecognised file"*) echo "  a JPEG named .tif: refused — ${msg##*— }" ;;
  *) echo "  a JPEG named .tif: expected a refusal, got: $msg" >&2; exit 1 ;;
esac

echo "== RGB TIFF: three planes, one transform =="
# The nightscape case. Registration runs on the median of the three samples —
# a hot pixel usually lands in ONE channel, and a median drops it where a mean
# would divide it by three and let it drag the star's centre — and the single
# transform it recovers drives all three planes. Colour planes of one exposure
# came through one lens; registering them independently could only introduce
# disagreement between them.
python3 gen_tiff.py "$WORK/rgbtif" --width 96 --height 64 --frames 8 \
        --dither 3.0 --truth "$WORK/rgbtif_truth.txt" > /dev/null
"$WORK/cumulus" "$WORK/rgb_reg.cstack" register "$WORK"/rgbtif/*.tif \
        > "$WORK/rgbtif_reg.txt"
python3 check_register.py "$WORK/rgbtif_truth.txt" "$WORK/rgbtif_reg.txt"
"$WORK/cumulus" "$WORK/rgbtif.cstack" stack "$WORK"/rgbtif/*.tif > /dev/null
# check_tiff.py asserts the injected R:G:B ratios came back. Nothing else here
# can see a channel transposition: such a stack is the right size, has sharp
# stars, and passes every other oracle in this file.
python3 check_tiff.py "$WORK/rgbtif.cstack"

echo "== the page's OWN TIFF reader agrees with the compiler's =="
# tiff.mjs is a second implementation of the format, racing the one in
# cumulus.kara. Two self-consistent decoders of one container is exactly where a
# stride or byte-order disagreement hides for months, so they are pinned to each
# other on pixels rather than left to agree by inspection. RGB has the most room
# to disagree (three interleaved samples, a plane argument, a median computed on
# the JS side); the big-endian multi-strip mono file exercises run-splitting.
if command -v node > /dev/null 2>&1 && [[ -f cumulus.wasm ]]; then
  node test_node_tiff.mjs "$WORK/rgbtif" "$WORK/rgbtif.cstack"
  rm -rf "$WORK/monotif"
  python3 gen_tiff.py "$WORK/monotif" --from-cstack "$WORK/in.cstack" \
          --endian big --rows-per-strip 7 > /dev/null
  "$WORK/cumulus" "$WORK/monotif.cstack" stack "$WORK"/monotif/*.tif > /dev/null
  node test_node_tiff.mjs "$WORK/monotif" "$WORK/monotif.cstack"
else
  echo "  no node or no cumulus.wasm — browser TIFF reader NOT checked" >&2
fi

echo "== a THIRD-PARTY encoder's TIFF decodes to the same pixels =="
# Without this, gen_tiff.py and the reader in cumulus.kara share one author's
# mental model of the format, and a mistake made in BOTH is invisible: every
# test above would pass while real files failed. So the fixtures are re-encoded
# by something that has never seen this code, and the stack must not move.
#
# Two tools, in preference order, because neither is everywhere:
#   sips    — macOS ImageIO. Rewrites the IFD in its own layout and, as it
#             happens, the opposite byte order.
#   tiffcp  — libtiff's own copier, so on Linux the control is the format's
#             REFERENCE implementation. `-c none` keeps it uncompressed.
#
# ImageMagick is deliberately NOT in that list. It is an image processor rather
# than a container copier: it may apply colour management, and a Q8 build
# silently halves the depth. Either would make the comparison below fail while
# the reader was correct — a false alarm pointing at the wrong file.
reenc_tool=""
reencode_one() {   # $1 = tool, $2 = in, $3 = out
  case "$1" in
    sips)   sips -s format tiff -s formatOptions none "$2" --out "$3" > /dev/null 2>&1 || true ;;
    tiffcp) tiffcp -c none "$2" "$3" > /dev/null 2>&1 || true ;;
  esac
}
for tool in sips tiffcp; do
  command -v "$tool" > /dev/null 2>&1 || continue
  rm -rf "$WORK/reenc"; mkdir -p "$WORK/reenc"
  probe_src="$WORK/rgbtif/sub_000.tif"
  probe_dst="$WORK/reenc/sub_000.tif"
  reencode_one "$tool" "$probe_src" "$probe_dst"
  if [[ ! -f "$probe_dst" ]]; then
    echo "  $tool: could not re-encode the fixture — trying the next" >&2
    continue
  fi
  # An encoder that changed the image is not a control, it is a second bug
  # source. gen_tiff.py --probe is a THIRD reader — four tags, no pixels — so
  # this question is not answered by either reader under test.
  before="$(python3 gen_tiff.py --probe "$probe_src")"
  after="$(python3 gen_tiff.py --probe "$probe_dst")"
  if [[ "$before" != "$after" ]]; then
    echo "  $tool: changed the image shape ($before -> $after), not a usable control" >&2
    continue
  fi
  # And an encoder that copied the bytes verbatim proves nothing at all.
  if cmp -s "$probe_src" "$probe_dst"; then
    echo "  $tool: copied the file byte for byte, so it re-encoded nothing" >&2
    continue
  fi
  reenc_tool="$tool"
  break
done
if [[ -n "$reenc_tool" ]]; then
  for f in "$WORK"/rgbtif/*.tif; do
    reencode_one "$reenc_tool" "$f" "$WORK/reenc/$(basename "$f")"
  done
  "$WORK/cumulus" "$WORK/reenc.cstack" stack "$WORK"/reenc/*.tif > /dev/null
  order="$(head -c 2 "$WORK/reenc/sub_000.tif")"
  if cmp -s "$WORK/rgbtif.cstack" "$WORK/reenc.cstack"; then
    echo "  $reenc_tool re-encode ($order byte order): byte-identical stack"
  else
    echo "  a $reenc_tool re-encode of the same pixels stacked differently" >&2
    exit 1
  fi
else
  echo "  no usable third-party TIFF encoder (tried sips, tiffcp) — control SKIPPED" >&2
fi

echo "== calibration masters are refused for RGB, not applied per-channel =="
# A dark's hot pixels and a flat's vignetting are both wavelength-dependent, so
# a mono master applied to R, G and B alike is three different wrong
# corrections, not one approximate one.
msg="$("$WORK/cumulus" "$WORK/junk.cstack" stack --dark "$WORK/in.cstack" \
        "$WORK"/rgbtif/*.tif 2>&1 | head -1)"
case "$msg" in
  *"one per channel"*) echo "  refused — ${msg##*: }" ;;
  *) echo "  expected a refusal, got: $msg" >&2; exit 1 ;;
esac

if command -v node >/dev/null 2>&1 && [[ -f cumulus.wasm ]]; then
echo "== wasm kernels equal native =="
  "$WORK/cumulus" "$WORK/w_mean.cstack"  mean  "$WORK/dith.cstack" > /dev/null
  "$WORK/cumulus" "$WORK/w_stack.cstack" stack "$WORK/dith.cstack" > /dev/null
  node test_node.mjs "$WORK/dith.cstack" "$WORK/w_mean.cstack" "$WORK/w_stack.cstack"

  echo "== wasm streams across MULTIPLE strips =="
  # The check above runs at 96x64 — one strip — so the module reads each frame
  # whole and the streaming request pattern is not exercised at all. This one is
  # 200 rows, so pass 2 has to walk 4 strips, and test_node.mjs asserts on the
  # SHAPE of the reads as well as the pixels: no read larger than a strip plus
  # its halo, and no whole-frame read outside pass 1's star detection.
  # Byte-identity alone would not notice a regression back to pulling the whole
  # stack in one call, which is the property the page depends on.
  "$WORK/cumulus" "$WORK/w_tall_mean.cstack" mean "$WORK/tall.cstack" > /dev/null
  node test_node.mjs "$WORK/tall.cstack" "$WORK/w_tall_mean.cstack" "$WORK/tall_res_stack.cstack"

  if [[ -f cumulus.threads.wasm ]]; then
    echo "== threaded wasm equals native (repeated: races are intermittent) =="
    # The page runs the THREADED module; test_node.mjs only ever exercises the
    # sequential one. Eighteen workers writing one output buffer is exactly where
    # a disjointness bug would show, and it would show as a few wrong pixels
    # rather than a crash — so this compares against the native reference, five
    # times, at a size big enough to give the scheduler room to interleave.
    node test_node_threaded.mjs "$WORK/tall.cstack" "$WORK/tall_res_stack.cstack" 2 5
  else
    echo "== threaded wasm check SKIPPED (build with --features wasm-threads) =="
  fi

  # `demo/` is a generated fixture and is gitignored, so a FRESH CLONE has none
  # — and this check used to read that as "no playwright" and skip, which is the
  # same shape of hole as a third-party control that quietly is not there. It is
  # deterministic (fixed seed) and costs a second, so generate it rather than
  # silently doing less. build_web.sh has always done exactly this.
  [[ -d demo ]] || python3 gen_fits.py demo --frames 16 --width 96 --height 64 \
                          --rays 12 --dither 3.0 > /dev/null
  if node -e "require('playwright')" 2>/dev/null; then
    echo "== the real page in a real browser =="
    "$WORK/cumulus" "$WORK/demo_native.cstack" stack demo/*.fits > /dev/null
    node verify_browser.mjs "$WORK/demo_native.cstack" --tiff "$WORK/rgbtif" "$WORK/rgbtif.cstack"
  else
    echo "== browser check SKIPPED (no playwright — npm install playwright) =="
  fi
else
  echo "== wasm checks SKIPPED (no node, or cumulus.wasm not built) =="
fi

echo "OK — integration exact, FITS round-trips, dithers recovered, stack sharpened"
