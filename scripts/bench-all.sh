#!/usr/bin/env bash
# Run every kata bench/bench.sh under leetcode/ and summarize pass/fail.
# Usage: ./scripts/bench-all.sh [--quick]
#   --quick  skip katas whose bench.sh comments mark long workloads (>1s kara)
#
# Logs: scripts/bench-logs/<kata-id>.log

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT/scripts/bench-logs"
mkdir -p "$LOG_DIR"

QUICK=0
if [ "${1:-}" = "--quick" ]; then
    QUICK=1
fi

pass=0
fail=0
skip=0

while IFS= read -r bench; do
    dir="$(dirname "$bench")"
    rel="${dir#$ROOT/}"
    id="$(echo "$rel" | sed 's|leetcode/||; s|/bench||')"
    log="$LOG_DIR/${id//\//_}.log"

    if [ "$QUICK" = 1 ] && grep -q 'long-bucket\|kara ~10s\|K=50_000_000\|k_iters: i64 = 50_000_000' "$bench" 2>/dev/null; then
        echo "SKIP  $id (long workload — run ./bench/bench.sh manually)"
        skip=$((skip + 1))
        continue
    fi

    echo "RUN   $id ..."
    if ( cd "$dir" && ./bench.sh ) >"$log" 2>&1; then
        echo "PASS  $id  (log: scripts/bench-logs/${id//\//_}.log)"
        pass=$((pass + 1))
    else
        echo "FAIL  $id  (log: scripts/bench-logs/${id//\//_}.log)"
        tail -5 "$log" >&2 || true
        fail=$((fail + 1))
    fi
done < <(find "$ROOT/leetcode" -path '*/bench/bench.sh' | sort)

echo
echo "Summary: $pass passed, $fail failed, $skip skipped"
