# LeetCode #2146: K Highest Ranked Items Within a Price Range -- the Python
# mirror of ranked.kara's ★ arm.
from collections import deque


def highest_ranked_k_items(grid, pricing, start, k):
    m = len(grid)
    n = len(grid[0])
    low, high = pricing
    seen = [[False] * n for _ in range(m)]
    seen[start[0]][start[1]] = True
    queue = deque([(start[0], start[1], 0)])
    found = []
    while queue:
        r, c, dist = queue.popleft()
        price = grid[r][c]
        if low <= price <= high:
            found.append((dist, price, r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and not seen[nr][nc] and grid[nr][nc] != 0:
                seen[nr][nc] = True
                queue.append((nr, nc, dist + 1))
    found.sort()
    return [[r, c] for _, _, r, c in found[:k]]


seed = 2146


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fmt(cells):
    return "[" + ", ".join(f"[{r}, {c}]" for r, c in cells) + "]"


def show(grid, pricing, start, k):
    print(f"{pricing} {start} {k} -> {fmt(highest_ranked_k_items(grid, pricing, start, k))}".replace("(", "[").replace(")", "]"))


def main():
    show([[1, 2, 0, 1], [1, 3, 0, 1], [0, 2, 5, 1]], [2, 5], [0, 0], 3)
    show([[1, 2, 0, 1], [1, 3, 3, 1], [0, 2, 5, 1]], [2, 3], [2, 3], 2)
    show([[1, 1, 1], [0, 0, 1], [2, 3, 4]], [2, 3], [0, 0], 3)
    show([[4]], [4, 4], [0, 0], 1)
    show([[2, 0, 2], [1, 0, 2]], [2, 2], [0, 0], 5)
    show([[1, 3, 1], [3, 1, 3], [1, 3, 1]], [3, 3], [1, 1], 3)
    total = 0
    check = 0
    for rnd in range(2000):
        m = next_random() % 6 + 1
        n = next_random() % 6 + 1
        top = [5, 100000][rnd % 2]
        grid = []
        for _ in range(m):
            row = []
            for _ in range(n):
                row.append(0 if next_random() % 4 == 0 else next_random() % top + 1)
            grid.append(row)
        sr = next_random() % m
        sc = next_random() % n
        if grid[sr][sc] == 0:
            grid[sr][sc] = 1
        a = next_random() % top + 1
        b = next_random() % top + 1
        k = next_random() % (m * n) + 1
        cells = highest_ranked_k_items(grid, [max(min(a, b), 2), max(a, b, 2)], [sr, sc], k)
        total += len(cells)
        for r, c in cells:
            check = (check * 31 + r * 1000 + c + 1) % 1000000007
    print(f"2000 grids: {total} items in all, checksum {check}")
    grid = [[(r * 316 + c) % 100000 + 1 for c in range(316)] for r in range(316)]
    for r in range(1, 316, 2):
        for c in range(316):
            if (c + r // 2) % 50 == 0:
                grid[r][c] = 0
    every = highest_ranked_k_items(grid, [2, 100000], [158, 158], 99856)
    cheap = highest_ranked_k_items(grid, [2, 1000], [0, 0], 10)
    check = 0
    for r, c in every:
        check = (check * 31 + r * 1000 + c + 1) % 1000000007
    print(f"316 x 316: {len(every)} items ranked, checksum {check}, first {fmt(every[:3])}, cheap {fmt(cheap[:3])}")


main()
