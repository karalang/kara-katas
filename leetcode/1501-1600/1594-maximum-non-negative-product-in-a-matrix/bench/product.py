# LeetCode #1594: Maximum Non Negative Product in a Matrix
# -- the bench in Python, mirroring product.kara: the largest and the
# smallest product of a path reaching each cell, on 40000 grids of 15 by
# 15 cells from -4 to 4, all drawn first.


def max_product_path(grid):
    rows, cols = len(grid), len(grid[0])
    hi = [[0] * cols for _ in range(rows)]
    lo = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            v = grid[r][c]
            if r == 0 and c == 0:
                hi[r][c] = lo[r][c] = v
                continue
            best = -(1 << 63)
            worst = (1 << 63) - 1
            if r > 0:
                best = max(best, hi[r - 1][c] * v, lo[r - 1][c] * v)
                worst = min(worst, hi[r - 1][c] * v, lo[r - 1][c] * v)
            if c > 0:
                best = max(best, hi[r][c - 1] * v, lo[r][c - 1] * v)
                worst = min(worst, hi[r][c - 1] * v, lo[r][c - 1] * v)
            hi[r][c], lo[r][c] = best, worst
    top = hi[rows - 1][cols - 1]
    return -1 if top < 0 else top % 1000000007


def main():
    seed = 1594

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    grids = [[[next_random() % 9 - 4 for _ in range(15)] for _ in range(15)] for _ in range(40000)]
    check = 0
    negative = 0
    for grid in grids:
        answer = max_product_path(grid)
        if answer == -1:
            negative += 1
        check = (check * 31 + answer + 1) % 1000000007
    print(f"40000 grids of 15 by 15: {negative} only negative, checksum {check}")


main()
