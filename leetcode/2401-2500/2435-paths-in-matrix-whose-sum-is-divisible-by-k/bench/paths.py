# LeetCode #2435: Paths in Matrix Whose Sum Is Divisible by K -- the
# bench, the ★ arm: one row of counts by remainder, each cell's from
# above, still in place, and from the left, shifted by its value.

MOD = 1000000007


def number_of_paths(grid, k):
    n = len(grid[0])
    row = [[0] * k for _ in range(n)]
    for i in range(len(grid)):
        for j in range(n):
            came = [0] * k
            if i == 0 and j == 0:
                came[0] = 1
            for r in range(k):
                left = row[j - 1][r] if j > 0 else 0
                came[r] = (came[r] + row[j][r] + left) % MOD
            v = grid[i][j]
            for r in range(k):
                row[j][(r + v) % k] = came[r]
    return row[n - 1][0]


seed = 2435


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    grids = [[[next_random() % 101 for _ in range(250)] for _ in range(200)] for _ in range(5)]
    check = 0
    for p in range(10):
        for g in range(len(grids)):
            grids[g][(p * 37) % 200][(p * 91) % 250] = p
            check = (check * 31 + number_of_paths(grids[g], 50) + p) % 1000000007
    print(f"10 passes over 5 grids of 200 by 250: checksum {check}")


main()
