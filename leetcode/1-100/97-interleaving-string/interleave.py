"""LeetCode #97: Interleaving String — 2D dynamic programming.

Mirror of interleave.kara. dp[i][j] = can the first i chars of s1 and first j of s2
interleave to form the first i+j chars of s3. Same battery of cases, same fold
(acc = acc*131 + verdict + 1, mod 1e9+7) so the files diff line-for-line.
"""

from __future__ import annotations


def is_interleave(s1: str, s2: str, s3: str) -> bool:
    a, b, c = s1.encode(), s2.encode(), s3.encode()
    n, m = len(a), len(b)
    if n + m != len(c):
        return False
    stride = m + 1
    dp = [False] * ((n + 1) * stride)
    dp[0] = True
    for j in range(1, m + 1):
        dp[j] = dp[j - 1] and b[j - 1] == c[j - 1]
    for i in range(1, n + 1):
        dp[i * stride] = dp[(i - 1) * stride] and a[i - 1] == c[i - 1]
        for j in range(1, m + 1):
            from_up = dp[(i - 1) * stride + j] and a[i - 1] == c[i + j - 1]
            from_left = dp[i * stride + j - 1] and b[j - 1] == c[i + j - 1]
            dp[i * stride + j] = from_up or from_left
    return dp[n * stride + m]


def main() -> None:
    acc = 0
    s1s = ["aabcc", "aabcc", "", "a", "", "abc", "aa", "ab", "abababab", "aaaa"]
    s2s = ["dbbca", "dbbca", "", "", "b", "def", "ab", "cd", "babababa", "bbbb"]
    s3s = ["aadbbcbcac", "aadbbbaccc", "", "a", "b", "adbcef", "aaba", "acbd", "aabbababbaba", "aabbaabb"]
    for k in range(len(s1s)):
        ok = is_interleave(s1s[k], s2s[k], s3s[k])
        acc = (acc * 131 + (1 if ok else 0) + 1) % 1000000007
        print(f"case {k}: {str(ok).lower()}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
