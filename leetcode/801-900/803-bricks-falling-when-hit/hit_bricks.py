# LeetCode 803 -- Bricks Falling When Hit: mirrors the harness of
# hit_bricks.kara with the ★ arm's union-find run backwards.
seed = 803
DR = [-1, 1, 0, 0]
DC = [0, 0, -1, 1]


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def hit_bricks(grid, hits):
    rows, cols = len(grid), len(grid[0])
    left = [row[:] for row in grid]
    for r, c in hits:
        left[r][c] = 0
    roof = rows * cols
    parent = list(range(roof + 1))
    size = [1] * (roof + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            parent[ra] = rb
            size[rb] += size[ra]
        else:
            parent[rb] = ra
            size[ra] += size[rb]

    def join(r, c):
        here = r * cols + c
        if r == 0:
            union(here, roof)
        for d in range(4):
            nr, nc = r + DR[d], c + DC[d]
            if 0 <= nr < rows and 0 <= nc < cols and left[nr][nc] == 1:
                union(here, nr * cols + nc)

    for r in range(rows):
        for c in range(cols):
            if left[r][c] == 1:
                join(r, c)
    fallen = [0] * len(hits)
    for k in range(len(hits) - 1, -1, -1):
        r, c = hits[k]
        if grid[r][c] == 1:
            before = size[find(roof)]
            left[r][c] = 1
            join(r, c)
            after = size[find(roof)]
            fallen[k] = max(after - before - 1, 0)
    return fallen


def settled(grid):
    rows, cols = len(grid), len(grid[0])
    out = [[0] * cols for _ in range(rows)]
    stack = []
    for c in range(cols):
        if grid[0][c] == 1:
            out[0][c] = 1
            stack.append((0, c))
    while stack:
        r, c = stack.pop()
        for d in range(4):
            nr, nc = r + DR[d], c + DC[d]
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1 and out[nr][nc] == 0:
                out[nr][nc] = 1
                stack.append((nr, nc))
    return out


def text_list(lst):
    return "[" + ", ".join(str(v) for v in lst) + "]"


def show(grid, hits):
    g = "[" + ", ".join(text_list(row) for row in grid) + "]"
    h = "[" + ", ".join(f"[{r}, {c}]" for r, c in hits) + "]"
    print(f"{g}, {h} -> {text_list(hit_bricks(grid, hits))}")


def main():
    show([[1, 0, 0, 0], [1, 1, 1, 0]], [(1, 0)])
    show([[1, 0, 0, 0], [1, 1, 0, 0]], [(1, 1), (1, 0)])
    show([[1], [1], [1], [1]], [(1, 0)])
    show([[1, 1, 1], [0, 1, 0], [1, 1, 1]], [(0, 1), (0, 0)])
    show([[0, 1, 0], [1, 1, 1]], [(0, 0), (0, 1), (1, 1)])
    show([[1, 1, 1], [1, 0, 1], [1, 1, 1]], [(0, 0), (0, 2), (0, 1)])
    show([[1, 0, 1], [1, 1, 1]], [(0, 0), (0, 2), (1, 1)])
    total = 0
    check = 0
    for i in range(300):
        rows = 1 + next_random() % 8
        cols = 1 + next_random() % 8
        fill = 2 + next_random() % 3
        grid = []
        for _ in range(rows):
            grid.append([1 if next_random() % 4 < fill else 0 for _ in range(cols)])
        grid = settled(grid)
        cells = list(range(rows * cols))
        for j in range(1, rows * cols):
            t = next_random() % (j + 1)
            cells[j], cells[t] = cells[t], cells[j]
        count = 1 + next_random() % (rows * cols)
        hits = [(cells[j] // cols, cells[j] % cols) for j in range(count)]
        for f in hit_bricks(grid, hits):
            total += f
            check = (check * 131 + f + 1) % 1000000007
        check = (check * 131 + i) % 1000000007
    print(f"300 random walls: {total} bricks fell, checksum {check}")


main()
