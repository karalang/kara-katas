"""LeetCode #96: Unique Binary Search Trees — count via the Catalan recurrence.

Mirror of num_trees.kara. dp[k] = number of structurally unique BSTs over any k
values; dp[n] = sum over roots r of dp[r-1]*dp[n-r], dp[0] = 1. Same per-n print and
same fold (acc = acc*1000003 + count, mod 1e9+7) so the files diff line-for-line.
"""

from __future__ import annotations


def num_trees(n: int) -> int:
    dp = [1]  # dp[0] = 1 (empty tree)
    for k in range(1, n + 1):
        total = 0
        for r in range(1, k + 1):
            total += dp[r - 1] * dp[k - r]  # left count * right count
        dp.append(total)
    return dp[n]


def main() -> None:
    acc = 0
    for n in range(1, 20):
        c = num_trees(n)
        print(f"n={n}: {c}")
        acc = (acc * 1000003 + c) % 1000000007
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
