# LeetCode #1391: Check if There is a Valid Path in a Grid -- Python
# mirror of the ★ arm: a breadth-first search from the top-left cell,
# stepping to a neighbour only when its street opens back.
from collections import deque

# each street's two openings, as (row step, column step)
WAYS = [[], [(0, -1), (0, 1)], [(-1, 0), (1, 0)], [(0, -1), (1, 0)],
        [(0, 1), (1, 0)], [(0, -1), (-1, 0)], [(0, 1), (-1, 0)]]


def has_valid_path(grid):
    m, n = len(grid), len(grid[0])
    seen = [False] * (m * n)
    queue = deque([(0, 0)])
    seen[0] = True
    while queue:
        r, c = queue.popleft()
        if r == m - 1 and c == n - 1:
            return True
        for dr, dc in WAYS[grid[r][c]]:
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= m or nc < 0 or nc >= n or seen[nr * n + nc]:
                continue
            if (-dr, -dc) in WAYS[grid[nr][nc]]:
                seen[nr * n + nc] = True
                queue.append((nr, nc))
    return False


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# sides: 0 up, 1 right, 2 down, 3 left; each street's pair of sides
SIDES = [(-1, -1), (3, 1), (0, 2), (3, 2), (1, 2), (3, 0), (1, 0)]


def street_joining(a, b):
    for s in range(1, 7):
        x, y = SIDES[s]
        if (x == a and y == b) or (x == b and y == a):
            return s
    return 0


def planted(m, n, broken):
    grid = [[1 + next_random() % 6 for _ in range(n)] for _ in range(m)]
    path = []
    r = c = 0
    came = -1
    while r != m - 1 or c != n - 1:
        if r == m - 1:
            go = 1
        elif c == n - 1:
            go = 2
        else:
            go = 1 if next_random() % 2 == 0 else 2
        frm = came if came >= 0 else (go + 1 + next_random() % 3) % 4
        grid[r][c] = street_joining(frm, go)
        path.append((r, c))
        if go == 1:
            c += 1
            came = 3
        else:
            r += 1
            came = 0
    if came >= 0:
        grid[r][c] = street_joining(came, (came + 1 + next_random() % 3) % 4)
    path.append((r, c))
    if broken:
        pr, pc = path[next_random() % len(path)]
        grid[pr][pc] = 1 + next_random() % 6
    return grid


def word(b):
    return "true" if b else "false"


def main():
    global seed
    shown = [
        has_valid_path([[2, 4, 3], [6, 5, 2]]),
        has_valid_path([[1, 2, 1], [1, 2, 1]]),
        has_valid_path([[1, 1, 2]]),
        has_valid_path([[1, 1, 1, 1, 1, 1, 3]]),
        has_valid_path([[2], [2], [2], [2], [2], [2], [6]]),
        has_valid_path([[4, 3], [6, 5]]),
        has_valid_path([[4, 3, 1], [6, 5, 1]]),
        has_valid_path([[5]]),
    ]
    print(" ".join(word(b) for b in shown))
    seed = 1391
    big = [has_valid_path(planted(300, 300, g % 2 == 1)) for g in range(6)]
    print("300 by 300, planted, every other one broken: " + " ".join(word(b) for b in big))
    check = 0
    found = 0
    for c in range(2000):
        m = 1 + next_random() % 12
        n = 1 + next_random() % 12
        got = has_valid_path(planted(m, n, c % 2 == 1))
        if got:
            found += 1
        check = (check * 131 + (2 if got else 1) * (m * 13 + n)) % 1000000007
    print(f"2000 random grids: {found} with a path, checksum {check}")


main()
