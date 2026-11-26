# LeetCode #1463 Cherry Pickup II: a mirror of cherry_pickup.kara.


def cherry_pickup(grid):
    rows = len(grid)
    cols = len(grid[0])
    # best[a][b]: the most cherries picked down to this row with robot 1 at
    # column a and robot 2 at column b, -1 where they cannot both be
    best = [[-1] * cols for _ in range(cols)]
    best[0][cols - 1] = grid[0][0] + grid[0][cols - 1]
    for r in range(1, rows):
        nxt = [[-1] * cols for _ in range(cols)]
        for a in range(cols):
            for b in range(cols):
                if best[a][b] < 0:
                    continue
                for da in (-1, 0, 1):
                    for db in (-1, 0, 1):
                        x, y = a + da, b + db
                        if x < 0 or x >= cols or y < 0 or y >= cols:
                            continue
                        here = grid[r][x] if x == y else grid[r][x] + grid[r][y]
                        nxt[x][y] = max(nxt[x][y], best[a][b] + here)
        best = nxt
    return max(max(row) for row in best)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(rows, cols, top):
    return [[next_random() % (top + 1) for _ in range(cols)] for _ in range(rows)]


def main():
    global seed
    f = cherry_pickup
    e1 = [[3, 1, 1], [2, 5, 1], [1, 5, 5], [2, 1, 1]]
    e2 = [[1, 0, 0, 0, 0, 0, 1], [2, 0, 0, 0, 0, 3, 0], [2, 0, 9, 0, 0, 0, 0], [0, 3, 0, 5, 4, 0, 0], [1, 0, 2, 3, 0, 0, 6]]
    e3 = [[1, 2], [3, 4]]
    e4 = [[5, 5], [5, 5], [5, 5]]
    full = [[100] * 70 for _ in range(70)]
    empty = [[0] * 70 for _ in range(70)]
    print(f"{f(e1)} {f(e2)} {f(e3)} {f(e4)} {f(full)} {f(empty)}")
    seed = 1463
    print(f"70 by 70: {f(draw(70, 70, 100))}")
    total = 0
    check = 0
    for _ in range(1000):
        rows = 2 + next_random() % 11
        cols = 2 + next_random() % 11
        top = next_random() % 101
        got = f(draw(rows, cols, top))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"1000 random grids: {total} cherries, checksum {check}")


main()
