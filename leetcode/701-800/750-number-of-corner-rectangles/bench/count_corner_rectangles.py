# LeetCode 750 — Number Of Corner Rectangles, bench: the ★ arm (pairs
# of rows) on a 200 x 200 grid that keeps changing.
# Mirrors count_corner_rectangles.kara.


def count_corner_rectangles(grid):
    m, n = len(grid), len(grid[0])
    total = 0
    for a in range(m):
        ra = grid[a]
        for b in range(a + 1, m):
            rb = grid[b]
            k = 0
            for c in range(n):
                if ra[c] == 1 and rb[c] == 1:
                    k += 1
            total += k * (k - 1) // 2
    return total


seed = 750


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 100
    grid = [[next_random() % 2 for _ in range(200)] for _ in range(200)]
    total = 0
    check = 0
    for _ in range(rounds):
        for _ in range(50):
            r = next_random() % 200
            c = next_random() % 200
            grid[r][c] = next_random() % 2
        k = count_corner_rectangles(grid)
        total += k
        check = (check * 31 + k) % 1000000007
    print(f"{rounds} grids of 200 x 200: {total} rectangles in all, checksum {check}")


main()
