# LeetCode #1139: Largest 1-Bordered Square -- the mirror of the ★ arm:
# runs of 1s left and up, each corner's sides tried from the longest down.


def largest1_bordered_square(grid):
    rows, cols = len(grid), len(grid[0])
    left = [[0] * cols for _ in range(rows)]
    up = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                left[i][j] = left[i][j - 1] + 1 if j > 0 else 1
                up[i][j] = up[i - 1][j] + 1 if i > 0 else 1
    best = 0
    for i in range(rows):
        for j in range(cols):
            k = min(left[i][j], up[i][j])
            while k > best:
                if left[i - k + 1][j] >= k and up[i][j - k + 1] >= k:
                    best = k
                k -= 1
    return best * best


seed = 1139


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(rows, cols, ones):
    return [[1 if next_random() % 100 < ones else 0 for _ in range(cols)] for _ in range(rows)]


def frame(grid, top, left, size):
    for k in range(size):
        grid[top][left + k] = 1
        grid[top + size - 1][left + k] = 1
        grid[top + k][left] = 1
        grid[top + k][left + size - 1] = 1


def main():
    f = largest1_bordered_square
    print(f"example 1: {f([[1, 1, 1], [1, 0, 1], [1, 1, 1]])}")
    print(f"example 2: {f([[1, 1, 0, 0]])}")
    print(f"one 1: {f([[1]])}")
    print(f"one 0: {f([[0]])}")
    print(f"all 0: {f([[0, 0, 0], [0, 0, 0]])}")
    print(f"a column: {f([[1], [1], [1]])}")
    print(f"solid 3 by 4: {f([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])}")
    print(f"broken border: {f([[1, 1, 1], [1, 1, 0], [1, 1, 1]])}")
    nested = [[0] * 7 for _ in range(7)]
    frame(nested, 0, 0, 7)
    nested[6][3] = 0
    frame(nested, 1, 2, 4)
    print(f"a frame of 4 in a broken frame of 7: {f(nested)}")
    total = check = 0
    for i in range(2000):
        rows = next_random() % 12 + 1
        cols = next_random() % 12 + 1
        ones = [50, 70, 90][i % 3]
        grid = random_grid(rows, cols, ones)
        if i % 4 == 3:
            size = next_random() % min(rows, cols) + 1
            top = next_random() % (rows - size + 1)
            left = next_random() % (cols - size + 1)
            frame(grid, top, left, size)
        area = f(grid)
        total += area
        check = (check * 131 + area + 1) % 1000000007
    print(f"2000 random grids: areas total {total}, checksum {check}")
    print(f"100 by 100, all 1: {f([[1] * 100 for _ in range(100)])}")
    print(f"100 by 100, 90 in 100: {f(random_grid(100, 100, 90))}")
    print(f"100 by 100, 0 on the diagonal: {f([[0 if i == j else 1 for j in range(100)] for i in range(100)])}")


main()
