# LeetCode #920: Number of Music Playlists -- mirrors num_music_playlists.kara
# (the table over the length and the distinct songs so far) and its harness.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(n, goal, k):
    print(f"n = {n}, goal = {goal}, k = {k}: {num_music_playlists(n, goal, k)}")


def main():
    global seed
    show(3, 3, 1)
    show(2, 3, 0)
    show(2, 3, 1)
    show(1, 1, 0)
    show(1, 5, 0)
    show(5, 5, 4)
    show(4, 9, 3)
    show(3, 6, 0)
    show(10, 20, 3)
    show(100, 100, 0)
    show(100, 100, 99)
    show(50, 100, 10)
    show(99, 100, 0)
    show(1, 100, 0)
    count = 0
    total = 0
    check = 0
    for goal in range(1, 31):
        for n in range(1, goal + 1):
            for k in range(n):
                r = num_music_playlists(n, goal, k)
                count += 1
                total += r
                check = (check * 1000003 + r) % 1000000007
    print(f"every case with goal up to 30: {count} cases, answers summing to {total}, checksum {check}")
    seed = 920
    total = 0
    check = 0
    for _ in range(300):
        goal = 1 + next_random() % 100
        n = 1 + next_random() % goal
        k = next_random() % n
        r = num_music_playlists(n, goal, k)
        total += r
        check = (check * 1000003 + r) % 1000000007
    print(f"300 random cases: answers summing to {total}, checksum {check}")


main()
