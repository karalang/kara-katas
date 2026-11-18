# LeetCode #2290: Minimum Obstacle Removal to Reach Corner -- the ★ arm's
# Python mirror. A 0-1 breadth-first search over a deque.

from collections import deque


def minimum_obstacles(grid):
    m = len(grid)
    n = len(grid[0])
    cost = [-1] * (m * n)
    best = [1 << 62] * (m * n)
    queue = deque()
    best[0] = 0
    queue.append((0, 0))
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while queue:
        r, c = queue.popleft()
        if cost[r * n + c] >= 0:
            continue
        here = best[r * n + c]
        cost[r * n + c] = here
        if r == m - 1 and c == n - 1:
            return here
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if nr < 0 or nc < 0 or nr >= m or nc >= n:
                continue
            step = grid[nr][nc]
            if here + step < best[nr * n + nc]:
                best[nr * n + nc] = here + step
                if step == 0:
                    queue.appendleft((nr, nc))
                else:
                    queue.append((nr, nc))
    return best[m * n - 1]


# ---- test harness ---------------------------------------------------------

seed = 2290


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        [[0, 1, 1], [1, 1, 0], [1, 1, 0]],
        [[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]],
        [[0]],
        [[0, 1, 1, 0, 1, 0]],
        [[0], [1], [1], [0]],
        [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [1, 1, 1, 0]],
        [[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]],
    ]
    for grid in cases:
        print(f"{len(grid)}x{len(grid[0])}: {minimum_obstacles(grid)}")
    check = 0
    total = 0
    for _ in range(2000):
        m = next_random() % 20 + 1
        n = next_random() % 20 + 1
        tenths = next_random() % 9 + 1
        grid = []
        for r in range(m):
            row = []
            for c in range(n):
                wall = next_random() % 10 < tenths
                row.append(1 if wall and not (r == 0 and c == 0) and not (r == m - 1 and c == n - 1) else 0)
            grid.append(row)
        removed = minimum_obstacles(grid)
        check = (check * 31 + removed) % 1000000007
        total += removed
    print(f"2000 grids: checksum {check}, {total} removed")


main()
