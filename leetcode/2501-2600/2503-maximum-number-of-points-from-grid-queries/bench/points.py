# LeetCode #2503: Maximum Number of Points From Grid Queries -- benchmark
# mirror of the ★ arm (points.kara): 4 grids of 316 by 316 and 10^4
# queries, built once, then the passes; each sets one cell of every grid
# from the checksum so far, asks every query, and puts it back.
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
    hi = next_random()
    return (hi * 32768 + next_random()) % top


def main():
    passes = 14
    grids = [[[below(1000000) + 1 for _ in range(316)] for _ in range(316)] for _ in range(4)]
    queries = [below(1000000) + 1 for _ in range(10000)]
    check = 0
    for p in range(passes):
        for grid in grids:
            r = check % 316
            c = check // 316 % 316
            was = grid[r][c]
            grid[r][c] = (check + p) % 1000000 + 1
            for a in max_points(grid, queries):
                check = (check * 31 + a + p) % 1000000007
            grid[r][c] = was
    print(f"{passes} passes over 4 grids of 316 by 316, 10^4 queries: checksum {check}")


main()
