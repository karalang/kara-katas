#!/usr/bin/env python3
"""LeetCode #120 — Python bench mirror (smaller K, timed separately, NOT cross-checked).
Same bottom-up rolling min-path DP as triangle.kara; K = 2000. Its wall-clock is not comparable."""
MOD = 1000000007
def min_path(tri, seed):
    n = len(tri)
    dp = [tri[n-1][j] + ((seed + j) % 7) for j in range(n)]
    for i in range(n-2, -1, -1):
        for k in range(i+1):
            a, b = dp[k], dp[k+1]
            dp[k] = tri[i][k] + (a if a < b else b)
    return dp[0]
def main():
    nrows = 200
    tri = [[(i*31 + j*17) % 100 for j in range(i+1)] for i in range(nrows)]
    acc = 0
    for _ in range(2000):
        seed = acc % 97
        acc = (acc * 131 + min_path(tri, seed)) % MOD
    print(acc)
if __name__ == "__main__":
    main()
