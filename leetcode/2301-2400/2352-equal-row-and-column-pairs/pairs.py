# LeetCode #2352: Equal Row and Column Pairs -- the Python mirror of the ★
# arm: the rows counted in a map keyed by the row, then each column looked
# up in it.


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
    # LeetCode's two examples; then one cell, 200 x 200 ones, the identity,
    # and (i j) mod 7, whose row i is its column i and the row of every i'
    # with i' = i mod 7
    print(equal_pairs([[3, 2, 1], [1, 7, 6], [2, 7, 7]]))
    print(equal_pairs([[3, 1, 2, 2], [1, 4, 4, 5], [2, 4, 2, 2], [2, 4, 2, 2]]))
    print(equal_pairs([[5]]))
    print(equal_pairs([[1] * 200 for _ in range(200)]))
    print(equal_pairs([[1 if i == j else 0 for j in range(200)] for i in range(200)]))
    print(equal_pairs([[i * j % 7 for j in range(200)] for i in range(200)]))
    # 1000 random grids of 1 to 6 rows of values from 1 to 1 up to 1 to 3,
    # and 1 to 10^5 in every tenth
    check = 0
    total = 0
    none = 0
    for g in range(1000):
        n = 1 + next_random() % 6
        top = 100000 if g % 10 == 9 else 1 + next_random() % 3
        grid = [[1 + next_random() % top for _ in range(n)] for _ in range(n)]
        p = equal_pairs(grid)
        check = (check * 31 + p) % 1000000007
        total += p
        if p == 0:
            none += 1
    print(f"1000 grids: checksum {check}, pairs {total}, {none} with none")


main()
