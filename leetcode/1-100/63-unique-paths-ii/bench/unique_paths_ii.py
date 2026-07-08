"""Benchmark workload — Unique Paths II (LeetCode #63).

Python mirror of bench/unique_paths_ii.kara. Same rolling-DP array (list)
allocated per call, sized to the real column count n, the same dp[c] += dp[c-1]
recurrence, the same inline obstacle predicate ((i*7 + c*3 + k) % 13 == 0), the
same k%span shape sweep, and the same rolling polynomial-hash sink. CPython is
multi-second per sample at the compiled mirrors' K=1_000_000, so this runs
K=100_000 (1/10th) — timed separately and NOT cross-checked against the compiled
sink. See ../README.md § Benchmarks.
"""

from __future__ import annotations


def unique_paths_with_obstacles(m: int, n: int, k: int) -> int:
    cols = n
    dp = [0] * cols
    dp[0] = 1
    for i in range(m):
        for c in range(cols):
            if (i * 7 + c * 3 + k) % 13 == 0:
                dp[c] = 0
            elif c > 0:
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
        ans = unique_paths_with_obstacles(m, n, k)
        acc = (acc * 131 + ans) % modulus
    print(acc)


if __name__ == "__main__":
    main()
