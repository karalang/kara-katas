# LeetCode #1162: As Far from Land as Possible -- a Python mirror of the
# ★ arm (a breadth-first search from every land cell at once) and its
# test harness; the output is byte-identical to max_distance.kara's.
import sys


def max_distance(grid):
    n = len(grid)
    dist = [-1] * (n * n)
    queue = []
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                dist[i * n + j] = 0
                queue.append(i * n + j)
    if len(queue) == 0 or len(queue) == n * n:
        return -1
    head = 0
    far = 0
    while head < len(queue):
        cell = queue[head]
        head += 1
        i, j = cell // n, cell % n
        far = dist[cell]
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            a, b = i + di, j + dj
            if 0 <= a < n and 0 <= b < n and dist[a * n + b] < 0:
                dist[a * n + b] = far + 1
                queue.append(a * n + b)
    return far


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(n, land):
    return [[1 if next_random() % 100 < land else 0 for _ in range(n)] for _ in range(n)]


def parse(s):
    inner = s[2:-2]
    return [[int(c) for c in row.split(",")] for row in inner.split("],[")]


def main(solve):
    global seed
    cases = [
        "[[1,0,1],[0,0,0],[1,0,1]]",
        "[[1,0,0],[0,0,0],[0,0,0]]",
        "[[1]]",
        "[[0]]",
        "[[1,1],[1,1]]",
        "[[0,0,0],[0,0,0],[0,0,0]]",
        "[[0,1],[0,0]]",
        "[[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1]]",
    ]
    for c in cases:
        print(f"{c} -> {solve(parse(c))}")
    seed = 1162
    total = 0
    check = 0
    for _ in range(1000):
        n = 1 + next_random() % 20
        land = [1, 3, 10, 30, 60, 90, 99][next_random() % 7]
        d = solve(random_grid(n, land))
        total += d
        check = (check * 31 + d + 1) % 1000000007
    print(f"1000 random grids: total {total}, checksum {check}")
    corner = [[0] * 100 for _ in range(100)]
    corner[0][0] = 1
    print(f"100 by 100, a corner: {solve(corner)}")
    middle = [[0] * 100 for _ in range(100)]
    middle[50][50] = 1
    print(f"100 by 100, the middle: {solve(middle)}")
    sparse = [[1 if next_random() % 500 == 0 else 0 for _ in range(100)] for _ in range(100)]
    print(f"100 by 100, sparse: {solve(sparse)}")


if __name__ == "__main__":
    main(max_distance)
