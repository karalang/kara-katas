"""Benchmark workload — Minimum Path Sum (LeetCode #64).

Python mirror of bench/minimum_path_sum.kara. Same rolling-DP array (list)
allocated per call, sized to the real column count n, the same
dp[c] = cost + min(dp[c], dp[c-1]) recurrence, the same inline cost predicate
((i*7 + c*3 + k) % 13 + 1), the same k%span shape sweep, and the same rolling
polynomial-hash sink. CPython is multi-second per sample at the compiled mirrors'
K=1_000_000, so this runs K=100_000 (1/10th) — timed separately and NOT
cross-checked against the compiled sink. See ../README.md § Benchmarks.
"""

from __future__ import annotations


def min_path_sum(m: int, n: int, k: int) -> int:
    cols = n
    dp = [0] * cols
    for j in range(cols):
        cost = ((j * 3 + k) % 13) + 1  # i == 0
        dp[j] = cost if j == 0 else dp[j - 1] + cost

    for i in range(1, m):
        dp[0] += ((i * 7 + k) % 13) + 1
        for c in range(1, cols):
            cost = ((i * 7 + c * 3 + k) % 13) + 1
            dp[c] = cost + min(dp[c], dp[c - 1])
    return dp[cols - 1]


def main() -> None:
    total = 100_000
    modulus = 1_000_000_007
    span = 32

    acc = 0
    for k in range(total):
        m = 2 + (k % span)
        n = 2 + ((k // span) % span)
        ans = min_path_sum(m, n, k)
        acc = (acc * 131 + ans) % modulus
    print(acc)


if __name__ == "__main__":
    main()
