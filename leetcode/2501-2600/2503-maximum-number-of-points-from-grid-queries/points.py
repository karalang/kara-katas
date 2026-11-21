# LeetCode #2503: Maximum Number of Points From Grid Queries -- mirror of
# the ★ arm (points.kara): the queries answered in increasing order by
# one growing region, its border in a least-first heap of (value, cell).
import heapq


def max_points(grid, queries):
    m, n = len(grid), len(grid[0])
    order = sorted(range(len(queries)), key=lambda i: queries[i])
    answer = [0] * len(queries)
    seen = [[False] * n for _ in range(m)]
    border = [(grid[0][0], 0)]
    seen[0][0] = True
    reached = 0
    for i in order:
        q = queries[i]
        while border and border[0][0] < q:
            _, cell = heapq.heappop(border)
            reached += 1
            r, c = divmod(cell, n)
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                rr, cc = r + dr, c + dc
                if 0 <= rr < m and 0 <= cc < n and not seen[rr][cc]:
                    seen[rr][cc] = True
                    heapq.heappush(border, (grid[rr][cc], rr * n + cc))
        answer[i] = reached
    return answer


seed = 2503


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(top):
    return (next_random() * 32768 + next_random()) % top


def random_grid(m, n, top):
    return [[below(top) + 1 for _ in range(n)] for _ in range(m)]


def fold(check, answers):
    for a in answers:
        check = (check * 31 + a) % 1000000007
    return check


def main():
    cases = [
        ([[1, 2, 3], [2, 5, 7], [3, 5, 1]], [5, 6, 2]),
        ([[5, 2, 1], [1, 1, 2]], [3]),
        ([[1, 1], [1, 1]], [1, 2, 1000000]),
        ([[3, 1], [1, 3]], [3, 4, 2]),
        ([[1, 9, 1, 1], [1, 9, 1, 9], [1, 1, 1, 9]], [2, 10, 9, 1]),
        ([[2, 2, 2], [2, 9, 2], [2, 2, 2]], [3, 9, 10]),
        ([[1000000, 1], [1, 1]], [1000000, 999999]),
        ([[1, 5, 4, 7, 2, 8], [9, 9, 9, 9, 9, 9]], [3, 6, 9, 10]),
    ]
    for grid, queries in cases:
        print(f"{len(grid)} by {len(grid[0])}, {queries} -> {max_points(grid, queries)}")
    for top in [10, 1000000]:
        check = 0
        for _ in range(1000):
            m = next_random() % 7 + 2
            n = next_random() % 7 + 2
            grid = random_grid(m, n, top)
            queries = [below(top + 1) + 1 for _ in range(next_random() % 10 + 1)]
            check = fold(check, max_points(grid, queries))
        print(f"1000 random to {top}: checksum {check}")
    big = random_grid(316, 316, 1000000)
    queries = [below(1000000) + 1 for _ in range(10000)]
    print(f"316 by 316, 10^4 queries: checksum {fold(0, max_points(big, queries))}")
    snake = [[(c if r % 4 == 0 else (999999 if (r % 4 == 1 and c != 999) or (r % 4 == 3 and c != 0) else c)) + 1 for c in range(1000)] for r in range(100)]
    rising = [(t + 1) * 100 for t in range(10000)]
    print(f"100 by 1000 walls, 10^4 queries: checksum {fold(0, max_points(snake, rising))}")
    flat = [[7] * 50000 for _ in range(2)]
    print(f"2 by 50000 sevens: {max_points(flat, [7, 8, 1000000])}")


main()
