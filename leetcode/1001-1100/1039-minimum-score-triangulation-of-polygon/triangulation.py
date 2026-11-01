# LeetCode #1039: Minimum Score Triangulation of Polygon -- mirror of
# triangulation.kara


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


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    examples = [
        [1, 2, 3],
        [3, 7, 4, 5],
        [1, 3, 1, 4, 1, 5],
        [100, 100, 100],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [5, 1, 5, 1, 5, 1],
        [2, 100, 3, 100, 4],
        [35, 73, 90, 27, 71, 80, 21, 33, 33, 13, 48, 12, 68, 70, 80, 36, 66, 3, 70, 58],
    ]
    for values in examples:
        print(f"{show(values)} -> {min_score_triangulation(values)}")
    for n in range(3, 8):
        count = 3 ** n
        total = 0
        check = 0
        for code in range(count):
            values = []
            c = code
            for _ in range(n):
                values.append(c % 3 + 1)
                c //= 3
            score = min_score_triangulation(values)
            total += score
            check = (check * 131 + score) % 1000000007
        print(f"all {count} polygons of {n} vertices from 1 to 3: total {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(300):
        n = next_random() % 48 + 3
        values = [next_random() % 100 + 1 for _ in range(n)]
        score = min_score_triangulation(values)
        total += score
        check = (check * 131 + score) % 1000000007
    print(f"300 random polygons: total {total}, checksum {check}")
    print(f"50 vertices of 100: {min_score_triangulation([100] * 50)}")
    print(f"1 to 50: {min_score_triangulation(list(range(1, 51)))}")


main()
