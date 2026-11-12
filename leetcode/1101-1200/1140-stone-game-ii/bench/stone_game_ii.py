# LeetCode #1140: Stone Game II -- the bench in Python, the ★ arm's algorithm.


def stone_game_ii(piles):
    n = len(piles)
    left = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        left[i] = left[i + 1] + piles[i]
    best = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for m in range(1, n + 1):
            if i + 2 * m >= n:
                best[i][m] = left[i]
            else:
                most = 0
                for x in range(1, 2 * m + 1):
                    most = max(most, left[i] - best[i + x][max(m, x)])
                best[i][m] = most
    return best[0][1]


seed = 1140


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rows = [[next_random() % 10000 + 1 for _ in range(100)] for _ in range(20)]
    total = 0
    check = 0
    for _ in range(100):
        for r in range(20):
            at = next_random() % 100
            rows[r][at] = next_random() % 10000 + 1
            answer = stone_game_ii(rows[r])
            total += answer
            check = (check * 131 + answer + 1) % 1000000007
    print(f"100 rounds over 20 rows of 100 piles: answers total {total}, checksum {check}")


main()
