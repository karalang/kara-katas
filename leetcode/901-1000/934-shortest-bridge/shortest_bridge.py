# LeetCode #934: Shortest Bridge -- mark one island, then search outward
# (Python mirror).

DR = [-1, 1, 0, 0]
DC = [0, 0, -1, 1]


def shortest_bridge(grid):
    n = len(grid)
    dist = [-1] * (n * n)
    start = 0
    while grid[start // n][start % n] == 0:
        start += 1
    stack = [start]
    frontier = []
    dist[start] = 0
    while stack:
        cell = stack.pop()
        frontier.append(cell)
        for d in range(4):
            r = cell // n + DR[d]
            c = cell % n + DC[d]
            if 0 <= r < n and 0 <= c < n and grid[r][c] == 1 and dist[r * n + c] < 0:
                dist[r * n + c] = 0
                stack.append(r * n + c)
    head = 0
    while head < len(frontier):
        cell = frontier[head]
        head += 1
        for d in range(4):
            r = cell // n + DR[d]
            c = cell % n + DC[d]
            if 0 <= r < n and 0 <= c < n and dist[r * n + c] < 0:
                if grid[r][c] == 1:
                    return dist[cell]
                dist[r * n + c] = dist[cell] + 1
                frontier.append(r * n + c)
    return -1


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(name, grid):
    print(f"{name}: {shortest_bridge(grid)}")


def beside(grid, r, c, mark):
    n = len(grid)
    return ((r > 0 and grid[r - 1][c] == mark) or (r + 1 < n and grid[r + 1][c] == mark)
            or (c > 0 and grid[r][c - 1] == mark) or (c + 1 < n and grid[r][c + 1] == mark))


def grow(grid, cells, size, mark, avoid):
    n = len(grid)
    tries = 0
    while len(cells) < size and tries < 4 * size:
        tries += 1
        cell = cells[next_random() % len(cells)]
        d = next_random() % 4
        r = cell // n + DR[d]
        c = cell % n + DC[d]
        if 0 <= r < n and 0 <= c < n and grid[r][c] == 0 and not beside(grid, r, c, avoid):
            grid[r][c] = mark
            cells.append(r * n + c)


def random_islands(n, size_a, size_b):
    while True:
        grid = [[0] * n for _ in range(n)]
        a = next_random() % (n * n)
        grid[a // n][a % n] = 2
        cells_a = [a]
        grow(grid, cells_a, size_a, 2, -1)
        b = -1
        for _ in range(100):
            x = next_random() % (n * n)
            if b < 0 and grid[x // n][x % n] == 0 and not beside(grid, x // n, x % n, 2):
                b = x
        if b >= 0:
            grid[b // n][b % n] = 3
            cells_b = [b]
            grow(grid, cells_b, size_b, 3, 2)
            return [[1 if v > 0 else 0 for v in row] for row in grid]


def main():
    global seed
    show("example 1", [[0, 1], [1, 0]])
    show("example 2", [[0, 1, 0], [0, 0, 0], [0, 0, 1]])
    show("example 3", [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]])
    show("two strips", [[1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1]])
    show("opposite corners", [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])
    show("centre of a ring", [[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1]])
    seed = 934
    total = 0
    check = 0
    for _ in range(300):
        n = 2 + next_random() % 59
        size_a = 1 + next_random() % (n * n // 4 + 1)
        size_b = 1 + next_random() % (n * n // 4 + 1)
        a = shortest_bridge(random_islands(n, size_a, size_b))
        total += a
        check = (check * 1000003 + a) % 1000000007
    print(f"300 random grids: answers summing to {total}, checksum {check}")
    corners = [[0] * 100 for _ in range(100)]
    corners[0][0] = 1
    corners[99][99] = 1
    halves = [[0 if c == 50 else 1 for c in range(100)] for _ in range(100)]
    a = shortest_bridge(corners)
    b = shortest_bridge(halves)
    c = shortest_bridge(random_islands(100, 2000, 2000))
    print(f"100 x 100: opposite corners {a}, two halves {b}, random islands {c}")


main()
