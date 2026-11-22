# LeetCode #2852: Sum of Remoteness of All Cells -- the bench: the ★ arm
# over 20 grids of 300 x 300, LeetCode's most, values up to 10^6, a cell
# blocked from 1 time in 10 to 6 in 10, all drawn first, then each
# answered 10 times.
from collections import deque


def sum_remoteness(grid):
    n = len(grid)
    total = sum(v for row in grid for v in row if v > 0)
    seen = [[False] * n for _ in range(n)]
    answer = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] < 0 or seen[i][j]:
                continue
            seen[i][j] = True
            queue = deque([(i, j)])
            size = s = 0
            while queue:
                r, c = queue.popleft()
                size += 1
                s += grid[r][c]
                for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] > 0 and not seen[nr][nc]:
                        seen[nr][nc] = True
                        queue.append((nr, nc))
            answer += size * (total - s)
    return answer


def main():
    count, rounds, n = 20, 10, 300
    seed = 2852

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide():
        a = nr()
        return a * 32768 + nr()

    grids = []
    for _ in range(count):
        blocked = nr() % 6 + 1
        grids.append([[-1 if nr() % 10 < blocked else wide() % 1000000 + 1 for _ in range(n)] for _ in range(n)])
    check = 0
    for r in range(rounds):
        for grid in grids:
            check = (check * 31 + sum_remoteness(grid) % 1000000007 + r) % 1000000007
    print(f"{count} grids of {n} x {n}, {rounds} rounds: checksum {check}")


main()
