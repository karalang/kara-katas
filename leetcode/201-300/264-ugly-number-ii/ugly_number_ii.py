# LeetCode 264 — Ugly Number II (oracle mirror).
def nth_ugly(n):
    dp = [1]; i2 = i3 = i5 = 0
    while len(dp) < n:
        c2, c3, c5 = dp[i2]*2, dp[i3]*3, dp[i5]*5
        nxt = min(c2, c3, c5)
        dp.append(nxt)
        if c2 == nxt: i2 += 1
        if c3 == nxt: i3 += 1
        if c5 == nxt: i5 += 1
    return dp[n-1]
for n in (1, 10, 11, 15, 20, 30): print(nth_ugly(n))
