# LeetCode 750 — Number Of Corner Rectangles, pairs of rows.
# Mirror of count_corner_rectangles.kara (the ★ arm); same output, byte for byte.


def count_corner_rectangles(grid):
    m, n = len(grid), len(grid[0])
    total = 0
    for a in range(m):
        for b in range(a + 1, m):
            k = sum(1 for c in range(n) if grid[a][c] == 1 and grid[b][c] == 1)
            total += k * (k - 1) // 2
    return total


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(text):
    grid = [[1 if c == '1' else 0 for c in row] for row in text.split('/')]
    print(f"{text} -> {count_corner_rectangles(grid)}")


def random_grid(rng, m, n, percent):
    return [[1 if rng.next() % 100 < percent else 0 for _ in range(n)] for _ in range(m)]


def main():
    for t in ["10010/00101/00010/10101", "111/111/111", "1111", "1/1/1", "0",
              "11/11", "101/010/101", "1100/1100/0011/0011"]:
        show(t)
    ones = [[1] * 50 for _ in range(50)]
    print(f"50 x 50 of ones: {count_corner_rectangles(ones)}")
    rng = Rng(750)
    for m, n, percent in [(200, 200, 5), (100, 100, 50), (30, 200, 70), (200, 30, 70)]:
        grid = random_grid(rng, m, n, percent)
        print(f"{m} x {n}, {percent}% ones: {count_corner_rectangles(grid)}")
    total = 0
    check = 0
    for _ in range(300):
        m = 1 + rng.next() % 8
        n = 1 + rng.next() % 8
        percent = 20 + rng.next() % 70
        grid = random_grid(rng, m, n, percent)
        k = count_corner_rectangles(grid)
        total += k
        check = (check * 31 + k) % 1000000007
    print(f"300 random grids: {total} rectangles in all, checksum {check}")


main()
