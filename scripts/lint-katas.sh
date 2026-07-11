#!/usr/bin/env bash
# lint-katas.sh — structural lints for the kata corpus. Run in CI (see
# .github/workflows/lint.yml) and locally before pushing.
#
# Check: every kata's bench/bench.sh is committed with the executable bit
# (git mode 100755). A harness committed 100644 aborts at run time with
# "permission denied" (exit 126) — this has recurred across several kata
# additions (#73/#74/#75), each caught only when its bench.sh first ran, so it
# is now a gate.
#
# Exit 0 = clean; exit 1 = one or more violations (each printed with the fix).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

# `git ls-files -s` emits: "<mode> <sha> <stage>\t<path>". Select the tracked
# bench harnesses whose mode is not 100755. (Git pathspec `*` matches `/`, so
# this globs every */bench/bench.sh in the tree — leetcode and bespoke alike.)
offenders="$(git ls-files -s -- '*/bench/bench.sh' \
    | awk '$1 != "100755" { sub(/^[^\t]*\t/, ""); print }')"

if [ -n "$offenders" ]; then
    echo "lint-katas: FAIL — bench.sh committed without the executable bit (git mode != 100755):" >&2
    while IFS= read -r p; do
        echo "  $p" >&2
    done <<<"$offenders"
    echo >&2
    echo "  Fix each:  git update-index --chmod=+x <path>   (or: chmod +x <path> && git add <path>)" >&2
    echo "  Why: a 100644 bench.sh aborts at run time with 'permission denied' (exit 126)." >&2
    exit 1
fi

count="$(git ls-files -- '*/bench/bench.sh' | wc -l | tr -d ' ')"
echo "lint-katas: OK — all ${count} bench/bench.sh files are executable (mode 100755)"
