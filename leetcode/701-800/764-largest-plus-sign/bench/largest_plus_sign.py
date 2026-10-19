# LeetCode 764 — Largest Plus Sign: benchmark, the ★ arm in Python.
# 300 random grids of 500 x 500 with 5,000 mines each.


def order_of_largest_plus_sign(n, mines):
    grid = [[n] * n for _ in range(n)]
    for r, c in mines:
        grid[r][c] = 0
    for i in range(n):
        left = right = up = down = 0
        for j in range(n):
            left = 0 if grid[i][j] == 0 else left + 1
            grid[i][j] = min(grid[i][j], left)
            k = n - 1 - j
            right = 0 if grid[i][k] == 0 else right + 1
            grid[i][k] = min(grid[i][k], right)
            up = 0 if grid[j][i] == 0 else up + 1
            grid[j][i] = min(grid[j][i], up)
            down = 0 if grid[k][i] == 0 else down + 1
            grid[k][i] = min(grid[k][i], down)
    return max(max(row) for row in grid)


def main():
    seed = 764

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    rounds = 300
    n = 500
    total = 0
    check = 0
    for _ in range(rounds):
        taken = [False] * (n * n)
        mines = []
        while len(mines) < 5000:
            r = next_random() % n
            c = next_random() % n
            if not taken[r * n + c]:
                taken[r * n + c] = True
                mines.append([r, c])
        order = order_of_largest_plus_sign(n, mines)
        total += order
        check = (check * 31 + order) % 1000000007
    print(f"{rounds} grids of 500 x 500 with 5000 mines: orders adding up to {total}, checksum {check}")


main()
