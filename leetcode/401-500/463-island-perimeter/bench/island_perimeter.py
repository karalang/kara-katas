# Benchmark for #463: mirror of island_perimeter.kara (the star arm: four
# sides per land cell, less two per shared edge) on the same workload.


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
    size = 1000
    islands = 2
    rounds = 200
    grids = []
    tops = []
    shores = []
    for _ in range(islands):
        inner = random_island(size - 2, size - 2, (size - 2) * (size - 2))
        grid = [[0] * size] + [[0] + row + [0] for row in inner] + [[0] * size]
        top = 0
        while 1 not in grid[top]:
            top += 1
        shores.append([j for j in range(size) if grid[top][j] == 1])
        grids.append(grid)
        tops.append(top)
    total = 0
    checksum = 0
    for _ in range(rounds):
        for g in range(islands):
            j = shores[g][next_random() % len(shores[g])]
            above = tops[g] - 1
            grids[g][above][j] = 1
            perimeter = island_perimeter(grids[g])
            grids[g][above][j] = 0
            total += perimeter
            checksum = (checksum * 31 + perimeter) % 1000000007
    print(f"{rounds} rounds on {islands} islands of {size}x{size}: perimeter {total} in all, checksum {checksum}")


main()
