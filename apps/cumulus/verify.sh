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

echo "== integrate (AOT) =="
"$WORK/cumulus" "$WORK/in.cstack" "$WORK/mean.cstack" mean
"$WORK/cumulus" "$WORK/in.cstack" "$WORK/clip.cstack" sigmaclip

echo "== integrate (interpreter) =="
"$KARAC" run --interp cumulus.kara -- "$WORK/in.cstack" "$WORK/mean_i.cstack" mean
"$KARAC" run --interp cumulus.kara -- "$WORK/in.cstack" "$WORK/clip_i.cstack" sigmaclip

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

echo "OK — AOT, interpreter and numpy all agree exactly"
