# LeetCode #2428: Maximum Sum of an Hourglass -- the bench, the ★ arm:
# every centre off the border, its seven cells added directly.

seed = 2428


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def max_sum(grid):
    m = len(grid)
    n = len(grid[0])
    best = 0
    for r in range(1, m - 1):
        for c in range(1, n - 1):
            total = (grid[r - 1][c - 1] + grid[r - 1][c] + grid[r - 1][c + 1]
                     + grid[r][c]
                     + grid[r + 1][c - 1] + grid[r + 1][c] + grid[r + 1][c + 1])
            best = max(best, total)
    return best


def main():
    grids = []
    for _ in range(10):
        grid = []
        for _ in range(150):
            row = []
            for _ in range(150):
                a = next_random()
                row.append((a * 32768 + next_random()) % 1000001)
            grid.append(row)
        grids.append(grid)
    check = 0
    for p in range(600):
        for g in range(10):
            grids[g][(p * 37) % 150][(p * 91) % 150] = (p * 7919) % 1000001
            check = (check * 31 + max_sum(grids[g]) + p) % 1000000007
    print(f"600 passes over 10 grids of 150 by 150: checksum {check}")


main()
