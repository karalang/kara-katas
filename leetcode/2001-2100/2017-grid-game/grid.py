# LeetCode #2017: Grid Game -- a mirror of the ★ arm, grid.kara.


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


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


def random_grid(n, top):
    grid = []
    for _ in range(2):
        row = []
        for _ in range(n):
            hi = next_random()
            row.append((hi * 32768 + next_random()) % top + 1)
        grid.append(row)
    return grid


def show(grid):
    return "[" + ", ".join("[" + ", ".join(map(str, row)) + "]" for row in grid) + "]"


def main():
    examples = [
        [[2, 5, 4], [1, 5, 1]],
        [[3, 3, 1], [8, 5, 2]],
        [[1, 3, 1, 15], [1, 3, 3, 1]],
        [[7], [9]],
        [[1, 100000], [100000, 1]],
        [[5, 5, 5, 5], [5, 5, 5, 5]],
        [[20, 3, 20, 17, 2, 12, 15, 17, 4, 15], [20, 10, 13, 14, 15, 5, 2, 3, 14, 3]],
    ]
    for grid in examples:
        print(f"{show(grid)} -> {grid_game(grid)}")
    total = check = 0
    for _ in range(3000):
        n = next_random() % 12 + 1
        top = next_random() % 20 + 1
        answer = grid_game(random_grid(n, top))
        total += answer
        check = mix(check, answer)
    print(f"3000 grids of 1 to 12 columns: sum {total}, checksum {check}")
    total = check = 0
    for a in range(4):
        n = [3000, 3000, 1000, 2][a]
        top = [100000, 3, 100000, 100000][a]
        answer = grid_game(random_grid(n, top))
        total += answer
        check = mix(check, answer)
    print(f"4 grids of up to 3000 columns: sum {total}, checksum {check}")


main()
