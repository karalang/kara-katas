# LeetCode #115 bench — distinct subsequences, Python mirror (smaller K, timed separately).
MOD = 1000000007
def num_distinct(s, t):
    m, n = len(s), len(t)
    dp = [[1 if j == 0 else 0 for j in range(n+1)] for _ in range(m+1)]
    for r in range(1, m+1):
        for c in range(1, n+1):
            skip = dp[r-1][c]
            dp[r][c] = skip + dp[r-1][c-1] if s[r-1]==t[c-1] else skip
    return dp[m][n]
ss = ["abcabcabcabcabcabcabcabc","aabbccaabbccaabbccaabbcc","abababababababababababab","xyzxyzxyzxyzxyzxyzxyzxyz","aaabbbcccaaabbbcccaaabbb","cbacbacbacbacbacbacbacba","abcabcabcabcabcabcabcabc","aabbaabbaabbaabbaabbaabb"]
ts = ["abcabc","abcabc","ababa","xyzxy","abcab","cbacb","cba","abab"]
acc = 1
for _ in range(20000):
    idx = acc % 8
    acc = (acc*1000003 + num_distinct(ss[idx], ts[idx]) + 1) % MOD
print(acc)
