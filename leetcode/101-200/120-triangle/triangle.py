#!/usr/bin/env python3
"""LeetCode #120 — Python mirror of the bottom-up rolling `triangle.kara`.
Same algorithm: seed dp with the base row, collapse each row in place `dp[k] = tri[i][k] +
min(dp[k], dp[k+1])` up to the apex. Produces the byte-identical output to the Kara solver."""

MOD = 1000000007


def minimum_total(tri):
    n = len(tri)
    if n == 0:
        return 0
    dp = [0] * n
    for j in range(n):
        dp[j] = tri[n - 1][j]
    for i in range(n - 2, -1, -1):
        for k in range(i + 1):
            a, b = dp[k], dp[k + 1]
            dp[k] = tri[i][k] + (a if a < b else b)
    return dp[0]


def main():
    print("example1:", minimum_total([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]))
    print("example2:", minimum_total([[-10]]))
    print("example3:", minimum_total([[1], [2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13, 14, 15]]))
    acc = 0
    for h in range(1, 41):
        tri = [[(i * 31 + j * 17 + h * 7) % 100 for j in range(i + 1)] for i in range(h)]
        acc = (acc * 131 + minimum_total(tri) + h) % MOD
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
