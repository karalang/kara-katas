# LeetCode #2304: Minimum Path Cost in a Grid -- the ★ arm in Python.
# Row by row: best[j] is the least cost of a path ending at column j of
# the row so far, and each column of the next row takes the least of
# best[k] plus the cost of moving from the value at column k to it, plus
# its own value. O(m n^2).


def min_path_cost(grid, move_cost):
    n = len(grid[0])
    best = list(grid[0])
    for r in range(1, len(grid)):
        nxt = [0] * n
        for j in range(n):
            nxt[j] = min(best[k] + move_cost[grid[r - 1][k]][j] for k in range(n)) + grid[r][j]
        best = nxt
    return min(best)


seed = 2304


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def make(m, n, most):
    values = list(range(m * n))
    for i in range(m * n - 1, 0, -1):
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    grid = [values[r * n:(r + 1) * n] for r in range(m)]
    move_cost = [[next_random() % most + 1 for _ in range(n)] for _ in range(m * n)]
    return grid, move_cost


def main():
    print(min_path_cost([[5, 3], [4, 0], [2, 1]], [[9, 8], [1, 5], [10, 12], [18, 6], [2, 4], [14, 3]]))
    print(min_path_cost([[5, 1, 2], [4, 0, 3]], [[12, 10, 15], [20, 23, 8], [21, 7, 1], [8, 1, 13], [9, 10, 25], [5, 3, 2]]))
    print(min_path_cost([[0, 1], [2, 3]], [[1, 1], [1, 1], [1, 1], [1, 1]]))
    print(min_path_cost([[3, 0, 1], [2, 4, 5]], [[100, 100, 100], [100, 100, 100], [100, 100, 100], [100, 100, 1], [100, 100, 100], [100, 100, 100]]))
    grid, move_cost = make(50, 50, 100)
    print(min_path_cost(grid, move_cost))
    check = 0
    total = 0
    for _ in range(1000):
        m = next_random() % 7 + 2
        n = next_random() % 7 + 2
        grid, move_cost = make(m, n, 100)
        cost = min_path_cost(grid, move_cost)
        check = (check * 31 + cost) % 1000000007
        total += cost
    print(f"1000 grids: checksum {check}, {total} in all")


main()
