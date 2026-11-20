# LeetCode #2328: Number of Increasing Paths in a Grid -- the Python
# mirror of the ★ arm: the cells sorted by value, largest first, each
# cell's count of paths one plus its larger neighbours' counts.

MOD = 1000000007


def count_paths(grid):
    m, n = len(grid), len(grid[0])
    cells = sorted(((grid[r][c], r, c) for r in range(m) for c in range(n)), reverse=True)
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    paths_from = [[1] * n for _ in range(m)]
    total = 0
    for value, r, c in cells:
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] > value:
                paths_from[r][c] = (paths_from[r][c] + paths_from[nr][nc]) % MOD
        total = (total + paths_from[r][c]) % MOD
    return total


seed = 2328


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(m, n, top):
    return [[next_random() % top + 1 for _ in range(n)] for _ in range(m)]


def main():
    print(count_paths([[1, 1], [3, 4]]))
    print(count_paths([[1], [2]]))
    print(count_paths([[5]]))
    print(count_paths([[7] * 3 for _ in range(3)]))
    print(count_paths([list(range(1, 11))]))
    print(f"300 by 300: {count_paths(random_grid(300, 300, 100))}")
    check = 0
    total = 0
    for _ in range(1000):
        m = next_random() % 6 + 1
        n = next_random() % 6 + 1
        paths = count_paths(random_grid(m, n, 5))
        check = (check * 31 + paths) % 1000000007
        total = (total + paths) % 1000000007
    print(f"1000 grids: checksum {check}, total {total}")


main()
