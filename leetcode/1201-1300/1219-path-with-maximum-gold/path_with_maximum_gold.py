# LeetCode #1219: Path with Maximum Gold -- the Python mirror of the ★ arm:
# a depth-first search from every cell with gold that zeroes a cell while
# the search goes on from it and puts its gold back on the way out.


def collect(grid, r, c):
    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or grid[r][c] == 0:
        return 0
    gold = grid[r][c]
    grid[r][c] = 0
    best = 0
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        best = max(best, collect(grid, r + dr, c + dc))
    grid[r][c] = gold
    return gold + best


def get_maximum_gold(grid):
    g = [row[:] for row in grid]
    best = 0
    for r in range(len(g)):
        for c in range(len(g[0])):
            if g[r][c] > 0:
                best = max(best, collect(g, r, c))
    return best


# ---- test harness -----------------------------------------------------------

seed = 1219


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(grid):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]" for row in grid) + "]"


def main():
    cases = [
        [[0, 6, 0], [5, 8, 7], [0, 9, 0]],
        [[1, 0, 7], [2, 0, 6], [3, 4, 5], [0, 3, 0], [9, 0, 20]],
        [[0]],
        [[5]],
        [[0, 0], [0, 0]],
        [[1, 1], [1, 1]],
        [[100, 0, 100], [0, 0, 0], [100, 0, 100]],
        [[1, 2, 3, 4, 5]],
    ]
    for grid in cases:
        print(f"{show(grid)}: {get_maximum_gold(grid)}")
    total = 0
    check = 0
    for _ in range(1000):
        rows = next_random() % 4 + 1
        cols = next_random() % 4 + 1
        grid = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                v = next_random() % 150
                row.append(0 if v < 50 else v - 49)
            grid.append(row)
        answer = get_maximum_gold(grid)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"1000 grids up to 4 by 4: gold total {total}, checksum {check}")
    scattered = [[0] * 15 for _ in range(15)]
    placed = 0
    while placed < 25:
        r = next_random() % 15
        c = next_random() % 15
        if scattered[r][c] == 0:
            scattered[r][c] = next_random() % 100 + 1
            placed += 1
    print(f"25 cells with gold scattered over 15 by 15: {get_maximum_gold(scattered)}")
    block = [[0] * 15 for _ in range(15)]
    for r in range(5, 10):
        for c in range(5, 10):
            block[r][c] = next_random() % 100 + 1
    print(f"a full 5 by 5 block of gold in 15 by 15: {get_maximum_gold(block)}")
    snake = [[0] * 15 for _ in range(15)]
    for c in range(15):
        snake[0][c] = next_random() % 100 + 1
    for r in range(1, 11):
        snake[r][14] = next_random() % 100 + 1
    print(f"25 cells of gold in one bent line: {get_maximum_gold(snake)}")
    apart = [[0] * 15 for _ in range(15)]
    for k in range(25):
        apart[(k // 5) * 3][(k % 5) * 3] = k + 1
    print(f"25 cells of gold, none next to another: {get_maximum_gold(apart)}")


main()
