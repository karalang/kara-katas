#!/usr/bin/env bash
# Convert every graphs/*.svg to a 2x PNG (GitHub renders PNG reliably; its SVG
# proxy sometimes blanks these charts). Run after scripts/bench-graph.py.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
command -v rsvg-convert >/dev/null || { echo "render-png: need rsvg-convert (brew install librsvg)"; exit 1; }
for svg in "$ROOT"/graphs/*.svg; do
    png="${svg%.svg}.png"
    rsvg-convert --zoom 2 -o "$png" "$svg"
done
echo "render-png: wrote $(ls "$ROOT"/graphs/*.png | wc -l | tr -d ' ') PNGs"
