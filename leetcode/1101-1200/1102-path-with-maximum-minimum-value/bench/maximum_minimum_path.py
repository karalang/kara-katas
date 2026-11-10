# Benchmark: LeetCode #1102 Path With Maximum Minimum Value -- a
# best-first search with heapq, the keys negated, as the Kāra ★ arm.
# Mirrors maximum_minimum_path.kara.
import heapq


def maximum_minimum_path(grid):
    m, n = len(grid), len(grid[0])
    done = [[False] * n for _ in range(m)]
    queue = [(-grid[0][0], 0, 0)]
    while queue:
        low, r, c = heapq.heappop(queue)
        low = -low
        if done[r][c]:
            continue
        done[r][c] = True
        if r == m - 1 and c == n - 1:
            return low
        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and not done[nr][nc]:
                heapq.heappush(queue, (-min(low, grid[nr][nc]), nr, nc))
    return -1


def main():
    seed = 1102

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    grids = [[[next_random() * 30517 % 1000000000 for _ in range(100)] for _ in range(100)] for _ in range(32)]
    total = 0
    check = 0
    for rnd in range(8):
        for j in range(32):
            at = (rnd * 7919 + j * 104729) % 10000
            r, c = at // 100, at % 100
            grids[j][r][c] //= 2
            best = maximum_minimum_path(grids[j])
            total += best
            check = (check * 31 + best % 1000003 + 1) % 1000000007
    print(f"8 rounds over 32 grids of 100 by 100: minimums total {total}, checksum {check}")


main()
