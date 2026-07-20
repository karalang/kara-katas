#!/usr/bin/env bash
# Build Prism to browser WASM and (optionally) serve it.
#
#   ./build.sh                 # build prism.wasm + prism.js next to index.html
#   ./build.sh --serve         # build, then serve on http://localhost:8000
#   KARAC=/path/to/karac ./build.sh
#
# Prism is a SEQUENTIAL wasm_browser build — it runs on the main thread, so it
# needs no SharedArrayBuffer and no COOP/COEP headers (a plain static server is
# fine). The pixel kernels are in prism.kara; the browser does codec I/O.
set -euo pipefail
cd "$(dirname "$0")"

# Default to the kara compiler tree's karac if not overridden. karac resolves
# the wasm runtime archives from its own build tree, so a cross-repo build works.
KARAC="${KARAC:-../../../kara/target/debug/karac}"

echo "==> building prism (wasm_browser) with $KARAC"
"$KARAC" build prism.kara --target=wasm_browser

echo "==> node smoke test (grayscale over a known image)"
node test_node.mjs

if [[ "${1:-}" == "--serve" ]]; then
  echo "==> serving on http://localhost:8000 (Ctrl-C to stop)"
  exec python3 -m http.server 8000
fi
echo "==> done. Open index.html via any static server to run."
