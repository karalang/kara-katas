# LeetCode #2482: Difference Between Ones and Zeros in Row and Column --
# bench, Python mirror of diff.kara.


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


def main():
    grids = [[[next_random() % 2 for _ in range(100)] for _ in range(100)] for _ in range(20)]
    check = 0
    for p in range(180):
        for g in range(20):
            i, j = check % 100, check // 100 % 100
            grids[g][i][j] = 1 - grids[g][i][j]
            diff = ones_minus_zeros(grids[g])
            for row in diff:
                for v in row:
                    check = (check * 31 + v + 200 + p) % 1000000007
    print(f"180 passes over 20 grids of 100 by 100: checksum {check}")


main()
