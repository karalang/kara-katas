# LeetCode #2132: Stamping the Grid -- the mirror of stamp.kara: a prefix
# sum of the occupied cells to fit each stamp, a difference table of the
# stamps laid down, and its prefix sum over every empty cell.


def possible_to_stamp(grid, stamp_height, stamp_width):
    m = len(grid)
    n = len(grid[0])
    w = n + 1
    full = [0] * ((m + 1) * w)
    for r in range(m):
        for c in range(n):
            full[(r + 1) * w + c + 1] = grid[r][c] + full[r * w + c + 1] + full[(r + 1) * w + c] - full[r * w + c]
    marks = [0] * ((m + 1) * w)
    for r in range(m - stamp_height + 1):
        for c in range(n - stamp_width + 1):
            r2 = r + stamp_height
            c2 = c + stamp_width
            if full[r2 * w + c2] - full[r * w + c2] - full[r2 * w + c] + full[r * w + c] == 0:
                marks[r * w + c] += 1
                marks[r * w + c2] -= 1
                marks[r2 * w + c] -= 1
                marks[r2 * w + c2] += 1
    for r in range(m):
        for c in range(n):
            if r > 0:
                marks[r * w + c] += marks[(r - 1) * w + c]
            if c > 0:
                marks[r * w + c] += marks[r * w + c - 1]
            if r > 0 and c > 0:
                marks[r * w + c] -= marks[(r - 1) * w + c - 1]
            if grid[r][c] == 0 and marks[r * w + c] == 0:
                return False
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def text(grid):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]" for row in grid) + "]"


def show(grid, h, w):
    print(f"{text(grid)} {h}x{w} -> {str(possible_to_stamp(grid, h, w)).lower()}")


def main():
    show([[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]], 4, 3)
    show([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], 2, 2)
    show([[1, 1], [1, 1]], 3, 3)
    show([[0]], 1, 1)
    show([[0]], 2, 1)
    show([[0, 0], [0, 0]], 2, 2)
    seed = [2132]
    yes = 0
    check = 0
    for rnd in range(2000):
        m = next_random(seed) % 6 + 1
        n = next_random(seed) % 6 + 1
        k = [2, 4, 8][rnd % 3]
        grid = []
        for _ in range(m):
            grid.append([1 if next_random(seed) % k == 0 else 0 for _ in range(n)])
        h = next_random(seed) % 4 + 1
        w = next_random(seed) % 4 + 1
        fits = possible_to_stamp(grid, h, w)
        if fits:
            yes += 1
        check = (check * 31 + (1 if fits else 0) + m * 7 + n) % 1000000007
    print(f"2000 grids: {yes} stamped, checksum {check}")
    empty = [[0] * 500 for _ in range(400)]
    line = [[1 if c % 1000 == 999 else 0 for c in range(200000)]]
    scattered = []
    for _ in range(400):
        scattered.append([1 if next_random(seed) % 200 == 0 else 0 for _ in range(500)])
    x = str(possible_to_stamp(empty, 400, 500)).lower()
    y = str(possible_to_stamp(line, 1, 999)).lower()
    z = str(possible_to_stamp(scattered, 2, 2)).lower()
    print(f"200000 cells: {x} empty, {y} in a line, {z} scattered")


main()
