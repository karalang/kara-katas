"""LeetCode 312 - Burst Balloons.

Mirror of burst_balloons.kara: the same last-burst interval DP, filled
shortest-interval-first over a padded array. Kept algorithm-for-algorithm so
the benchmark lane is honest.
"""

import sys


def max_coins(nums):
    n = len(nums)
    if n == 0:
        return 0

    a = [1] + list(nums) + [1]
    w = n + 2
    dp = [[0] * w for _ in range(w)]

    for length in range(2, w):
        for i in range(0, w - length):
            j = i + length
            best = 0
            for k in range(i + 1, j):
                coins = dp[i][k] + dp[k][j] + a[i] * a[k] * a[j]
                if coins > best:
                    best = coins
            dp[i][j] = best

    return dp[0][n + 1]


def report(nums):
    print("[" + ",".join(str(v) for v in nums) + "] -> " + str(max_coins(nums)))


def main():
    report([3, 1, 5, 8])
    report([1, 5])
    report([])
    report([7])
    report([3, 0, 5])
    report([0, 0, 0])
    report([1, 2, 3, 4, 5])
    report([5, 4, 3, 2, 1])
    report([2, 2, 2, 2])
    report([1, 1, 1, 1, 1, 1])
    report([1, 100, 1])
    report([9, 76, 64, 21, 97, 60])


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
