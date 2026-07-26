#!/usr/bin/env python3
"""Benchmark harness for LeetCode #279 — Perfect Squares.

Mirrors perfect_squares.kara algorithm-for-algorithm. Kept as a correctness
oracle for the sink; Python is not a measured lane (see ../README.md).
"""


def num_squares(n):
    dp = [0]
    for i in range(1, n + 1):
        best = i
        j = 1
        while j * j <= i:
            cand = dp[i - j * j] + 1
            if cand < best:
                best = cand
            j += 1
        dp.append(best)
    return dp[n]


def main():
    iters = 100
    sink = 0
    for it in range(iters):
        n = 25000 + (it * 37) % 5001
        sink = (sink * 31 + num_squares(n)) % 1000000007
    print(sink)


main()
