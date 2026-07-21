#!/usr/bin/env bash
# Sync freshly built app artifacts into a karalang/website checkout — the repo
# that serves karac.dev (GitHub Pages deploys its public/ verbatim on every
# push to main).
#
# This is the ONE direction artifacts flow: kara-katas is the source of truth
# for the apps' source + tests (build artifacts are gitignored here);
# website/public/{prism,veil} is the single deployed-artifact location.
#
#   ./sync-website.sh /path/to/website-checkout
#   # then: cd /path/to/website-checkout && git add public && git commit && git push
set -euo pipefail
cd "$(dirname "$0")"

WEBSITE="${1:?usage: ./sync-website.sh /path/to/karalang-website-checkout}"
[[ -d "$WEBSITE/public" ]] || {
  echo "error: $WEBSITE has no public/ directory — not the website repo?" >&2
  exit 1
}

PRISM=(index.html coi-serviceworker.min.js prism.js prism.wasm prism.threads.wasm)
VEIL=(index.html veil.js veil.wasm)

for f in "${PRISM[@]}"; do
  [[ -f "prism/$f" ]] || { echo "error: prism/$f missing — run prism/build.sh first" >&2; exit 1; }
done
for f in "${VEIL[@]}"; do
  [[ -f "veil/$f" ]] || { echo "error: veil/$f missing — run veil/build.sh first" >&2; exit 1; }
done

mkdir -p "$WEBSITE/public/prism" "$WEBSITE/public/veil"
for f in "${PRISM[@]}"; do cp "prism/$f" "$WEBSITE/public/prism/$f"; done
for f in "${VEIL[@]}"; do cp "veil/$f" "$WEBSITE/public/veil/$f"; done

echo "synced -> $WEBSITE/public/{prism,veil}"
echo "next: commit & push the website repo; GitHub Pages redeploys karac.dev automatically"
