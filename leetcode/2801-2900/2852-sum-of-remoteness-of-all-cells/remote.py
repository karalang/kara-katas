# LeetCode #2852: Sum of Remoteness of All Cells -- the Python mirror of
# the ★ arm: each region flooded breadth first, adding its size times the
# sum of the open cells outside it.
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


seed = 2852


def nr():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = nr()
    return a * 32768 + nr()


def main():
    print(sum_remoteness([[-1, 1, -1], [5, -1, 4], [-1, 3, -1]]), sum_remoteness([[-1, 3, 4], [-1, -1, -1], [3, -1, -1]]), sum_remoteness([[1]]))
    open_ = [[1000000] * 300 for _ in range(300)]
    checker = [[1000000 if (i + j) % 2 == 0 else -1 for j in range(300)] for i in range(300)]
    shut = [[-1] * 300 for _ in range(300)]
    print(sum_remoteness(open_), sum_remoteness(checker), sum_remoteness(shut))
    check = 0
    for c in range(3020):
        small = c < 3000
        n = nr() % 6 + 1 if small else nr() % 300 + 1
        blocked = 3 if small else nr() % 6 + 1
        grid = []
        for _ in range(n):
            row = []
            for _ in range(n):
                if small:
                    row.append(-1 if nr() % 3 == 0 else nr() % 9 + 1)
                elif nr() % 10 < blocked:
                    row.append(-1)
                else:
                    row.append(wide() % 1000000 + 1)
            grid.append(row)
        check = (check * 31 + sum_remoteness(grid)) % 1000000007
        if c == 2999:
            print(f"3000 small grids: checksum {check}")
            check = 0
    print(f"20 large grids: checksum {check}")


main()
