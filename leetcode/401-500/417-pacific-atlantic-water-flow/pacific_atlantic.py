# LeetCode #417: Pacific Atlantic Water Flow -- mirror of
# pacific_atlantic.kara (search up from each ocean).
from collections import deque


def climb(heights, queue):
    rows = len(heights)
    cols = len(heights[0])
    seen = [[False] * cols for _ in range(rows)]
    for r, c in queue:
        seen[r][c] = True
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    while queue:
        r, c = queue.popleft()
        for k in range(4):
            nr = r + dr[k]
            nc = c + dc[k]
            if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc] and heights[nr][nc] >= heights[r][c]:
                seen[nr][nc] = True
                queue.append((nr, nc))
    return seen


def pacific_atlantic(heights):
    rows = len(heights)
    cols = len(heights[0])
    pacific = deque()
    atlantic = deque()
    for r in range(rows):
        pacific.append((r, 0))
        atlantic.append((r, cols - 1))
    for c in range(cols):
        pacific.append((0, c))
        atlantic.append((rows - 1, c))
    to_pacific = climb(heights, pacific)
    to_atlantic = climb(heights, atlantic)
    return [(r, c) for r in range(rows) for c in range(cols) if to_pacific[r][c] and to_atlantic[r][c]]


seed = 417


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(heights):
    cells = pacific_atlantic(heights)
    line = " ".join(f"({r},{c})" for r, c in cells)
    print(f"{len(heights)}x{len(heights[0])}: {len(cells)} cells: {line}")


show([
    [1, 2, 2, 3, 5],
    [3, 2, 3, 4, 4],
    [2, 4, 5, 3, 1],
    [6, 7, 1, 4, 5],
    [5, 1, 1, 2, 4],
])
show([[1]])
show([[3, 3, 3], [3, 3, 3]])
show([[1, 2, 3, 4, 5]])
show([[5], [1], [4]])
show([[9, 9, 9], [9, 1, 9], [9, 9, 9]])
show([[1, 1, 1], [1, 9, 1], [1, 1, 1]])
show([[1, 2, 3], [8, 9, 4], [7, 6, 5]])
show([[10, 1, 10], [1, 1, 1], [10, 1, 10]])
total = 0
checksum = 0
for _ in range(1000):
    rows = 1 + step() % 12
    cols = 1 + step() % 12
    limit = 1 + step() % 10
    heights = [[step() % limit for _ in range(cols)] for _ in range(rows)]
    cells = pacific_atlantic(heights)
    total += len(cells)
    for r, c in cells:
        checksum = (checksum * 31 + r * 13 + c + 1) % 1000000007
print(f"1000 random grids: {total} cells, checksum {checksum}")
