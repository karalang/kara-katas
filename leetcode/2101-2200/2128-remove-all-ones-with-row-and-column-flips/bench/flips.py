# LeetCode #2128: Remove All Ones With Row and Column Flips -- the
# benchmark, the same algorithm as flips.kara.


def remove_ones(grid):
    first = grid[0]
    for row in grid:
        for j in range(len(row)):
            if row[j] ^ row[0] != first[j] ^ first[0]:
                return False
    return True


seed = 2128


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 300
    grids = []
    for _ in range(20):
        columns = [next_random() % 2 for _ in range(n)]
        grid = []
        for _ in range(n):
            r = next_random() % 2
            grid.append([c ^ r for c in columns])
        grids.append(grid)
    cleared = 0
    check = 0
    for rnd in range(100):
        for k in range(20):
            r = next_random() % n
            grids[k][r] = [1 - c for c in grids[k][r]]
            broken = next_random() % 2 == 0
            i = next_random() % n
            j = next_random() % n
            if broken:
                grids[k][i][j] = 1 - grids[k][i][j]
            if remove_ones(grids[k]):
                cleared += 1
                check = (check * 31 + rnd * 20 + k) % 1000000007
            if broken:
                grids[k][i][j] = 1 - grids[k][i][j]
    print(f"2000 solves: {cleared} cleared, checksum {check}")


main()
