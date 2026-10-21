# LeetCode #840: Magic Squares In Grid -- Python mirror of the ★ arm and its harness.


def is_magic(grid, r, c):
    if grid[r + 1][c + 1] != 5:
        return False
    mask = 0
    for i in range(r, r + 3):
        for j in range(c, c + 3):
            v = grid[i][j]
            if v < 1 or v > 9:
                return False
            mask |= 1 << v
    if mask != 1022:
        return False
    for k in range(3):
        if grid[r + k][c] + grid[r + k][c + 1] + grid[r + k][c + 2] != 15:
            return False
        if grid[r][c + k] + grid[r + 1][c + k] + grid[r + 2][c + k] != 15:
            return False
    return grid[r][c] + grid[r + 2][c + 2] == 10 and grid[r][c + 2] + grid[r + 2][c] == 10


def num_magic_squares_inside(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    for r in range(rows - 2):
        for c in range(cols - 2):
            if is_magic(grid, r, c):
                count += 1
    return count


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def oriented(turn):
    return turned_square([[4, 9, 2], [3, 5, 7], [8, 1, 6]], turn)


def turned_square(base, turn):
    out = []
    for i in range(3):
        row = []
        for j in range(3):
            a = i
            b = 2 - j if turn >= 4 else j
            for _ in range(turn % 4):
                a, b = 2 - b, a
            row.append(base[a][b])
        out.append(row)
    return out


def random_grid(rows, cols, plants):
    grid = [[next_random() % 16 for _ in range(cols)] for _ in range(rows)]
    if rows < 3 or cols < 3:
        return grid
    for _ in range(plants):
        turn = next_random() % 8
        kind = next_random() % 6
        square = turned_square([[1, 5, 9], [6, 7, 2], [8, 3, 4]], turn) if kind == 5 else oriented(turn)
        shift = [-1, 1, 2, 6][next_random() % 4] if kind == 1 else 0
        swap_a = next_random() % 9
        swap_b = next_random() % 9
        r = next_random() % (rows - 2)
        c = next_random() % (cols - 2)
        for i in range(3):
            for j in range(3):
                k = 3 * i + j
                if kind == 3:
                    k = swap_b if k == swap_a else swap_a if k == swap_b else k
                grid[r + i][c + j] = 5 if kind == 2 else square[k // 3][k % 3] + shift
        if kind == 4:
            grid[r + 1][c + 1] = next_random() % 16
    return grid


def show(grid):
    print(f"{grid} -> {num_magic_squares_inside(grid)}")


def main():
    global seed
    show([[4, 3, 8, 4], [9, 5, 1, 9], [2, 7, 6, 2]])
    show([[8]])
    show([[4, 9, 2], [3, 5, 7], [8, 1, 6]])
    show([[2, 9, 4], [7, 5, 3], [6, 1, 8]])
    show([[5, 5, 5], [5, 5, 5], [5, 5, 5]])
    show([[5, 10, 3], [4, 6, 8], [9, 2, 7]])
    show([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    show([[9, 4, 2], [3, 5, 7], [8, 1, 6]])
    show([[4, 9, 2, 9, 4], [3, 5, 7, 5, 3], [8, 1, 6, 1, 8]])
    show([[4, 9, 2], [3, 5, 7]])
    show([[5], [5], [5]])
    show([[0, 0, 0, 0], [0, 8, 1, 6], [0, 3, 5, 7], [0, 4, 9, 2]])
    row_of_eight = [[], [], []]
    for turn in range(8):
        square = oriented(turn)
        for i in range(3):
            row_of_eight[i].extend(square[i])
    show(row_of_eight)
    seed = 840
    for plants in [4, 12, 40]:
        grid = random_grid(10, 10, plants)
        check = 0
        for row in grid:
            for v in row:
                check = (check * 31 + v) % 1000000007
        print(f"10 by 10, {plants} squares stamped: {num_magic_squares_inside(grid)} magic, grid checksum {check}")
    total = 0
    check = 0
    for _ in range(300):
        rows = 1 + next_random() % 10
        cols = 1 + next_random() % 10
        plants = next_random() % 6
        count = num_magic_squares_inside(random_grid(rows, cols, plants))
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"300 random grids: {total} magic, checksum {check}")


main()
