#!/usr/bin/env bash
# Build Prism to browser WASM and (optionally) serve it.
#
#   ./build.sh                 # build prism.wasm + prism.js next to index.html
#   ./build.sh --serve         # build, then serve on http://localhost:8000
#   ./build.sh --verify        # build, then drive the page in headless Chrome
#   ./build.sh --bench         # build, then time lanczos seq-vs-threaded there
#   KARAC=/path/to/karac ./build.sh
#
# Prism is a DUAL wasm_browser build (--features wasm-threads): prism.wasm is
# the sequential module, prism.threads.wasm the multicore one. The page picks
# threads when cross-origin isolated — via real COOP/COEP headers (serve.py)
# or the vendored coi-serviceworker shim on headers-blind hosts. The pixel
# kernels are in prism.kara; the browser does codec I/O.
set -euo pipefail
cd "$(dirname "$0")"

# Default to the kara compiler tree's karac if not overridden. karac resolves
# the wasm runtime archives from its own build tree, so a cross-repo build works.
KARAC="${KARAC:-../../../kara/target/debug/karac}"

# karac resolves the wasm sysroot from the ACTIVE rustup toolchain, but the
# wasm runtime archives it links were built with the compiler tree's PINNED
# one. Running from here — outside that tree — those disagree: rustup falls
# back to `stable`, which usually has no wasm32-wasip1 std, and the build dies
# telling you to `rustup target add` a target that IS installed, just on the
# other toolchain. Pin to the channel the archives came from. An explicit
# RUSTUP_TOOLCHAIN from the caller always wins.
if [[ -z "${RUSTUP_TOOLCHAIN:-}" ]]; then
  kara_toolchain_file="$(dirname "$(dirname "$(dirname "$KARAC")")")/rust-toolchain.toml"
  if [[ -f "$kara_toolchain_file" ]]; then
    pinned="$(sed -n 's/^channel *= *"\(.*\)"/\1/p' "$kara_toolchain_file" | head -1)"
    if [[ -n "$pinned" ]]; then
      export RUSTUP_TOOLCHAIN="$pinned"
      echo "==> pinning RUSTUP_TOOLCHAIN=$pinned (from the compiler tree)"
    fi
  fi
fi

echo "==> building prism (wasm_browser) with $KARAC"
"$KARAC" build prism.kara --target=wasm_browser --features wasm-threads

echo "==> node smoke test (all kernels, exact oracles)"
node test_node.mjs

if [[ "${1:-}" == "--verify" ]]; then
  echo "==> real-browser verification (headless Chrome over CDP)"
  exec node verify_browser.mjs
fi
if [[ "${1:-}" == "--bench" ]]; then
  echo "==> real-browser benchmark (sequential vs threaded lanczos)"
  exec node bench_browser.mjs
fi
if [[ "${1:-}" == "--serve" ]]; then
  echo "==> serving on http://localhost:8000 (Ctrl-C to stop)"
  exec python3 serve.py
fi
echo "==> done. Open index.html via any static server to run."
