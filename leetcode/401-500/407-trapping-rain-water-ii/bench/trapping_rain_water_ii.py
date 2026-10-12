# Benchmark for #407: mirror of trapping_rain_water_ii.kara (a min-heap
# walking in from the border).
import heapq


def trap_rain_water(height):
    m = len(height)
    if m < 3 or len(height[0]) < 3:
        return 0
    n = len(height[0])
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


def main():
    grids = 60
    size = 200
    seed = 407
    total = 0
    checksum = 0

    def step():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    for _ in range(grids):
        grid = []
        for _ in range(size):
            row = []
            for _ in range(size):
                hi = step()
                row.append((hi * 32768 + step()) % 20000)
            grid.append(row)
        w = trap_rain_water(grid)
        total += w
        checksum = (checksum * 31 + w) % 1000000007
    print(f"{grids} grids of {size} x {size}: {total} units of water, checksum {checksum}")


main()
