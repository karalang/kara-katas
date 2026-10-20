# LeetCode 807 — Max Increase to Keep City Skyline: the bench.
#
# 64 grids of 50 by 50, LeetCode's largest, with heights from 0 to 100,
# are made once; each round finds how much the next one can grow.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def max_increase_keeping_skyline(grid):
    n = len(grid)
    row_max = [0] * n
    col_max = [0] * n
    for i in range(n):
        for j in range(n):
            row_max[i] = max(row_max[i], grid[i][j])
            col_max[j] = max(col_max[j], grid[i][j])
    total = 0
    for i in range(n):
        for j in range(n):
            total += min(row_max[i], col_max[j]) - grid[i][j]
    return total


def main():
    seed = [807]
    grids = []
    for _ in range(64):
        grid = []
        for _ in range(50):
            grid.append([next_random(seed) % 101 for _ in range(50)])
        grids.append(grid)
    rounds = 300000
    total = 0
    check = 0
    for r in range(rounds):
        added = max_increase_keeping_skyline(grids[r % 64])
        total += added
        check = (check * 131 + added) % 1000000007
    print(f"{rounds} rounds of 50 x 50: {total} floors in all, checksum {check}")


main()
