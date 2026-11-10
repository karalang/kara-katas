# Benchmark: LeetCode #1091 Shortest Path in Binary Matrix -- Python mirror
# of the ★ arm: breadth-first search with a deque and a grid of distances.
# Same workload and sink as shortest_path_binary_matrix.kara.
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


def main():
    seed = 1091

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    grids = []
    for k in range(200):
        blocked = 25 + k % 20
        grid = [[1 if next_random() % 100 < blocked else 0 for _ in range(100)] for _ in range(100)]
        grid[0][0] = 0
        grid[99][99] = 0
        grids.append(grid)
    none = total = check = 0
    for _ in range(20):
        for grid in grids:
            answer = shortest_path_binary_matrix(grid)
            if answer == -1:
                none += 1
            else:
                total += answer
            check = (check * 31 + answer + 1) % 1000000007
    print(f"20 rounds over 200 grids of 100 by 100: {none} without a path, lengths sum to {total}, checksum {check}")


main()
