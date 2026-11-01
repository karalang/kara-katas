# LeetCode #1039: Minimum Score Triangulation of Polygon -- bench
# Mirrors ../triangulation.kara; see ../README.md § Benchmarks.


def min_score_triangulation(values):
    n = len(values)
    best = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            least = None
            for k in range(i + 1, j):
                score = best[i][k] + best[k][j] + values[i] * values[k] * values[j]
                if least is None or score < least:
                    least = score
            best[i][j] = least
    return best[0][n - 1]


seed = 1039


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 2000, 10
    polygons = [[next_random() % 100 + 1 for _ in range(50)] for _ in range(count)]
    total = 0
    check = 0
    for _ in range(rounds):
        for values in polygons:
            score = min_score_triangulation(values)
            total += score
            check = (check * 131 + score) % 1000000007
    print(f"{count} polygons of 50 vertices, {rounds} rounds: total {total}, checksum {check}")


main()
