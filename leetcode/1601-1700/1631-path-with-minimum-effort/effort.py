# LeetCode #1631: Path With Minimum Effort -- the Python mirror of the ★
# arm: Dijkstra's algorithm on a heap of (effort, row, column), a path's
# cost its largest step.

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


# ---- the harness: the same as every arm's ---------------------------------

seed = 1631


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, top):
    check = 0
    total = 0
    for _ in range(count):
        rows = next_random() % most + 1
        cols = next_random() % most + 1
        heights = [[next_random() % top + 1 for _ in range(cols)] for _ in range(rows)]
        effort = minimum_effort_path(heights)
        total += effort
        check = (check * 31 + effort + 1) % 1000000007
    print(f"{count} grids of up to {most} x {most}: efforts sum to {total}, checksum {check}")


print(minimum_effort_path([[1, 2, 2], [3, 8, 2], [5, 3, 5]]))
print(minimum_effort_path([[1, 2, 3], [3, 8, 4], [5, 3, 5]]))
print(minimum_effort_path([[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]]))
print(minimum_effort_path([[7]]))
print(minimum_effort_path([[1, 10, 4, 6]]))
batch(2000, 4, 5)
batch(200, 20, 1000)
batch(5, 100, 30000)
