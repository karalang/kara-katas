# LeetCode #1034: Coloring A Border -- Python mirror of color_border.kara
import sys

sys.setrecursionlimit(10000)


def visit(grid, r, c, color, seen, out):
    seen[r][c] = True
    m = len(grid)
    n = len(grid[0])
    border = False
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if nr < 0 or nr >= m or nc < 0 or nc >= n or grid[nr][nc] != grid[r][c]:
            border = True
        elif not seen[nr][nc]:
            visit(grid, nr, nc, color, seen, out)
    if border:
        out[r][c] = color


def color_border(grid, row, col, color):
    seen = [[False] * len(grid[0]) for _ in grid]
    out = [list(r) for r in grid]
    visit(grid, row, col, color, seen, out)
    return out


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(grid):
    return "[" + ",".join("[" + ",".join(str(v) for v in row) + "]" for row in grid) + "]"


def fold(grid, check):
    h = check
    for row in grid:
        for v in row:
            h = (h * 131 + v) % 1000000007
    return h


def random_grid(m, n, top, seed):
    return [[next_random(seed) % top + 1 for _ in range(n)] for _ in range(m)]


def main():
    examples = [
        ([[1, 1], [1, 2]], 0, 0, 3),
        ([[1, 2, 2], [2, 3, 2]], 0, 1, 3),
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1, 1, 2),
        ([[7]], 0, 0, 9),
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1, 1, 1),
        ([[1, 2, 1], [1, 1, 1], [2, 1, 2]], 1, 1, 2),
        ([[1, 1, 1, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 1, 1, 1]], 0, 0, 2),
        ([[5, 5, 5, 5, 5], [5, 4, 4, 4, 5], [5, 4, 5, 4, 5], [5, 4, 4, 4, 5], [5, 5, 5, 5, 5]], 2, 2, 6),
    ]
    for grid, row, col, color in examples:
        painted = color_border(grid, row, col, color)
        print(f"{show(grid)}, {row}, {col}, {color} -> {show(painted)}")
    seed = [1034]
    small = random_grid(6, 6, 2, seed)
    print(f"{show(small)}, 2, 3, 3 -> {show(color_border(small, 2, 3, 3))}")
    for top in [1, 2, 3, 1000]:
        check = 0
        painted_cells = 0
        for _ in range(60):
            m = next_random(seed) % 30 + 1
            n = next_random(seed) % 30 + 1
            grid = random_grid(m, n, top, seed)
            row = next_random(seed) % m
            col = next_random(seed) % n
            color = next_random(seed) % (top + 1) + 1
            painted = color_border(grid, row, col, color)
            for i in range(m):
                for j in range(n):
                    if painted[i][j] != grid[i][j]:
                        painted_cells += 1
            check = fold(painted, check)
        print(f"60 random grids up to 30 by 30, values from 1 to {top}: {painted_cells} cells changed, checksum {check}")
    full = [[4] * 50 for _ in range(50)]
    rings = []
    path = []
    for i in range(50):
        ring_row = []
        path_row = []
        for j in range(50):
            ring_row.append(min(i, j, 49 - i, 49 - j) % 2 + 1)
            open_ = i % 2 == 0 or (i % 4 == 1 and j == 49) or (i % 4 == 3 and j == 0)
            path_row.append(1 if open_ else 2)
        rings.append(ring_row)
        path.append(path_row)
    for name, grid, row, col in [("one colour", full, 25, 25), ("rings", rings, 0, 0), ("rings", rings, 24, 24), ("winding path", path, 0, 0)]:
        painted = color_border(grid, row, col, 3)
        changed = sum(1 for i in range(50) for j in range(50) if painted[i][j] != grid[i][j])
        print(f"50 by 50, {name}, from ({row}, {col}): {changed} cells changed, checksum {fold(painted, 0)}")


main()
