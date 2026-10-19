# LeetCode 764 — Largest Plus Sign: the ★ arm in Python, same output.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_mines(n, count):
    taken = set()
    mines = []
    while len(mines) < count:
        r = next_random() % n
        c = next_random() % n
        if r * n + c not in taken:
            taken.add(r * n + c)
            mines.append([r, c])
    return mines


def show(n, mines):
    print(f"n = {n}, mines {mines} -> {order_of_largest_plus_sign(n, mines)}")


def main():
    global seed
    show(5, [[4, 2]])
    show(1, [[0, 0]])
    show(2, [[0, 0]])
    show(3, [[0, 0]])
    show(3, [[1, 1]])
    show(10, [[0, 0]])
    show(4, [[0, 1], [1, 3], [2, 0], [3, 2]])
    show(500, [[0, 0], [249, 250], [499, 499]])
    seed = 764
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 60
        count = 1 + next_random() % (n * n // 4 + 1)
        order = order_of_largest_plus_sign(n, random_mines(n, count))
        total += order
        check = (check * 31 + order) % 1000000007
    print(f"300 random grids: orders adding up to {total}, checksum {check}")


main()
