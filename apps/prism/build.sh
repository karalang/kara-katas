#!/usr/bin/env bash
# Build Prism to browser WASM and (optionally) serve it.
#
#   ./build.sh                 # build prism.wasm + prism.js next to index.html
#   ./build.sh --serve         # build, then serve on http://localhost:8000
#   ./build.sh --verify        # build, then drive the page in headless Chrome
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

echo "==> building prism (wasm_browser) with $KARAC"
"$KARAC" build prism.kara --target=wasm_browser --features wasm-threads

echo "==> node smoke test (all kernels, exact oracles)"
node test_node.mjs

if [[ "${1:-}" == "--verify" ]]; then
  echo "==> real-browser verification (headless Chrome over CDP)"
  exec node verify_browser.mjs
fi
if [[ "${1:-}" == "--serve" ]]; then
  echo "==> serving on http://localhost:8000 (Ctrl-C to stop)"
  exec python3 serve.py
fi
echo "==> done. Open index.html via any static server to run."
