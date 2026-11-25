# LeetCode #1380: Lucky Numbers in a Matrix -- Python mirror of the ★ arm:
# each row's least value and each column's greatest found in one pass,
# then every cell that is both.

seed = 1380


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def lucky_numbers(matrix):
    m, n = len(matrix), len(matrix[0])
    row_min = [2**31 - 1] * m
    col_max = [-(2**31)] * n
    for i in range(m):
        for j in range(n):
            row_min[i] = min(row_min[i], matrix[i][j])
            col_max[j] = max(col_max[j], matrix[i][j])
    return [matrix[i][j] for i in range(m) for j in range(n) if matrix[i][j] == row_min[i] and matrix[i][j] == col_max[j]]


def matrix(m, n, kind):
    cells = m * n
    step = 1 + next_random() % 99990
    start = next_random() % 99991
    values = sorted(1 + (start + k * step) % 99991 for k in range(cells))
    grid = [[0] * n for _ in range(m)]
    free = []
    nxt = 0
    if kind == 1:
        r, c = next_random() % m, next_random() % n
        for i in range(m):
            if i != r:
                grid[i][c] = values[nxt]
                nxt += 1
        grid[r][c] = values[nxt]
        nxt += 1
        top = cells - 1
        for j in range(n):
            if j != c:
                grid[r][j] = values[top]
                top -= 1
        free = [(i, j) for i in range(m) for j in range(n) if i != r and j != c]
    else:
        free = [(i, j) for i in range(m) for j in range(n)]
    rest = values[nxt:nxt + len(free)]
    for i in range(len(rest) - 1, 0, -1):
        j = next_random() % (i + 1)
        rest[i], rest[j] = rest[j], rest[i]
    for k, (i, j) in enumerate(free):
        grid[i][j] = rest[k]
    return grid


def show(lucky):
    return "[" + ",".join(str(v) for v in lucky) + "]"


def main():
    shown = [
        show(lucky_numbers([[3, 7, 8], [9, 11, 13], [15, 16, 17]])),
        show(lucky_numbers([[1, 10, 4, 2], [9, 3, 8, 7], [15, 16, 17, 12]])),
        show(lucky_numbers([[7, 8], [1, 2]])),
        show(lucky_numbers([[i * 50 + j + 1 for j in range(50)] for i in range(50)])),
        show(lucky_numbers([[(i + j) % 50 * 50 + i + 1 for j in range(50)] for i in range(50)])),
    ]
    print(" ".join(shown))
    found = 0
    check = 0
    for c in range(2000):
        m = 1 + next_random() % 50
        n = 1 + next_random() % 50
        lucky = lucky_numbers(matrix(m, n, c % 2))
        found += len(lucky)
        for v in lucky:
            check = (check * 131 + v) % 1000000007
        check = (check * 131 + len(lucky)) % 1000000007
    print(f"2000 random matrices: {found} lucky numbers, checksum {check}")


main()
