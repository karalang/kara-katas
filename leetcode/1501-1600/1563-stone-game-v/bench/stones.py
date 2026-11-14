# LeetCode #1563: Stone Game V -- bench: the ★ arm (every stretch,
# shortest first, every split) over 5 rows of 400 stones of 1 to 10^6,
# built once, each asked twice.
# Python mirror of stones.kara.


def stone_game_v(row):
    n = len(row)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + row[i]
    best = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            most = 0
            for k in range(i, j):
                left = prefix[k + 1] - prefix[i]
                right = prefix[j + 1] - prefix[k + 1]
                if left < right:
                    most = max(most, left + best[i][k])
                elif left > right:
                    most = max(most, right + best[k + 1][j])
                else:
                    most = max(most, left + max(best[i][k], best[k + 1][j]))
            best[i][j] = most
    return best[0][n - 1]


seed = 1563


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    rows = [[(next_random() * 32768 + next_random()) % 1000000 + 1 for _ in range(400)] for _ in range(5)]
    check = 0
    total = 0
    for _ in range(2):
        for row in rows:
            score = stone_game_v(row)
            total += score
            check = mix(check, score)
    print(f"2 passes over 5 rows of 400 stones: {total} points, checksum {check}")


main()
