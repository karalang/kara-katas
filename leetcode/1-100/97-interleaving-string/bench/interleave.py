"""Benchmark workload for LeetCode #97 — 2D interleaving-string DP, Python mirror.
Smaller K (pure-Python is slow); timed separately, not cross-checked."""

from __future__ import annotations

S1 = ["baacccbabbacacabbbcabbcc", "abcababacbbacbcbccbcac", "abbaabbabacbcaaccbbcbcca", "bacaccbbaaacbaaaabaaaa", "cbabaabcacccbccaabbbc", "bacaacaccaccacabcbbcccb", "aaaccbbbcbaabbbcabbbbabc", "abbabbabcbcccaaacabbccbb", "caccbacaaacabbbcccb", "cccbacbaacbbbcbaaccbb", "aacbcaccaabbaababcccbc", "bbacbaabbabbaabccbacccaa"]
S2 = ["baabaabbbcaccbcaaaaa", "cacccaaaccaaacccbcacabc", "bbacbacccccbaabccaacc", "ccbbaabcaacaccccbcccaca", "abaaabbbbccbaaccca", "babaaccaccbaaaacbcccc", "bbacaaaabaabbabacbcb", "ccbbabaaabaccababacacbbc", "bbccaabcbabcbcacacbccacc", "ccabccacabbbaabacbacb", "babcaabacabcbbcacab", "abbaacaabccbcaababbbbbc"]
S3 = ["baabcaabcacabbbabbcaccbacabccaaaaaabbbcabbcc", "cabacccacbaaabaccacaaabbaccbccbcbccacbcacabcc", "bbaabbaabcbabcacbccaccbbcaaabacccaaccbbcbccca", "baccacccbbbaabaaabccabaacaccccbaacabaaaaccaca", "acbababaaabbbbcacbcbaacccabccccacaabbbc", "babbaacaaaccaccacccabccacabcabbcaccbaacbcccc", "aaabbacacaacabbbaabbbacbabacbcbabbbcabbbbabc", "cabbacbbbabbaaabaacbcbcacccabaaabacacbcbabcbccbb", "bcbacccacababcacbabcaabccaaacabbcbcccccbacc", "cccccbaabcbcacacacbabbbbcbbaabacbacbaaccbb", "aabcabbccaaacbaccabacabbbcbacaabababcccbc", "abbbbaaaccabaabcacbbbabcbaabaabbabbbcbcbaccccaa"]


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
            up = dp[(i - 1) * stride + j] and a[i - 1] == c[i + j - 1]
            left = dp[i * stride + j - 1] and b[j - 1] == c[i + j - 1]
            dp[i * stride + j] = up or left
    return dp[n * stride + m]


def main() -> None:
    acc = 1
    for _ in range(20000):
        idx = acc % 12
        ok = is_interleave(S1[idx], S2[idx], S3[idx])
        acc = (acc * 131 + (1 if ok else 0) + 1) % 1000000007
    print(acc)


if __name__ == "__main__":
    main()
