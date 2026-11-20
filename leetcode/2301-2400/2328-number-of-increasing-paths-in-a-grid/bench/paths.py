# LeetCode #2328: Number of Increasing Paths in a Grid -- the bench, the ★
# arm in Python. The cells sorted by value, largest first, and each
# cell's count of paths one plus its larger neighbours' counts, all of
# them already done. O(m n log(m n)).

MOD = 1000000007


def count_paths(grid):
    m, n = len(grid), len(grid[0])
    cells = [(grid[r][c], r, c) for r in range(m) for c in range(n)]
    cells.sort()
    cells.reverse()
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


def main():
    seed = 2328

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    grids = []
    for _ in range(10):
        grids.append([[next_random() % 1000 + 1 for _ in range(400)] for _ in range(250)])
    check = 0
    for p in range(3):
        for k in range(10):
            check = (check * 31 + count_paths(grids[k]) + p) % 1000000007
    print(f"3 passes over 10 grids of 10^5 cells: checksum {check}")


main()
