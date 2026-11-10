# LeetCode #1091: Shortest Path in Binary Matrix -- Python mirror of the ★
# arm: breadth-first search from the top left cell over the eight
# neighbours, a deque of cells and a grid of distances counted in cells.
from collections import deque


def shortest_path_binary_matrix(grid):
    n = len(grid)
    if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
        return -1
    dist = [[-1] * n for _ in range(n)]
    dist[0][0] = 1
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if r == n - 1 and c == n - 1:
            return dist[r][c]
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))
    return -1


seed = 1091


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def parse(rows):
    return [[1 if ch == "1" else 0 for ch in r] for r in rows]


def random_grid(n, blocked):
    return [[1 if next_random() % 100 < blocked else 0 for _ in range(n)] for _ in range(n)]


def main():
    cases = [
        ["01", "10"],
        ["000", "110", "110"],
        ["100", "110", "110"],
        ["0"],
        ["1"],
        ["00", "01"],
        ["0000", "1110", "0000", "0110"],
        ["00000", "11110", "00000", "01111", "00000"],
        ["0100", "0101", "0101", "0001"],
        ["000", "000", "000"],
        ["010", "111", "010"],
        ["0110", "1001", "1001", "0110"],
    ]
    for rows in cases:
        print(f"{'/'.join(rows)} -> {shortest_path_binary_matrix(parse(rows))}")
    h = 0
    total = 0
    none = 0
    for _ in range(2000):
        n = next_random() % 12 + 1
        blocked = next_random() % 26 + 25
        grid = random_grid(n, blocked)
        answer = shortest_path_binary_matrix(grid)
        if answer == -1:
            none += 1
        else:
            total += answer
        h = (h * 31 + answer + 1) % 1000000007
    print(f"2000 random grids: {none} without a path, lengths sum to {total}, checksum {h}")
    for blocked in (10, 30, 40):
        grid = random_grid(100, blocked)
        grid[0][0] = 0
        grid[99][99] = 0
        print(f"100 by 100, {blocked}% blocked: {shortest_path_binary_matrix(grid)}")


main()
