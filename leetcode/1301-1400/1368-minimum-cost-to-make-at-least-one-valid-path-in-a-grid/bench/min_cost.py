# LeetCode #1368 bench -- Python: a 0-1 breadth-first search over the
# cells, a step the sign points to costing 0 and going to the front of
# the deque, any other costing 1 and going to its back.
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


def main():
    # 20 grids of 100 by 100 signs, the constraints' most, built once;
    # then 600 rounds, each changing one cell's sign and finding the
    # cheapest valid path through that grid, all drawn from the checksum
    # so far
    grids = [[[1 + next_random() % 4 for _ in range(100)] for _ in range(100)] for _ in range(20)]
    check = 0
    for r in range(600):
        g = check % 20
        cell = (check // 20) % 10000
        grids[g][cell // 100][cell % 100] = 1 + (check // 200000) % 4
        cost = min_cost(grids[g])
        check = (check * 31 + cost + r) % 1000000007
    print(f"600 rounds over 20 grids of 100 by 100: checksum {check}")


main()
