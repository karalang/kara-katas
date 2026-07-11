"""Benchmark workload for LeetCode #96 — Catalan DP-table, Python mirror.
Smaller K than the compiled mirrors (pure-Python loop is slow); timed separately,
not cross-checked against the sink."""

from __future__ import annotations


def num_trees(n: int) -> int:
    dp = [1]
    for k in range(1, n + 1):
        total = 0
        for r in range(1, k + 1):
            total += dp[r - 1] * dp[k - r]
        dp.append(total)
    return dp[n]


def main() -> None:
    acc = 1
    for _ in range(300000):
        m = 2 + (acc % 18)
        c = num_trees(m)
        acc = (acc * 1000003 + c) % 1000000007
    print(acc)


if __name__ == "__main__":
    main()
