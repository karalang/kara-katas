# LeetCode #883: Projection Area of 3D Shapes -- Python mirror of the
# one-pass solution in projection_area.kara, with the same test harness.
#
# Seen from above, every cell holding a tower shows one square. Seen from
# the front, each row shows a column of squares as high as its tallest
# tower, and from the side each column of the grid the same. Reading
# grid[i][j] and grid[j][i] in the same loop gives row i's tallest tower
# and column i's together, so one pass over the grid adds up all three
# views. O(n^2).


def projection_area(grid):
    n = len(grid)
    area = 0
    for i in range(n):
        row = 0
        column = 0
        for j in range(n):
            if grid[i][j] > 0:
                area += 1
            row = max(row, grid[i][j])
            column = max(column, grid[j][i])
        area += row + column
    return area


# ---- test harness ----------------------------------------------------------


def text(grid):
    n = len(grid)
    if n > 3:
        cubes = sum(sum(row) for row in grid)
        return f"{n} x {n} grid of {cubes} cubes"
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]" for row in grid) + "]"


def show(grid):
    print(f"grid = {text(grid)} -> {projection_area(grid)}")


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# an n x n grid of towers 0 to most - 1 high, a quarter of the cells empty
def random_grid(n, most):
    grid = []
    for _ in range(n):
        row = []
        for _ in range(n):
            if next_random() % 4 == 0:
                row.append(0)
            else:
                row.append(next_random() % most)
        grid.append(row)
    return grid


def filled(n, cell):
    return [[cell(i, j) for j in range(n)] for i in range(n)]


def main():
    global seed
    show([[1, 2], [3, 4]])
    show([[2]])
    show([[1, 0], [0, 2]])
    show([[0]])
    show([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    show([[2, 2, 2], [2, 1, 2], [2, 2, 2]])
    show([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    show(filled(50, lambda i, j: 50))
    show(filled(50, lambda i, j: 50 if i == 49 and j == 0 else 0))
    show(filled(50, lambda i, j: (i * j) % 51))
    # small cases
    seed = 883
    total = 0
    for _ in range(3000):
        n = next_random() % 8 + 1
        total += projection_area(random_grid(n, 10))
    print(f"3000 grids of up to 8 x 8: area {total}")
    # LeetCode's sizes: n up to 50, towers up to 50
    total = 0
    check = 0
    for _ in range(1000):
        n = next_random() % 50 + 1
        area = projection_area(random_grid(n, 51))
        total += area
        check = (check * 131 + area) % 1000000007
    print(f"1000 grids of up to 50 x 50: area {total}, checksum {check}")


main()
