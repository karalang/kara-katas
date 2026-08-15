#!/usr/bin/env python3
"""LeetCode 276 — Paint Fence. Mirror of the ★ solver.

Same two rolling states, same base cases: `same[2] = k` and `diff[2] = k*(k-1)`,
which sum to k² because every two-post painting is legal.
"""


def num_ways(n, k):
    if n == 0:
        return 0
    if n == 1:
        return k
    same, diff = k, k * (k - 1)
    for _ in range(3, n + 1):
        same, diff = diff, (same + diff) * (k - 1)
    return same + diff


def main():
    cases = [(1, 1), (1, 5), (2, 2), (3, 2), (7, 2), (2, 4), (3, 4), (4, 3),
             (10, 3), (20, 2)]
    for n, k in cases:
        print(f"n={n} k={k} -> {num_ways(n, k)}")


main()
