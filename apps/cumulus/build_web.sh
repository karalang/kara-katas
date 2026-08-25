#!/usr/bin/env bash
# build_web.sh — build the browser bundle and verify it against the native binary.
set -euo pipefail
cd "$(dirname "$0")"
# `karac` on PATH first, the compiler tree second — the same default verify.sh
# uses. A tree-local DEBUG build is often compiled without `--features llvm`,
# and such a karac makes `build` a no-op: it type-checks every target, prints
# nothing about emitting, and exits 0. See the reference-binary guard below for
# what that used to cost.
KARAC="${KARAC:-$(command -v karac || echo ../../../kara/target/debug/karac)}"

# karac resolves the wasm sysroot from the ACTIVE rustup toolchain, but the wasm
# runtime archive was built with the compiler tree's PINNED one. Outside that
# tree those disagree and the build dies telling you to `rustup target add` a
# target that IS installed, just on the other toolchain. (Same footgun Prism
# documents in its build.sh.)
if [[ -z "${RUSTUP_TOOLCHAIN:-}" ]]; then
  tf="$(dirname "$(dirname "$(dirname "$KARAC")")")/rust-toolchain.toml"
  if [[ -f "$tf" ]]; then
    pinned="$(sed -n 's/^channel *= *"\(.*\)"/\1/p' "$tf" | head -1)"
    [[ -n "$pinned" ]] && export RUSTUP_TOOLCHAIN="$pinned" && echo "==> pinned toolchain $pinned"
  fi
fi

echo "==> building cumulus.wasm"
"$KARAC" build cumulus.kara --target=wasm_browser --features wasm-threads

echo "==> demo subs"
[[ -d demo ]] || python3 gen_fits.py demo --frames 16 --width 96 --height 64 --rays 12 --dither 3.0

echo "==> native reference"
# Delete first, then REQUIRE it back. Every "byte-identical to native" claim in
# this script is measured against this binary, and it lives at a fixed path in
# /tmp — so a karac that cannot emit (a debug build without `--features llvm`
# type-checks, prints nothing and exits 0) left the PREVIOUS run's binary lying
# there and the whole suite compared today's wasm against a week-old native.
# That is a vacuous pass of the worst kind: green, and measuring nothing.
# Found because a stale reference could not read TIFF; it had been silently
# stale for FITS since 2026-08-22.
rm -f /tmp/cumulus_ref
"$KARAC" build cumulus.kara -o /tmp/cumulus_ref
[[ -x /tmp/cumulus_ref ]] || {
  echo "error: '$KARAC' did not emit a native binary — a karac built without" >&2
  echo "       --features llvm type-checks and exits 0 without emitting." >&2
  echo "       Build one with: cargo build --features llvm" >&2
  exit 1
}
python3 gen_frames.py /tmp/cw.cstack --width 96 --height 64 --frames 16 --rays 12 --dither 3.0
/tmp/cumulus_ref /tmp/cw_mean.cstack  mean  /tmp/cw.cstack  > /dev/null
/tmp/cumulus_ref /tmp/cw_stack.cstack stack /tmp/cw.cstack  > /dev/null
/tmp/cumulus_ref /tmp/cw_demo.cstack  stack demo/*.fits     > /dev/null

echo "==> wasm equals native"
node test_node.mjs /tmp/cw.cstack /tmp/cw_mean.cstack /tmp/cw_stack.cstack

echo "==> wasm streams across multiple strips"
# 96x64 is a single strip, so the run above reads every frame whole and proves
# nothing about the request pattern. 200 rows makes pass 2 walk 4 strips, and
# test_node.mjs then asserts the read SHAPE as well as the pixels.
python3 gen_frames.py /tmp/cw_tall.cstack --width 96 --height 200 --frames 12 \
        --rays 12 --dither 3.0 > /dev/null
/tmp/cumulus_ref /tmp/cw_tall_mean.cstack  mean  /tmp/cw_tall.cstack > /dev/null
/tmp/cumulus_ref /tmp/cw_tall_stack.cstack stack /tmp/cw_tall.cstack > /dev/null
node test_node.mjs /tmp/cw_tall.cstack /tmp/cw_tall_mean.cstack /tmp/cw_tall_stack.cstack

# The TIFF reader in tiff.mjs is a SECOND implementation of the format, racing
# the Kāra one in cumulus.kara. Two self-consistent decoders of one container is
# exactly where a stride or byte-order disagreement hides, so they are pinned to
# each other on pixels. RGB is the case with the most room to disagree — three
# interleaved samples, a plane argument, a median computed on the JS side —
# and the multi-strip big-endian mono file exercises the run-splitting.
rm -rf /tmp/cw_rgbtif /tmp/cw_monotif
python3 gen_tiff.py /tmp/cw_rgbtif --width 96 --height 64 --frames 8 --dither 3.0 > /dev/null
python3 gen_tiff.py /tmp/cw_monotif --width 96 --height 64 --frames 8 --mono \
        --dither 3.0 --endian big --rows-per-strip 7 > /dev/null
/tmp/cumulus_ref /tmp/cw_rgbtif.cstack  stack /tmp/cw_rgbtif/*.tif  > /dev/null
/tmp/cumulus_ref /tmp/cw_monotif.cstack stack /tmp/cw_monotif/*.tif > /dev/null
node test_node_tiff.mjs /tmp/cw_rgbtif  /tmp/cw_rgbtif.cstack
node test_node_tiff.mjs /tmp/cw_monotif /tmp/cw_monotif.cstack

# The memory model the README quotes is what decides whether a phone survives a
# real stack, so it gets a standing guard rather than a one-off measurement. It
# needs a mid-size frame: at 96x64 the fixed module overhead swamps everything
# that scales with the input, and the check would pass whatever the code did.
if python3 -c "import numpy" 2>/dev/null; then
  echo "==> peak wasm memory stays within the model"
  python3 gen_large.py /tmp/cw_mem.cstack --width 1024 --height 768 --frames 16 >/dev/null
  node mem_probe.mjs /tmp/cw_mem.cstack 2 --assert-model
  rm -f /tmp/cw_mem.cstack
else
  echo "==> memory-model check skipped (needs numpy)"
fi

# ESM `import`, matching how verify_browser.mjs loads it — a CJS `require`
# probe answers a different question (NODE_PATH feeds one and not the other),
# so a global-only playwright passed the gate and then failed inside the script.
if node --input-type=module -e "await import('playwright')" 2>/dev/null; then
  echo "==> the real page in a real browser"
  node verify_browser.mjs /tmp/cw_demo.cstack --tiff /tmp/cw_rgbtif /tmp/cw_rgbtif.cstack "$@"
else
  echo "==> browser check skipped (npm install playwright to enable)"
fi
