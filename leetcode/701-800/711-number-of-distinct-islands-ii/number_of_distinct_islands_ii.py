# LeetCode #711: Number of Distinct Islands II -- a canonical form
# under the eight symmetries.
#
# A mirror of number_of_distinct_islands_ii.kara (the ★ arm) and its
# harness.

import sys

sys.setrecursionlimit(10000)

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def collect(grid, seen, r, c, cells):
    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
        return
    if grid[r][c] == 0 or seen[r][c]:
        return
    seen[r][c] = True
    cells.append((r, c))
    collect(grid, seen, r + 1, c, cells)
    collect(grid, seen, r - 1, c, cells)
    collect(grid, seen, r, c + 1, cells)
    collect(grid, seen, r, c - 1, cells)


def canonical(cells):
    best = None
    for k in range(8):
        moved = []
        for r, c in cells:
            a, b = (r, c) if k < 4 else (c, r)
            x = -a if k % 2 == 1 else a
            y = -b if k % 4 >= 2 else b
            moved.append((x, y))
        moved.sort()
        r0, c0 = moved[0]
        flat = []
        for r, c in moved:
            flat.append(r - r0)
            flat.append(c - c0)
        if k == 0 or flat < best:
            best = flat
    return tuple(best)


def num_distinct_islands2(grid):
    seen = [[False] * len(row) for row in grid]
    shapes = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 1 and not seen[r][c]:
                cells = []
                collect(grid, seen, r, c, cells)
                shapes.add(canonical(cells))
    return len(shapes)


def grid_of(rows):
    return [[1 if ch == "1" else 0 for ch in row] for row in rows]


def random_grid(rows, cols, pct):
    return [[1 if next_random() % 100 < pct else 0 for _ in range(cols)]
            for _ in range(rows)]


def show(name, rows):
    print(f"{name}: {num_distinct_islands2(grid_of(rows))}")


def main():
    global seed
    show("example 1", ["11000", "10000", "00001", "00011"])
    show("example 2", ["11000", "11000", "00011", "00011"])
    show("one cell", ["1"])
    show("all water", ["000", "000"])
    show("all land", ["111", "111"])
    show("L turned four ways", ["1100011", "1000001", "0000000",
                                "1000001", "1100011"])
    show("L and its mirror", ["110011", "100001"])
    show("S and Z", ["0110011000", "1100001100"])
    show("bar across and down", ["11101", "00001", "00001"])
    show("plus and another pentomino", ["0100100", "1110111", "0100010"])
    show("checkerboard", ["10101", "01010", "10101", "01010"])
    seed = 711
    big = random_grid(50, 50, 45)
    print(f"50 by 50, 45% land: {num_distinct_islands2(big)}")
    dense = random_grid(50, 50, 60)
    print(f"50 by 50, 60% land: {num_distinct_islands2(dense)}")
    total_sum = 0
    total = 0
    for _ in range(300):
        rows = 1 + next_random() % 12
        cols = 1 + next_random() % 12
        pct = 20 + next_random() % 50
        n = num_distinct_islands2(random_grid(rows, cols, pct))
        total += n
        total_sum = (total_sum * 131 + n) % 1000000007
    print(f"300 random grids: {total} distinct islands, checksum {total_sum}")


main()
