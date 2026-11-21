# LeetCode #2482: Difference Between Ones and Zeros in Row and Column --
# Python mirror of diff.kara: by the ones alone.


def ones_minus_zeros(grid):
    m = len(grid)
    n = len(grid[0])
    row_ones = [0] * m
    col_ones = [0] * n
    for i in range(m):
        for j in range(n):
            row_ones[i] += grid[i][j]
            col_ones[j] += grid[i][j]
    diff = []
    for i in range(m):
        row = []
        for j in range(n):
            row.append(2 * row_ones[i] + 2 * col_ones[j] - m - n)
        diff.append(row)
    return diff


seed = 2482


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(m, n):
    return [[next_random() % 2 for _ in range(n)] for _ in range(m)]


def fold(diff):
    check = len(diff)
    for row in diff:
        for v in row:
            check = (check * 31 + v + 1000000) % 1000000007
    return check


def show(grid):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]" for row in grid) + "]"


def main():
    grids = [
        [[0, 1, 1], [1, 0, 1], [0, 0, 1]],
        [[1, 1, 1], [1, 1, 1]],
        [[0]],
        [[1]],
        [[1, 0, 1, 1, 0]],
        [[1], [0], [0], [1]],
        [[0, 0], [0, 0]],
    ]
    for grid in grids:
        print(f"{show(grid)} -> {show(ones_minus_zeros(grid))}")
    for m, n in [(1, 100000), (100000, 1), (316, 316)]:
        grid = random_grid(m, n)
        print(f"{m} by {n} -> checksum {fold(ones_minus_zeros(grid))}")
    check = 0
    for _ in range(3000):
        m = 1 + next_random() % 8
        n = 1 + next_random() % 8
        check = (check * 31 + fold(ones_minus_zeros(random_grid(m, n)))) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
