# LeetCode #1368: Minimum Cost to Make at Least One Valid Path in a Grid
# -- Python mirror of the ★ arm: a 0-1 breadth-first search, a step the
# cell's sign points to costing 0 and going to the deque's front, any
# other costing 1 and going to its back.
from collections import deque

MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]
INF = 2147483647


def min_cost(grid):
    m, n = len(grid), len(grid[0])
    cost = [[INF] * n for _ in range(m)]
    queue = deque()
    cost[0][0] = 0
    queue.append((0, 0))
    while queue:
        r, c = queue.popleft()
        for d in range(4):
            nr, nc = r + MOVES[d][0], c + MOVES[d][1]
            if nr < 0 or nr >= m or nc < 0 or nc >= n:
                continue
            step = 0 if grid[r][c] == d + 1 else 1
            if cost[r][c] + step < cost[nr][nc]:
                cost[nr][nc] = cost[r][c] + step
                if step == 0:
                    queue.appendleft((nr, nc))
                else:
                    queue.append((nr, nc))
    return cost[m - 1][n - 1]


seed = 1368


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(m, n):
    return [[1 + next_random() % 4 for _ in range(n)] for _ in range(m)]


def main():
    e1 = min_cost([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]])
    e2 = min_cost([[1, 1, 3], [3, 2, 2], [1, 1, 4]])
    e3 = min_cost([[1, 2], [4, 3]])
    one = min_cost([[4]])
    left = min_cost([[2] * 100 for _ in range(100)])
    big = min_cost(random_grid(100, 100))
    print(f"{e1} {e2} {e3} {one} {left} {big}")
    total = 0
    check = 0
    for _ in range(2000):
        m = 1 + next_random() % 30
        n = 1 + next_random() % 30
        got = min_cost(random_grid(m, n))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random grids: costs total {total}, checksum {check}")


main()
