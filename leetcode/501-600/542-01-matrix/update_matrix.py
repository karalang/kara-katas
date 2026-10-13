# LeetCode #542: 01 Matrix -- Python mirror of the ★ arm (breadth-first
# search from every 0 at once); see update_matrix.kara.
from collections import deque


def update_matrix(mat):
    m, n = len(mat), len(mat[0])
    dist = [[-1] * n for _ in range(m)]
    queue = deque()
    for r in range(m):
        for c in range(n):
            if mat[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] < 0:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist


# ---- test harness ---------------------------------------------------------

seed = 542


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(m, n, ones):
    g = [[1 if next_random() % 100 < ones else 0 for _ in range(n)] for _ in range(m)]
    r = next_random() % m
    c = next_random() % n
    g[r][c] = 0
    return g


def mix(h, g):
    for row in g:
        for x in row:
            h = (h * 31 + x + 1) % 1000000007
    return h


def fmt(g):
    return "[" + ", ".join("[" + ", ".join(map(str, row)) + "]" for row in g) + "]"


def show(name, mat):
    print(f"{name}: {fmt(mat)} -> {fmt(update_matrix(mat))}")


def summary(name, mat):
    d = update_matrix(mat)
    print(f"{name}: largest distance {max(max(row) for row in d)}, checksum {mix(0, d)}")


def main():
    show("example 1", [[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    show("example 2", [[0, 0, 0], [0, 1, 0], [1, 1, 1]])
    show("one cell", [[0]])
    show("one row", [[1, 1, 0, 1, 1, 1]])
    show("one column", [[1], [0], [1], [1]])
    show("a 0 in the corner", [[1, 1, 1], [1, 1, 1], [1, 1, 0]])
    count = 300
    cells = 0
    h = 0
    for t in range(count):
        m = 1 + next_random() % 12
        n = 1 + next_random() % 12
        ones = (30, 70, 95)[t % 3]
        cells += m * n
        h = mix(h, update_matrix(random_grid(m, n, ones)))
    print(f"{count} random grids: {cells} cells, checksum {h}")
    summary("100 by 100, 1s at 99 in 100", random_grid(100, 100, 99))
    corner = [[1] * 100 for _ in range(100)]
    corner[0][0] = 0
    summary("100 by 100, one 0 in a corner", corner)
    column = [[1] for _ in range(10000)]
    column[0][0] = 0
    summary("10000 by 1, a 0 at the top", column)


main()
