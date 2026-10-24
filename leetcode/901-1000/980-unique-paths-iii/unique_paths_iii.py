# LeetCode #980: Unique Paths III -- mirror of the ★ arm
# (unique_paths_iii.kara), backtracking on the grid.


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


seed = 980


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(rows, cols):
    grid = []
    free = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if next_random() % 5 == 0:
                row.append(-1)
            else:
                row.append(0)
                free.append((r, c))
        grid.append(row)
    while len(free) < 2:
        r = next_random() % rows
        c = next_random() % cols
        if grid[r][c] == -1:
            grid[r][c] = 0
            free.append((r, c))
    a = next_random() % len(free)
    b = next_random() % (len(free) - 1)
    if b >= a:
        b += 1
    ar, ac = free[a]
    br, bc = free[b]
    grid[ar][ac] = 1
    grid[br][bc] = 2
    return grid


def open_grid(rows, cols, start, end):
    grid = [[0] * cols for _ in range(rows)]
    grid[start[0]][start[1]] = 1
    grid[end[0]][end[1]] = 2
    return grid


def main():
    cases = [
        [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]],
        [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]],
        [[0, 1], [2, 0]],
        [[1, 2]],
        [[1, -1, 2]],
        [[2, 0, 1]],
        [[1, 0], [0, 2]],
        [[1, 0, 0], [0, -1, 0], [0, 0, 2]],
        [[1, 0, 0], [0, 0, 0], [0, 0, 2]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 2]],
    ]
    for i, grid in enumerate(cases):
        print(f"case {i + 1}: {unique_paths_iii(grid)}")
    for count, area in [(300, 9), (3000, 16)]:
        total = check = 0
        for _ in range(count):
            rows = 1 + next_random() % area
            cols = 1 + next_random() % (area // rows)
            if rows * cols < 2:
                cols = 2
            p = unique_paths_iii(random_grid(rows, cols))
            total += p
            check = (check * 31 + p + 1) % 1000000007
        print(f"{count} random grids of up to {area} squares: {total} paths, checksum {check}")
    print(f"4 x 5, corner to corner: {unique_paths_iii(open_grid(4, 5, (0, 0), (3, 4)))}")
    print(f"4 x 5, corner to the corner below: {unique_paths_iii(open_grid(4, 5, (0, 0), (3, 0)))}")
    print(f"4 x 5, middle to corner: {unique_paths_iii(open_grid(4, 5, (1, 2), (0, 0)))}")
    print(f"2 x 10, corner to the far corner on its side: {unique_paths_iii(open_grid(2, 10, (0, 0), (0, 9)))}")
    print(f"1 x 20, end to end: {unique_paths_iii(open_grid(1, 20, (0, 0), (0, 19)))}")


main()
