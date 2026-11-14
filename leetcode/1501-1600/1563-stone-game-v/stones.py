# LeetCode #1563: Stone Game V -- the Python mirror of stones.kara, the ★
# arm: the best score of every stretch, shortest first, over every split.
# Prints byte-identical output.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % most + 1
        row = [(next_random() * 32768 + next_random()) % top + 1 for _ in range(n)]
        score = stone_game_v(row)
        total += score
        check = mix(check, score)
    print(f"{count} rows of up to {most} stones of up to {top}: {total} points, checksum {check}")


def main():
    global seed
    examples = [
        [6, 2, 3, 4, 5, 5],
        [7, 7, 7, 7, 7, 7, 7],
        [4],
        [1, 1],
        [1, 2],
        [2, 1, 1],
        [1, 1, 1, 1],
        [10, 1, 1, 1],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    ]
    for row in examples:
        print(f"{row} -> {stone_game_v(row)}")
    seed = 1563
    batch(3000, 8, 10)
    batch(300, 60, 1000000)
    batch(20, 300, 1000000)


main()
