# LeetCode #2146: K Highest Ranked Items Within a Price Range -- the
# benchmark, the same algorithm as ranked.kara.
from collections import deque

seed = 2146


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw():
    if next_random() % 5 == 0:
        return 0
    return next_random() % 99999 + 2


def highest_ranked_k_items(grid, pricing, start, k):
    m = len(grid)
    n = len(grid[0])
    seen = [[False] * n for _ in range(m)]
    seen[start[0]][start[1]] = True
    queue = deque([(start[0], start[1], 0)])
    found = []
    while queue:
        r, c, dist = queue.popleft()
        price = grid[r][c]
        if pricing[0] <= price <= pricing[1]:
            found.append((dist, price, r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and not seen[nr][nc] and grid[nr][nc] != 0:
                seen[nr][nc] = True
                queue.append((nr, nc, dist + 1))
    found.sort()
    return [[r, c] for _, _, r, c in found[:k]]


def main():
    grids = [[[draw() for _ in range(316)] for _ in range(316)] for _ in range(4)]
    total = check = 0
    for rnd in range(25):
        for g in range(4):
            r = next_random() % 316
            c = next_random() % 316
            grids[g][r][c] = draw()
            sr = next_random() % 316
            sc = next_random() % 316
            if grids[g][sr][sc] == 0:
                grids[g][sr][sc] = 1
            cells = highest_ranked_k_items(grids[g], [2, 50000], [sr, sc], 1000)
            total += len(cells)
            for cr, cc in cells:
                check = (check * 31 + cr * 1000 + cc + rnd) % 1000000007
    print(f"100 searches: {total} items in all, checksum {check}")


main()
