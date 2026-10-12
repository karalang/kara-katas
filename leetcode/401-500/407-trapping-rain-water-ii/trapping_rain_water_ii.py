# LeetCode #407: Trapping Rain Water II -- mirror of trapping_rain_water_ii.kara
# (a min-heap walking in from the border).
import heapq


def trap_rain_water(height):
    m = len(height)
    n = len(height[0]) if m else 0
    if m < 3 or n < 3:
        return 0
    seen = [[False] * n for _ in range(m)]
    heap = []
    for r in range(m):
        for c in range(n):
            if r == 0 or c == 0 or r == m - 1 or c == n - 1:
                heapq.heappush(heap, (height[r][c], r, c))
                seen[r][c] = True
    water = 0
    while heap:
        level, r, c = heapq.heappop(heap)
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and not seen[nr][nc]:
                seen[nr][nc] = True
                if height[nr][nc] < level:
                    water += level - height[nr][nc]
                heapq.heappush(heap, (max(level, height[nr][nc]), nr, nc))
    return water


seed = 407


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(name, grid):
    print(f"{name}: {trap_rain_water(grid)}")


show("example 1", [[1, 4, 3, 1, 3, 2], [3, 2, 1, 3, 2, 4], [2, 3, 3, 2, 3, 1]])
show("example 2", [[3, 3, 3, 3, 3], [3, 2, 2, 2, 3], [3, 2, 1, 2, 3], [3, 2, 2, 2, 3], [3, 3, 3, 3, 3]])
show("one cell", [[5]])
show("one row", [[3, 0, 3, 0, 3]])
show("two by two", [[1, 0], [0, 1]])
show("a pit", [[5, 5, 5], [5, 0, 5], [5, 5, 5]])
show("a leaky wall", [[5, 5, 5, 5], [5, 0, 0, 1], [5, 5, 5, 5]])
show("a lower rim", [[9, 9, 9, 9, 9], [9, 1, 4, 1, 9], [9, 4, 2, 4, 9], [9, 1, 4, 1, 9], [9, 9, 3, 9, 9]])
show("two basins", [[6, 6, 6, 6, 6, 6, 6], [6, 1, 6, 8, 2, 2, 8], [6, 6, 6, 8, 8, 8, 8]])
total = 0
checksum = 0
for _ in range(1000):
    m = 1 + step() % 12
    n = 1 + step() % 12
    grid = [[step() % 10 for _ in range(n)] for _ in range(m)]
    w = trap_rain_water(grid)
    total += w
    checksum = (checksum * 31 + w + 1) % 1000000007
print(f"1000 random grids: {total} units of water, checksum {checksum}")
