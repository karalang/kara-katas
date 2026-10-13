# Benchmark for #542: Python mirror of the ★ arm (breadth-first search
# from every 0 at once); see update_matrix.kara.
from collections import deque


def update_matrix(mat):
    m, n = len(mat), len(mat[0])
    dist = [[-1] * n for _ in range(m)]
    queue = deque()
    for r in range(m):
        for c in range(n):
            if mat[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))
    steps = ((-1, 0), (1, 0), (0, -1), (0, 1))
    while queue:
        r, c = queue.popleft()
        for dr, dc in steps:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] < 0:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist


seed = 542


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 random 100 by 100 grids (the problem's 10,000 cells), from half
    # ones to 88 in a hundred, built once. Then 50 times over every grid
    # is answered; one row of the answer, picked by the round and the
    # grid, is summed, and one cell goes into the checksum.
    grids = 20
    all_grids = []
    for g in range(grids):
        ones = 50 + 2 * g
        all_grids.append([[1 if next_random() % 100 < ones else 0 for _ in range(100)] for _ in range(100)])
    total = 0
    checksum = 0
    for r in range(50):
        for t in range(grids):
            answer = update_matrix(all_grids[t])
            total += sum(answer[(r * 7 + t * 13) % 100])
            cell = answer[(r * 11 + t * 3) % 100][(r * 5 + t * 17) % 100]
            checksum = (checksum * 31 + cell) % 1000000007
    print(f"{grids} grids, 50 times each: row sum {total}, checksum {checksum}")


main()
