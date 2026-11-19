# LeetCode #1631: Path With Minimum Effort -- the bench's Python mirror:
# the ★ arm on 200 random grids of 100 x 100 heights up to 10^6, all drawn
# first.

import heapq


def minimum_effort_path(heights):
    rows, cols = len(heights), len(heights[0])
    best = [[2**31 - 1] * cols for _ in range(rows)]
    best[0][0] = 0
    queue = [(0, 0, 0)]
    while queue:
        effort, r, c = heapq.heappop(queue)
        if r == rows - 1 and c == cols - 1:
            return effort
        if effort > best[r][c]:
            continue
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            step = max(effort, abs(heights[nr][nc] - heights[r][c]))
            if step < best[nr][nc]:
                best[nr][nc] = step
                heapq.heappush(queue, (step, nr, nc))
    return 0


seed = 1631


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


grids = []
for _ in range(200):
    heights = []
    for _ in range(100):
        row = []
        for _ in range(100):
            high = next_random()
            row.append((high * 32768 + next_random()) % 1000000 + 1)
        heights.append(row)
    grids.append(heights)
check = 0
total = 0
for heights in grids:
    effort = minimum_effort_path(heights)
    total += effort
    check = (check * 31 + effort + 1) % 1000000007
print(f"200 grids of 100 x 100: efforts sum to {total}, checksum {check}")
