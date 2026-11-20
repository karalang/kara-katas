# LeetCode #1260 bench, in Python: the ★ arm (each value at flat place p
# written to (p + k) % (m * n) of a new grid) on 200 random grids of 50 by
# 50 built once, each shifted by a random 0 to 100, 150 rounds; a corner and
# the middle of each result folded into a checksum.


def shift_grid(grid, k):
    m, n = len(grid), len(grid[0])
    total = m * n
    shifted = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            to = (i * n + j + k) % total
            shifted[to // n][to % n] = grid[i][j]
    return shifted


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    rng = Rng(1260)
    grids = []
    shifts = []
    for _ in range(200):
        grids.append([[rng.next() % 2001 - 1000 for _ in range(50)] for _ in range(50)])
        shifts.append(rng.next() % 101)
    check = 0
    for _ in range(150):
        for g in range(200):
            shifted = shift_grid(grids[g], shifts[g])
            check = (check * 131 + shifted[0][0] + 1000) % 1000000007
            check = (check * 131 + shifted[25][25] + 1000) % 1000000007
    print(f"150 rounds of 200 grids of 50 by 50: checksum {check}")


main()
