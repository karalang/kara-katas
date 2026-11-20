# LeetCode #2352: Equal Row and Column Pairs -- the bench, the ★ arm in
# Python: the rows counted in a dict keyed by the row as a tuple, then each
# column built and looked up there.


def equal_pairs(grid):
    n = len(grid)
    rows = {}
    for row in grid:
        key = tuple(row)
        rows[key] = rows.get(key, 0) + 1
    total = 0
    for j in range(n):
        column = tuple(grid[i][j] for i in range(n))
        total += rows.get(column, 0)
    return total


SEED = [2352]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # grid g is 200 x 200, cell (i, j) being (a i j + b) mod m, so that
    # rows repeat and match columns, with a in 1 to 5 and m in 2 to 10
    grids = []
    for _ in range(10):
        a = 1 + next_random() % 5
        b = next_random() % 10
        m = 2 + next_random() % 9
        grids.append([[(a * i * j + b) % m for j in range(200)] for i in range(200)])
    check = 0
    for p in range(40):
        for grid in grids:
            check = (check * 31 + equal_pairs(grid) + p) % 1000000007
    print(f"40 passes over 10 grids of 200 x 200: checksum {check}")


main()
