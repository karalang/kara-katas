# LeetCode #2373: Largest Local Values in a Matrix -- the Python mirror of
# the ★ arm: each cell of the answer is the largest of the nine values in
# the 3 x 3 block whose top left corner it names.


def largest_local(grid):
    n = len(grid)
    out = []
    for i in range(n - 2):
        row = []
        for j in range(n - 2):
            most = 0
            for di in range(3):
                for dj in range(3):
                    most = max(most, grid[i + di][j + dj])
            row.append(most)
        out.append(row)
    return out


SEED = [2373]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def show(grid):
    return "[" + " / ".join(",".join(str(v) for v in row) for row in grid) + "]"


def fold(check, grid):
    for row in grid:
        for v in row:
            check = (check * 31 + v) % 1000000007
    return check


def main():
    # LeetCode's two examples; a 3 x 3 grid; a 100 x 100 grid of
    # (i j) % 100 + 1 and one of 100 - (i + j) % 100; then 1000 random
    # grids of 3 x 3 to 12 x 12 with values from 1 to 1 to 100
    print(show(largest_local([[9, 9, 8, 1], [5, 6, 2, 6], [8, 2, 6, 4], [6, 2, 2, 2]])))
    print(show(largest_local([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 2, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]])))
    print(show(largest_local([[1, 2, 3], [4, 5, 6], [7, 8, 9]])))
    product = [[(i * j) % 100 + 1 for j in range(100)] for i in range(100)]
    falling = [[100 - (i + j) % 100 for j in range(100)] for i in range(100)]
    print(f"{fold(0, largest_local(product))} {fold(0, largest_local(falling))}")
    check = 0
    flat = 0
    for _ in range(1000):
        n = 3 + next_random() % 10
        top = 1 + next_random() % 100
        grid = [[1 + next_random() % top for _ in range(n)] for _ in range(n)]
        out = largest_local(grid)
        check = fold(check, out)
        if all(v == out[0][0] for row in out for v in row):
            flat += 1
    print(f"1000 grids: checksum {check}, {flat} with one value throughout")


main()
