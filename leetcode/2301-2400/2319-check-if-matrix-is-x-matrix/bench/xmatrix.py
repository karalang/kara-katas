# LeetCode #2319: Check if Matrix Is X-Matrix -- the bench, the ★ arm in
# Python. One walk over the cells, a cell on either diagonal nonzero and
# any other zero, the first cell that breaks its rule ending the walk.
# O(n^2).


def check_x_matrix(grid):
    n = len(grid)
    for i in range(n):
        row = grid[i]
        for j in range(n):
            on = i == j or i + j == n - 1
            if on != (row[j] != 0):
                return False
    return True


seed = 2319


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100
    grids = []
    for _ in range(200):
        g = []
        for i in range(n):
            row = []
            for j in range(n):
                value = next_random() % 100000 + 1
                row.append(value if i == j or i + j == n - 1 else 0)
            g.append(row)
        grids.append(g)
    check = 0
    for p in range(400):
        for g in range(200):
            punch = next_random() % 2 == 0
            i = next_random() % n
            j = next_random() % n
            old = grids[g][i][j]
            if punch:
                grids[g][i][j] = p + 1 if old == 0 else 0
            is_x = check_x_matrix(grids[g])
            grids[g][i][j] = old
            check = (check * 31 + (2 if is_x else 1) + p) % 1000000007
    print(f"400 passes over 200 grids of 100 by 100: checksum {check}")


main()
