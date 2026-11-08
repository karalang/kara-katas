# LeetCode #2017: Grid Game -- the ★ arm's benchmark, a mirror of grid.kara.


def grid_game(grid):
    top = sum(grid[0])
    bottom = 0
    best = 2**63 - 1
    for i in range(len(grid[0])):
        top -= grid[0][i]
        best = min(best, max(top, bottom))
        bottom += grid[1][i]
    return best


seed = 2017


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    grids = []
    for _ in range(200):
        grids.append([[next_random() * 3 % 100000 + 1 for _ in range(50000)] for _ in range(2)])
    calls = total = check = 0
    for _ in range(10):
        for grid in grids:
            answer = grid_game(grid)
            calls += 1
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
