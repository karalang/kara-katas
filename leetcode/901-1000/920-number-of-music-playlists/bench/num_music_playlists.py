# LeetCode #920: Number of Music Playlists -- bench: a table over the
# length and the distinct songs so far. Mirrors num_music_playlists.kara.


def num_music_playlists(n, goal, k):
    modulus = 1000000007
    dp = [[0] * (n + 1) for _ in range(goal + 1)]
    dp[0][0] = 1
    for i in range(1, goal + 1):
        for j in range(1, min(i, n) + 1):
            fresh = dp[i - 1][j - 1] * (n - j + 1) % modulus
            again = dp[i - 1][j] * (j - k) % modulus if j > k else 0
            dp[i][j] = (fresh + again) % modulus
    return dp[goal][n]


def main():
    top = 64
    count = 0
    total = 0
    check = 0
    for goal in range(1, top + 1):
        for n in range(1, goal + 1):
            for k in range(n):
                r = num_music_playlists(n, goal, k)
                count += 1
                total += r
                check = (check * 1000003 + r) % 1000000007
    print(f"every case with goal up to {top}: {count} cases, answers summing to {total}, checksum {check}")


main()
