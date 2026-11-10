# LeetCode #1102: Path With Maximum Minimum Value -- Python mirror of the
# ★ arm: a best-first search from the start, the cell whose path carries
# the largest minimum taken next (heapq with the keys negated). Same
# cases and output as maximum_minimum_path.kara.
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


seed = 1102


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(m, n, top):
    return [[(next_random() * 32768 + next_random()) % top for _ in range(n)] for _ in range(m)]


def main():
    cases = [
        [[5, 4, 5], [1, 2, 6], [7, 4, 6]],
        [[2, 2, 1, 2, 2, 2], [1, 2, 2, 2, 1, 2]],
        [[3, 4, 6, 3, 4], [0, 2, 1, 1, 7], [8, 8, 3, 2, 7], [3, 2, 4, 9, 8], [4, 1, 2, 0, 0], [4, 6, 5, 4, 3]],
        [[7]],
        [[0, 9], [9, 9]],
        [[9, 1, 9]],
        [[9], [3], [9]],
        [[5, 1, 5], [5, 1, 5], [5, 5, 5]],
        [[1000000000, 1000000000], [1000000000, 1000000000]],
        [[8, 0, 9, 9, 9], [8, 0, 9, 0, 9], [8, 8, 8, 0, 4]],
    ]
    for grid in cases:
        print(maximum_minimum_path(grid))
    total = 0
    check = 0
    for _ in range(2000):
        m = next_random() % 12 + 1
        n = next_random() % 12 + 1
        top = next_random() % 999 + 2
        best = maximum_minimum_path(random_grid(m, n, top))
        total += best
        check = (check * 31 + best + 1) % 1000000007
    print(f"2000 random grids: minimums total {total}, checksum {check}")
    grid = random_grid(100, 100, 1000000000)
    print(f"100 by 100: {maximum_minimum_path(grid)}")
    snake = [[9 - (r * 100 + c) % 7 % 3 if r % 2 == 1 or (r % 4 == 2 and c == 99) or (r % 4 == 0 and c == 0) else 1
              for c in range(100)] for r in range(100)]
    print(f"100 by 100 snake: {maximum_minimum_path(snake)}")


main()
