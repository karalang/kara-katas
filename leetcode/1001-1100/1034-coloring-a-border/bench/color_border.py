# LeetCode #1034: Coloring A Border -- bench
# Mirrors ./color_border.kara; see ../README.md § Benchmarks.
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
    out = [list(line) for line in grid]
    visit(grid, row, col, color, seen, out)
    return out


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count, starts, rounds = 100, 10, 20
    seed = [1034]
    grids = []
    asks = []
    for g in range(count):
        grids.append([[2 if next_random(seed) % 3 == 0 else 1 for _ in range(50)] for _ in range(50)])
        for _ in range(starts):
            row = next_random(seed) % 50
            col = next_random(seed) % 50
            color = next_random(seed) % 3 + 1
            asks.append((g, row, col, color))
    changed = 0
    check = 0
    for _ in range(rounds):
        for g, row, col, color in asks:
            grid = grids[g]
            painted = color_border(grid, row, col, color)
            for r in range(50):
                for c in range(50):
                    if painted[r][c] != grid[r][c]:
                        changed += 1
                        check = (check * 131 + r * 50 + c) % 1000000007
    print(f"{count} grids of 50 by 50, {starts} starts each, {rounds} rounds: {changed} squares changed, checksum {check}")


main()
