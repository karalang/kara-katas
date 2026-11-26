# LeetCode #1463 bench in Python: the ★ arm (the most cherries over each
# pair of robot columns, row by row) on the same 40 grids of 70 by 70.


def cherry_pickup(grid):
    rows = len(grid)
    cols = len(grid[0])
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


seed = 1463


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    grids = [[[next_random() % 101 for _ in range(70)] for _ in range(70)] for _ in range(40)]
    check = 0
    for g in range(40):
        cell = check % 4900
        grids[g][cell // 70][cell % 70] = check % 101
        most = cherry_pickup(grids[g])
        check = (check * 31 + most) % 1000000007
    print(f"40 grids of 70 by 70: checksum {check}")


main()
