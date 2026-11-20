# LeetCode #1219 bench, Python mirror of the Kāra ★ arm: a depth-first
# search from every cell with gold that zeroes a cell while the search goes
# on from it and puts its gold back on the way out, on 160 grids of 15 by
# 15, each holding one blob of 25 cells with gold, drawn once.

seed = 1219


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


STEPS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def collect(grid, r, c):
    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or grid[r][c] == 0:
        return 0
    gold = grid[r][c]
    grid[r][c] = 0
    best = 0
    for dr, dc in STEPS:
        best = max(best, collect(grid, r + dr, c + dc))
    grid[r][c] = gold
    return gold + best


def get_maximum_gold(grid):
    g = [row[:] for row in grid]
    best = 0
    for r in range(len(g)):
        for c in range(len(g[0])):
            if g[r][c] > 0:
                best = max(best, collect(g, r, c))
    return best


def main():
    grids = []
    for _ in range(160):
        grid = [[0] * 15 for _ in range(15)]
        r0 = next_random() % 15
        c0 = next_random() % 15
        grid[r0][c0] = next_random() % 100 + 1
        cells = [(r0, c0)]
        while len(cells) < 25:
            at = next_random() % len(cells)
            dr, dc = STEPS[next_random() % 4]
            r, c = cells[at][0] + dr, cells[at][1] + dc
            if 0 <= r < 15 and 0 <= c < 15 and grid[r][c] == 0:
                grid[r][c] = next_random() % 100 + 1
                cells.append((r, c))
        grids.append(grid)
    check = 0
    total = 0
    for grid in grids:
        answer = get_maximum_gold(grid)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"160 grids of 15 by 15, one blob of 25 cells with gold each: gold total {total}, checksum {check}")


main()
