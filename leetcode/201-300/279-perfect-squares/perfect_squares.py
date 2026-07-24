# LeetCode 279 — Perfect Squares (oracle mirror).
def num_squares(n):
    dp = [0]
    for i in range(1, n + 1):
        best = i; j = 1
        while j * j <= i:
            best = min(best, dp[i - j*j] + 1); j += 1
        dp.append(best)
    return dp[n]
for n in (12, 13, 1, 2, 4, 43, 100): print(num_squares(n))
