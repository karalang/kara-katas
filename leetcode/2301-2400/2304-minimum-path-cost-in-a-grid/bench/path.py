# LeetCode #2304: Minimum Path Cost in a Grid -- the bench, the ★ arm in
# Python. Row by row, each column of the next row takes the least over
# the row before of the cost so far plus the move, plus its own value.

seed = 2304


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def min_path_cost(grid, move_cost):
    n = len(grid[0])
    best = list(grid[0])
    for r in range(1, len(grid)):
        above = grid[r - 1]
        row = grid[r]
        nxt = [0] * n
        for j in range(n):
            least = None
            for k in range(n):
                c = best[k] + move_cost[above[k]][j]
                if least is None or c < least:
                    least = c
            nxt[j] = least + row[j]
        best = nxt
    return min(best)


def main():
    grids = []
    tables = []
    for _ in range(20):
        values = list(range(2500))
        for i in range(2499, 0, -1):
            j = next_random() % (i + 1)
            values[i], values[j] = values[j], values[i]
        grids.append([values[r * 50:(r + 1) * 50] for r in range(50)])
        tables.append([[next_random() % 100 + 1 for _ in range(50)] for _ in range(2500)])
    check = 0
    for p in range(40):
        for a in range(20):
            check = (check * 31 + min_path_cost(grids[a], tables[(a + p) % 20])) % 1000000007
    print(f"40 passes over 20 grids of 50 by 50: checksum {check}")


main()
