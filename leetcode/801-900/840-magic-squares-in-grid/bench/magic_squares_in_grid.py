# Benchmark for #840: Magic Squares In Grid -- the ★ arm (the centre first).
#
# Mirrors magic_squares_in_grid.kara: each 3 by 3 window is looked at
# only if its centre is 5; then its nine numbers must be 1 to 9, each
# once, kept as bits of a mask, its rows and columns must add up to 15,
# and each diagonal's two corners to 10.


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


seed = 840


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 64 grids drawn once, each LeetCode's largest, 10 by 10, of numbers
    # 0 to 15 with 12 squares of 3 by 3 stamped on it: the Lo Shu turned
    # or mirrored, a square of 5s, or the Lo Shu with 1 added to every
    # number. Each round changes one cell of the next grid and counts its
    # magic squares.
    count = 64
    rounds = 14000000
    lo_shu = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
    grids = []
    for _ in range(count):
        grid = [[next_random() % 16 for _ in range(10)] for _ in range(10)]
        for _ in range(12):
            turn = next_random() % 8
            kind = next_random() % 3
            r = next_random() % 8
            c = next_random() % 8
            for i in range(3):
                for j in range(3):
                    a = i
                    b = 2 - j if turn >= 4 else j
                    for _ in range(turn % 4):
                        a, b = 2 - b, a
                    grid[r + i][c + j] = 5 if kind == 1 else lo_shu[a][b] + kind // 2
        grids.append(grid)
    total = 0
    checksum = 0
    for round in range(rounds):
        g = round % count
        cell = round * 7 % 100
        grids[g][cell // 10][cell % 10] = round % 16
        magic = num_magic_squares_inside(grids[g])
        total += magic
        checksum = (checksum * 31 + magic + round) % 1000000007
    print(f"{rounds} rounds of {count} grids: {total} magic squares, checksum {checksum}")


main()
