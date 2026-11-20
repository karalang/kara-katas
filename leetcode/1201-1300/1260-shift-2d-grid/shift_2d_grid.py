# LeetCode #1260: Shift 2D Grid -- Python mirror of the ★ arm (each value at
# flat place p written to (p + k) % (m * n) of a new grid), with the same
# harness.


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


def random_grid(m, n, rng):
    return [[rng.next() % 2001 - 1000 for _ in range(n)] for _ in range(m)]


def fold(check, grid):
    for row in grid:
        for x in row:
            check = (check * 131 + x + 1000) % 1000000007
        check = (check * 131 + 7) % 1000000007
    return check


def show(grid):
    return "[" + ", ".join("[" + ", ".join(map(str, r)) + "]" for r in grid) + "]"


def main():
    g = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(show(shift_grid(g, 1)))
    print(show(shift_grid([[3, 8, 1, 9], [19, 7, 2, 5], [4, 6, 11, 10], [12, 0, 21, 13]], 4)))
    print(show(shift_grid(g, 9)))
    rng = Rng(1260)
    check = 0
    corner = 0
    for _ in range(1000):
        m = rng.next() % 50 + 1
        n = rng.next() % 50 + 1
        k = rng.next() % 101
        grid = random_grid(m, n, rng)
        shifted = shift_grid(grid, k)
        corner += shifted[0][0]
        check = fold(check, shifted)
    print(f"1000 random grids: corners {corner}, checksum {check}")
    big = random_grid(50, 50, rng)
    a = shift_grid(big, 100)
    column = shift_grid(random_grid(50, 1, rng), 99)
    row = shift_grid(random_grid(1, 50, rng), 99)
    print(f"50 by 50: {a[0][0]} {a[49][49]} {fold(0, a)}; column {column[0][0]} {fold(0, column)}; row {row[0][49]} {fold(0, row)}")


main()
