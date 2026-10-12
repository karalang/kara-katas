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


def ridge(r, c, n):
    a = r + c
    b = 2 * n - 2 - r - c
    return a if a < b else b


def main():
    n = 200
    rounds = 3000
    heights = [[3 * ridge(r, c, n) + step() % 3 for c in range(n)] for r in range(n)]
    total = 0
    checksum = 0
    for _ in range(rounds):
        r = step() % n
        c = step() % n
        heights[r][c] = step() % (3 * ridge(r, c, n) + 3)
        cells = pacific_atlantic(heights)
        total += len(cells)
        lr, lc = cells[-1]
        checksum = (checksum * 31 + len(cells) + lr * n + lc) % 1000000007
    print(f"{rounds} rounds on a {n}x{n} grid: {total} cells, checksum {checksum}")


main()
