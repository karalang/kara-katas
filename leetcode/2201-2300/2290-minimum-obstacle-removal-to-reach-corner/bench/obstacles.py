# LeetCode #2290: Minimum Obstacle Removal to Reach Corner -- the bench,
# the ★ arm's Python mirror. A 0-1 breadth-first search over a deque.

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


# ---- bench harness ---------------------------------------------------------

seed = 2290


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    grids = []
    for _ in range(10):
        grid = [[1 if next_random() % 10 < 4 else 0 for _ in range(200)] for _ in range(200)]
        grid[0][0] = 0
        grid[199][199] = 0
        grids.append(grid)
    check = 0
    for _ in range(5):
        total = 0
        for grid in grids:
            total += minimum_obstacles(grid)
        check = (check * 31 + total) % 1000000007
    print(f"5 passes over 10 grids of 200x200: checksum {check}")


main()
