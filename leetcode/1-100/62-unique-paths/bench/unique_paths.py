"""Benchmark workload — Unique Paths (LeetCode #62).

Python mirror of bench/unique_paths.kara. Same rolling-DP array (list) allocated
per call, the same dp[c] += dp[c-1] recurrence, the same k%span shape sweep, and
the same rolling polynomial-hash sink. CPython is multi-second per sample at the
compiled mirrors' K=1_000_000, so this runs K=100_000 (1/10th) — timed
separately and NOT cross-checked against the compiled sink. See
../README.md § Benchmarks.
"""

from __future__ import annotations


def unique_paths(m: int, n: int) -> int:
    rows, cols = m, n
    if cols > rows:
        rows, cols = cols, rows

    dp = [1] * cols
    for _ in range(1, rows):
        for c in range(1, cols):
            dp[c] += dp[c - 1]
    return dp[cols - 1]


def main() -> None:
    total = 100_000
    modulus = 1_000_000_007
    span = 32

    acc = 0
    for k in range(total):
        m = 2 + (k % span)
        n = 2 + ((k // span) % span)
        ans = unique_paths(m, n)
        acc = (acc * 131 + ans) % modulus
    print(acc)


if __name__ == "__main__":
    main()
