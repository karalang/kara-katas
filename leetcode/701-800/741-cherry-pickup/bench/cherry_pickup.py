# LeetCode #741: Cherry Pickup -- two walkers, one layer at a time.
# Benchmark mirror of the Kara star arm: two walkers go from the near
# corner to the far one together, a cherry on a shared cell counted
# once; keep the best cherries for every pair of rows after k steps
# and build the next layer from it.


def cherry_pickup(grid):
    n = len(grid)
    none = -1
    best = []
    for _ in range(n):
        best.append([none] * n)
    if grid[0][0] == -1:
        return 0
    best[0][0] = grid[0][0]
    for k in range(1, 2 * n - 1):
        nxt = []
        for _ in range(n):
            nxt.append([none] * n)
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


def main():
    seed = 741
    n = 50

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    grid = []
    for r in range(n):
        row = []
        for c in range(n):
            corner = (r == 0 and c == 0) or (r == n - 1 and c == n - 1)
            if not corner and next_random() % 10 == 0:
                row.append(-1)
            else:
                row.append(next_random() % 2)
        grid.append(row)
    total = 0
    for _ in range(300):
        for _ in range(5):
            r = next_random() % n
            c = next_random() % n
            v = next_random() % 10
            corner = (r == 0 and c == 0) or (r == n - 1 and c == n - 1)
            if not corner:
                grid[r][c] = -1 if v == 0 else v % 2
        total += cherry_pickup(grid)
    print(f"300 rounds of a 50 by 50 grid: {total} cherries in all")


main()
