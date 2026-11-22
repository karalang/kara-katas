# LeetCode #2812: Find the Safest Path in a Grid -- the Python mirror of
# the ★ arm: one breadth-first search from every thief at once, then a
# binary search on the answer, each guess asked by a breadth-first search.
from collections import deque

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def thief_distances(grid):
    n = len(grid)
    dist = [[-1] * n for _ in range(n)]
    queue = deque()
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                dist[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist


def reachable(dist, s):
    n = len(dist)
    if dist[0][0] < s:
        return False
    seen = [[False] * n for _ in range(n)]
    seen[0][0] = True
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if r == n - 1 and c == n - 1:
            return True
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc] and dist[nr][nc] >= s:
                seen[nr][nc] = True
                queue.append((nr, nc))
    return False


def maximum_safeness_factor(grid):
    n = len(grid)
    dist = thief_distances(grid)
    lo, hi = 0, min(dist[0][0], dist[n - 1][n - 1])
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if reachable(dist, mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


seed = 2812


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(n, odds):
    grid = [[1 if next_random() % odds == 0 else 0 for _ in range(n)] for _ in range(n)]
    r = next_random() % n
    c = next_random() % n
    grid[r][c] = 1
    return grid


def main():
    print(maximum_safeness_factor([[1, 0, 0], [0, 0, 0], [0, 0, 1]]))
    print(maximum_safeness_factor([[0, 0, 1], [0, 0, 0], [0, 0, 0]]))
    print(maximum_safeness_factor([[0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]))
    print(maximum_safeness_factor([[1]]))
    middle = [[0] * 100 for _ in range(100)]
    middle[50][50] = 1
    print(maximum_safeness_factor(middle))
    for count, top, odds, label in ((3000, 6, 4, "small"), (50, 60, 200, "large")):
        total = 0
        check = 0
        for _ in range(count):
            n = next_random() % top + 1
            a = maximum_safeness_factor(random_grid(n, odds))
            total += a
            check = (check * 31 + a + 1) % 1000000007
        print(f"{count} {label} grids: safeness sums to {total}, checksum {check}")


main()
