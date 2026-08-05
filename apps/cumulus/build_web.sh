#!/usr/bin/env bash
# build_web.sh — build the browser bundle and verify it against the native binary.
set -euo pipefail
cd "$(dirname "$0")"
KARAC="${KARAC:-../../../kara/target/debug/karac}"

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
"$KARAC" build cumulus.kara --target=wasm_browser

echo "==> demo subs"
[[ -d demo ]] || python3 gen_fits.py demo --frames 16 --width 96 --height 64 --rays 12 --dither 3.0

echo "==> native reference"
"$KARAC" build cumulus.kara -o /tmp/cumulus_ref
python3 gen_frames.py /tmp/cw.cstack --width 96 --height 64 --frames 16 --rays 12 --dither 3.0
/tmp/cumulus_ref /tmp/cw_mean.cstack  mean  /tmp/cw.cstack  > /dev/null
/tmp/cumulus_ref /tmp/cw_stack.cstack stack /tmp/cw.cstack  > /dev/null
/tmp/cumulus_ref /tmp/cw_demo.cstack  stack demo/*.fits     > /dev/null

echo "==> wasm equals native"
node test_node.mjs /tmp/cw.cstack /tmp/cw_mean.cstack /tmp/cw_stack.cstack

if node -e "require('playwright')" 2>/dev/null; then
  echo "==> the real page in a real browser"
  node verify_browser.mjs /tmp/cw_demo.cstack "$@"
else
  echo "==> browser check skipped (npm install playwright to enable)"
fi
