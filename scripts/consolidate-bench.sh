#!/usr/bin/env bash
# consolidate-bench.sh — merge every per-kata bench/results.json into one
# top-level bench-results.json, the single feed a dashboard reads.
#
# Usage: ./scripts/consolidate-bench.sh [-o OUTPUT]
#   -o OUTPUT   output path (default: <repo-root>/bench-results.json)
#
# Discovers all leetcode/*/*/bench/results.json, validates each carries the
# expected schema_version, and emits:
#
#   {
#     "schema_version": 1,
#     "generated_at": "<UTC>",
#     "kata_count": N,
#     "katas": [ <each per-kata results.json>, ... ]   # sorted by numeric id
#   }
#
# A kata that has no results.json yet (bench never run, or run before the JSON
# pipeline landed) is simply absent — its omission is logged to stderr so a
# stale feed is never silently mistaken for full coverage.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/bench-results.json"
SCHEMA_VERSION=1

while [ $# -gt 0 ]; do
    case "$1" in
        -o) OUT="$2"; shift 2 ;;
        *) echo "consolidate-bench: unknown arg '$1'" >&2; exit 2 ;;
    esac
done

# Collect result files, sorted. (find|sort keeps macOS bash 3.2 happy — no
# mapfile.)
files=()
while IFS= read -r f; do
    files+=("$f")
done < <(find "$ROOT/leetcode" -path '*/bench/results.json' | sort)

if [ "${#files[@]}" -eq 0 ]; then
    echo "consolidate-bench: no per-kata results.json found under leetcode/ — " \
         "run a kata's bench.sh first" >&2
    exit 1
fi

# Warn on any schema-version skew before merging.
for f in "${files[@]}"; do
    v="$(jq -r '.schema_version // "missing"' "$f")"
    if [ "$v" != "$SCHEMA_VERSION" ]; then
        echo "consolidate-bench: WARNING $f has schema_version=$v " \
             "(expected $SCHEMA_VERSION) — re-run its bench.sh" >&2
    fi
done

# Which kata bench dirs have a bench.sh but no results.json? Report them so the
# coverage gap is explicit (never silently truncate).
while IFS= read -r benchsh; do
    dir="$(dirname "$benchsh")"
    if [ ! -f "$dir/results.json" ]; then
        echo "consolidate-bench: no results.json for ${dir#"$ROOT"/} " \
             "(bench.sh not yet migrated/run)" >&2
    fi
done < <(find "$ROOT/leetcode" -path '*/bench/bench.sh' | sort)

now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

jq -s \
    --arg now "$now" --argjson sv "$SCHEMA_VERSION" \
    '{
        schema_version: $sv,
        generated_at: $now,
        kata_count: length,
        katas: (sort_by(.kata.id | tonumber? // 0))
     }' "${files[@]}" >"$OUT"

echo "consolidate-bench: wrote $OUT ($(jq '.kata_count' "$OUT") katas)" >&2
