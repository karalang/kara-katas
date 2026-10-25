# Benchmark: LeetCode #1000 Minimum Cost to Merge Stones -- the ★ arm,
# an interval table by length, on rows of up to 30 piles, LeetCode's
# largest. Mirrors merge_stones.kara, .c, .rs and go-seq/.


def merge_stones(stones, k):
    n = len(stones)
    if (n - 1) % (k - 1) != 0:
        return -1
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stones[i]
    dp = [[0] * n for _ in range(n)]
    for length in range(k, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = 1 << 60
            m = i
            while m < j:
                best = min(best, dp[i][m] + dp[m + 1][j])
                m += k - 1
            if (length - 1) % (k - 1) == 0:
                best += prefix[j + 1] - prefix[i]
            dp[i][j] = best
    return dp[0][n - 1]


seed = 1000


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 5000
    # 20 rows, k from 2 to 11 twice over, each with as many piles of 1 to
    # 100 stones, up to 30, as k can merge down to one pile
    rows = []
    ks = []
    for t in range(20):
        k = 2 + t % 10
        n = 1 + 29 // (k - 1) * (k - 1)
        rows.append([1 + next_random() % 100 for _ in range(n)])
        ks.append(k)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            t = (r + i) % 20
            got = merge_stones(rows[t], ks[t])
            total += got
            check = (check * 31 + got + 2) % 1000000007
    print(f"{rounds} rounds over 20 rows of up to 30 piles: cost {total}, checksum {check}")


main()
