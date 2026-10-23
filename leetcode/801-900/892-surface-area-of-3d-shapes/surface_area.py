# LeetCode #892: Surface Area of 3D Shapes -- Python mirror of the
# six-faces-less-shared solution in surface_area.kara, with the same test
# harness.
#
# Each cube has 6 faces, and every face two cubes share hides both of
# theirs. A tower of v cubes shares v - 1 faces inside it, so it shows
# 4v + 2; two towers side by side share as many faces as the shorter
# is tall. Count each tower, then take away twice the shorter of each
# pair of neighbours, right and down so each pair is seen once. O(n^2).


def surface_area(grid):
    n = len(grid)
    area = 0
    for i in range(n):
        for j in range(n):
            v = grid[i][j]
            if v > 0:
                area += 4 * v + 2
            if i + 1 < n:
                area -= 2 * min(v, grid[i + 1][j])
            if j + 1 < n:
                area -= 2 * min(v, grid[i][j + 1])
    return area


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(grid):
    text = "[" + ", ".join("[" + ", ".join(map(str, row)) + "]" for row in grid) + "]"
    print(f"grid = {text} -> {surface_area(grid)}")


def main():
    global seed
    show([[1, 2], [3, 4]])
    show([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    show([[2, 2, 2], [2, 1, 2], [2, 2, 2]])
    show([[0]])
    show([[50]])
    show([[0, 3], [3, 0]])
    # random grids of LeetCode's sizes: up to 50 by 50, towers up to 50
    # high, or, a third of the time, up to 3 high with a cell in three
    # empty
    seed = 892
    cubes = 0
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 50
        low = next_random() % 3 == 0
        grid = []
        for _ in range(n):
            row = []
            for _ in range(n):
                if low:
                    v = 0 if next_random() % 3 == 0 else 1 + next_random() % 3
                else:
                    v = next_random() % 51
                cubes += v
                row.append(v)
            grid.append(row)
        got = surface_area(grid)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"300 grids of up to 50 by 50 ({cubes} cubes): surface area {total}, checksum {check}")


main()
