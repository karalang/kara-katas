# LeetCode #883 bench: Python mirror of projection_area.kara (the ★ arm,
# one pass over rows and columns together) on the same 100 grids.


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


seed = 883


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    total = 0
    check = 0
    for _ in range(100):
        # a grid of 40 x 40 to 50 x 50, towers up to 50, a quarter empty
        n = 40 + next_random() % 11
        grid = []
        for _ in range(n):
            row = []
            for _ in range(n):
                if next_random() % 4 == 0:
                    row.append(0)
                else:
                    row.append(next_random() % 51)
            grid.append(row)
        # 1000 towers rebuilt one at a time, the area after each
        for _ in range(1000):
            i = next_random() % n
            j = next_random() % n
            grid[i][j] = next_random() % 51
            area = projection_area(grid)
            total += area
            check = (check * 131 + area) % 1000000007
    print(f"100 grids, 1000 towers rebuilt in each: area {total}, checksum {check}")


main()
