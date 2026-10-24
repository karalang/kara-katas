# Benchmark: LeetCode #980 Unique Paths III -- the ★ arm, backtracking
# on the grid, on every start and end of an open 4 x 5 grid, LeetCode's
# largest. Mirrors unique_paths_iii.kara, .rs, .c and go-seq/.


def walk(grid, r, c, left):
    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or grid[r][c] == -1:
        return 0
    if grid[r][c] == 2:
        return 1 if left == 0 else 0
    grid[r][c] = -1
    paths = (walk(grid, r + 1, c, left - 1) + walk(grid, r - 1, c, left - 1)
             + walk(grid, r, c + 1, left - 1) + walk(grid, r, c - 1, left - 1))
    grid[r][c] = 0
    return paths


def unique_paths_iii(grid):
    g = [row[:] for row in grid]
    start = (0, 0)
    left = 0
    for r in range(len(g)):
        for c in range(len(g[0])):
            if g[r][c] == 1:
                start = (r, c)
            elif g[r][c] != -1:
                left += 1
    r, c = start
    g[r][c] = 0
    return walk(g, r, c, left)


def main():
    rounds, rows, cols = 20, 4, 5
    total = check = 0
    for _ in range(rounds):
        for s in range(rows * cols):
            for e in range(rows * cols):
                if s != e:
                    grid = [[0] * cols for _ in range(rows)]
                    grid[s // cols][s % cols] = 1
                    grid[e // cols][e % cols] = 2
                    p = unique_paths_iii(grid)
                    total += p
                    check = (check * 31 + p + s) % 1000000007
    print(f"{rounds} rounds over 380 starts and ends of a 4 x 5 grid: {total} paths, checksum {check}")


main()
