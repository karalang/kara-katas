#!/usr/bin/env python3
"""LeetCode #115: Distinct Subsequences — 2-D DP (mirror of num_distinct.kara).

dp[i][j] = number of distinct subsequences of s[:i] equal to t[:j]. Empty target: one way
(dp[i][0]=1). s[i-1] can be skipped (dp[i-1][j]); when it equals t[j-1] it can also match
(+ dp[i-1][j-1]).
"""


def num_distinct(s, t):
    m, n = len(s), len(t)
    dp = [[1 if j == 0 else 0 for j in range(n + 1)] for _ in range(m + 1)]
    for r in range(1, m + 1):
        for c in range(1, n + 1):
            skip = dp[r - 1][c]
            if s[r - 1] == t[c - 1]:
                dp[r][c] = skip + dp[r - 1][c - 1]
            else:
                dp[r][c] = skip
    return dp[m][n]


PAIRS = [
    ("rabbbit", "rabbit"), ("babgbag", "bag"), ("aaaaaa", "aaa"),
    ("abcabcabc", "abc"), ("xyzzyx", "xz"), ("banana", "ban"),
    ("mississippi", "issi"), ("aaaaaaaaaa", "aaaaa"),
]


def main():
    acc = 0
    for i, (s, t) in enumerate(PAIRS):
        c = num_distinct(s, t)
        acc = (acc * 131 + c) % 1000000007
        print(f"pair {i}: count={c}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
