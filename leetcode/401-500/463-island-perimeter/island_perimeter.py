# LeetCode #463: Island Perimeter -- mirror of island_perimeter.kara (the
# star arm: four sides per land cell, less two per shared edge).


def island_perimeter(grid):
    land = 0
    shared = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                land += 1
                if j + 1 < len(grid[i]) and grid[i][j + 1] == 1:
                    shared += 1
                if i + 1 < len(grid) and grid[i + 1][j] == 1:
                    shared += 1
    return 4 * land - 2 * shared


# ---- test harness ---------------------------------------------------------


def drawn(grid):
    return "/".join("".join(str(cell) for cell in row) for row in grid)


def show(grid):
    print(f"{drawn(grid)} -> {island_perimeter(grid)}")


seed = 463


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_island(rows, cols, steps):
    grid = [[0] * cols for _ in range(rows)]
    i = next_random() % rows
    j = next_random() % cols
    grid[i][j] = 1
    for _ in range(steps):
        d = next_random() % 4
        if d == 0 and i > 0:
            i -= 1
        elif d == 1 and i + 1 < rows:
            i += 1
        elif d == 2 and j > 0:
            j -= 1
        elif d == 3 and j + 1 < cols:
            j += 1
        grid[i][j] = 1
    sea = [[False] * cols for _ in range(rows)]
    queue = []
    for r in range(rows):
        for c in range(cols):
            if (r == 0 or c == 0 or r == rows - 1 or c == cols - 1) and grid[r][c] == 0:
                sea[r][c] = True
                queue.append((r, c))
    head = 0
    while head < len(queue):
        r, c = queue[head]
        head += 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and not sea[nr][nc]:
                sea[nr][nc] = True
                queue.append((nr, nc))
    for r in range(rows):
        for c in range(cols):
            if not sea[r][c]:
                grid[r][c] = 1
    return grid


def main():
    show([[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]])
    show([[1]])
    show([[1, 0]])
    show([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    show([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    show([[1, 1, 1, 1, 1]])
    show([[1], [1], [1]])
    show([[1, 0, 1], [1, 0, 1], [1, 1, 1]])
    show([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    show([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]])
    count = 300
    total = 0
    land = 0
    checksum = 0
    for _ in range(count):
        rows = 1 + next_random() % 40
        cols = 1 + next_random() % 40
        steps = next_random() % (rows * cols + 1)
        grid = random_island(rows, cols, steps)
        for row in grid:
            land += sum(row)
        perimeter = island_perimeter(grid)
        total += perimeter
        checksum = (checksum * 31 + perimeter) % 1000000007
    print(f"{count} random islands: {land} land cells, perimeter {total} in all, checksum {checksum}")


main()
