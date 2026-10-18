# LeetCode #741: Cherry Pickup -- two walkers, one layer at a time.
# Mirror of the Kara star arm: two walkers go from the near corner to
# the far one together, a cherry on a shared cell counted once; keep
# the best cherries for every pair of rows after k steps and build the
# next layer from it.


def cherry_pickup(grid):
    n = len(grid)
    none = -1
    best = [[none] * n for _ in range(n)]
    if grid[0][0] == -1:
        return 0
    best[0][0] = grid[0][0]
    for k in range(1, 2 * n - 1):
        nxt = [[none] * n for _ in range(n)]
        low = k - n + 1 if k >= n else 0
        high = k if k < n else n - 1
        for r1 in range(low, high + 1):
            for r2 in range(low, high + 1):
                c1 = k - r1
                c2 = k - r2
                if grid[r1][c1] == -1 or grid[r2][c2] == -1:
                    continue
                frm = none
                for d1 in range(2):
                    for d2 in range(2):
                        p1 = r1 - d1
                        p2 = r2 - d2
                        if p1 >= 0 and p2 >= 0 and best[p1][p2] > frm:
                            frm = best[p1][p2]
                if frm == none:
                    continue
                here = grid[r1][c1]
                if r2 != r1:
                    here += grid[r2][c2]
                nxt[r1][r2] = frm + here
        best = nxt
    return 0 if best[n - 1][n - 1] == none else best[n - 1][n - 1]


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def fmt(grid):
    return "[" + ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in grid) + "]"


def show(grid):
    print(f"{fmt(grid)} -> {cherry_pickup(grid)}")


def random_grid(seed, n, thorns):
    grid = []
    for r in range(n):
        row = []
        for c in range(n):
            corner = (r == 0 and c == 0) or (r == n - 1 and c == n - 1)
            if not corner and next_random(seed) % thorns == 0:
                row.append(-1)
            else:
                row.append(next_random(seed) % 2)
        grid.append(row)
    return grid


def main():
    show([[0, 1, -1], [1, 0, -1], [1, 1, 1]])
    show([[1, 1, -1], [1, -1, 1], [-1, 1, 1]])
    show([[1]])
    show([[0]])
    show([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    show([[1, 1, 1, 1], [-1, -1, -1, 1], [1, 1, 1, 1], [1, -1, -1, 1]])
    show([[0, 1, 1, 0], [1, -1, 1, 1], [1, 1, -1, 1], [0, 1, 1, 1]])
    show([[1, -1], [-1, 1]])
    seed = [741]
    big = random_grid(seed, 50, 10)
    print(f"50 by 50, a thorn in about one cell in 10 -> {cherry_pickup(big)}")
    full = [[1] * 50 for _ in range(50)]
    print(f"50 by 50, a cherry in every cell -> {cherry_pickup(full)}")
    total = 0
    most = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 6
        thorns = 2 + next_random(seed) % 4
        grid = random_grid(seed, n, thorns)
        got = cherry_pickup(grid)
        most += got
        total = (total * 131 + got + 1) % 1000000007
    print(f"300 random grids up to 6 by 6: {most} cherries in all, checksum {total}")


main()
