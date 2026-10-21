# LeetCode 827 — Making A Large Island, by labelling the islands.
#
# Mirrors largest_island.kara: a breadth-first search labels every island
# and records its size; each 0 joins the distinct islands beside it, and a
# grid with no 0 is one island.
from collections import deque

def largest_island(grid):
    n = len(grid)
    label = [[0] * n for _ in range(n)]
    size = []
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1 and label[r][c] == 0:
                ident = len(size) + 1
                label[r][c] = ident
                queue = deque([(r, c)])
                count = 0
                while queue:
                    cr, cc = queue.popleft()
                    count += 1
                    for k in range(4):
                        nr = cr + dr[k]
                        nc = cc + dc[k]
                        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1 and label[nr][nc] == 0:
                            label[nr][nc] = ident
                            queue.append((nr, nc))
                size.append(count)
    best = max(size, default=0)
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                seen = []
                made = 1
                for k in range(4):
                    nr = r + dr[k]
                    nc = c + dc[k]
                    if 0 <= nr < n and 0 <= nc < n:
                        ident = label[nr][nc]
                        if ident > 0 and ident not in seen:
                            seen.append(ident)
                            made += size[ident - 1]
                best = max(best, made)
    return best

seed = 0
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def show(grid):
    text = "[" + ", ".join("[" + ", ".join(map(str, row)) + "]" for row in grid) + "]"
    print(f"{text} -> {largest_island(grid)}")

def random_grid(n, land):
    return [[1 if next_random() % 100 < land else 0 for _ in range(n)] for _ in range(n)]

show([[1, 0], [0, 1]])
show([[1, 1], [1, 0]])
show([[1, 1], [1, 1]])
show([[0]])
show([[1]])
show([[0, 0], [0, 0]])
show([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
show([[1, 0, 1], [0, 0, 0], [1, 0, 1]])
show([[1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [0, 0, 0, 0, 0], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1]])
seed = 827
print(f"500 by 500, half land -> {largest_island(random_grid(500, 50))}")
print(f"500 by 500, 60% land -> {largest_island(random_grid(500, 60))}")
print(f"500 by 500, all water -> {largest_island(random_grid(500, 0))}")
total = 0
check = 0
for _ in range(300):
    n = 1 + next_random() % 8
    land = 20 + next_random() % 60
    r = largest_island(random_grid(n, land))
    total += r
    check = (check * 131 + r) % 1000000007
print(f"300 random grids: total {total}, checksum {check}")
