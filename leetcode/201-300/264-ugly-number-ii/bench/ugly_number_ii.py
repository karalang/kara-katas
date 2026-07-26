#!/usr/bin/env python3
"""Benchmark harness for LeetCode #264 — Ugly Number II.

Mirrors ugly_number_ii.kara algorithm-for-algorithm. Kept as a correctness
oracle for the sink; Python is not a measured lane (see ../README.md).
"""


def nth_ugly(n):
    dp = [1]
    i2 = i3 = i5 = 0
    while len(dp) < n:
        c2 = dp[i2] * 2
        c3 = dp[i3] * 3
        c5 = dp[i5] * 5

        nxt = c2
        if c3 < nxt:
            nxt = c3
        if c5 < nxt:
            nxt = c5

        dp.append(nxt)

        if c2 == nxt:
            i2 += 1
        if c3 == nxt:
            i3 += 1
        if c5 == nxt:
            i5 += 1
    return dp[n - 1]


def main():
    iters = 12000
    sink = 0
    for it in range(iters):
        n = 9000 + (it * 37) % 3001
        sink = (sink * 31 + nth_ugly(n)) % 1000000007
    print(sink)


main()
