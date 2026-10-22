# LeetCode #861: Score After Flipping Matrix -- Python mirror of the ★ arm
# (count each column against the first).


def matrix_score(grid):
    m = len(grid)
    n = len(grid[0])
    score = 0
    for j in range(n):
        ones = 0
        for row in grid:
            if row[j] == row[0]:
                ones += 1
        score = score * 2 + max(ones, m - ones)
    return score


def show(grid):
    print(f"{grid} -> {matrix_score(grid)}")


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def zeros(m, n):
    return [[0] * n for _ in range(m)]


def main():
    global seed
    for grid in [[[0, 0, 1, 1], [1, 0, 1, 0], [1, 1, 0, 0]], [[0]], [[1]], [[0, 0]],
                 [[0], [0], [1]], [[1, 0], [1, 1]], [[0, 1], [1, 0]], [[1, 1, 1], [0, 0, 0]],
                 [[0, 1, 1, 0, 1]], [[1, 0], [1, 0], [1, 1]],
                 [[1, 0, 0, 1], [1, 0, 1, 0], [1, 1, 0, 0], [1, 0, 0, 0]],
                 [[0, 1, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0]]]:
        show(grid)
    grid = zeros(20, 20)
    print(f"20 by 20, all zeros -> {matrix_score(grid)}")
    for i in range(20):
        for j in range(20):
            grid[i][j] = (i + j) % 2
    print(f"20 by 20, a chessboard -> {matrix_score(grid)}")
    grids = 0
    total = 0
    for m in range(1, 4):
        for n in range(1, 4):
            for code in range(1 << (m * n)):
                g = zeros(m, n)
                for k in range(m * n):
                    g[k // n][k % n] = (code >> k) & 1
                grids += 1
                total += matrix_score(g)
    print(f"all {grids} grids up to 3 by 3: scores sum to {total}")
    seed = 861
    total = 0
    check = 0
    for _ in range(2000):
        m = 1 + next_random() % 20
        n = 1 + next_random() % 20
        g = zeros(m, n)
        for i in range(m):
            for j in range(n):
                g[i][j] = next_random() % 2
        s = matrix_score(g)
        total += s
        check = (check * 31 + s) % 1000000007
    print(f"2000 random grids up to 20 by 20: scores sum to {total}, checksum {check}")


main()
