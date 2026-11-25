# LeetCode #1351 bench -- Python: a staircase walk from the bottom-left
# corner.


def count_negatives(grid):
    n = len(grid[0])
    row = len(grid) - 1
    col = 0
    count = 0
    while row >= 0 and col < n:
        if grid[row][col] < 0:
            count += n - col
            row -= 1
        else:
            col += 1
    return count


def main():
    seed = 1351
    grids = []
    for _ in range(50):
        grid = []
        for i in range(100):
            row = []
            for j in range(100):
                v = 60
                if i > 0:
                    v = min(v, grid[i - 1][j])
                if j > 0:
                    v = min(v, row[j - 1])
                if i + j > 0:
                    seed = (seed * 1103515245 + 12345) % 2147483648
                    v -= (seed // 65536) % 2
                row.append(max(v, -100))
            grid.append(row)
        grids.append(grid)
    check = 0
    for r in range(300000):
        k = check % 50
        i = (check // 50) % 100
        j = (check // 5000) % 100
        g = grids[k]
        if check % 2 == 0:
            v = 100
            if i > 0:
                v = min(v, g[i - 1][j])
            if j > 0:
                v = min(v, g[i][j - 1])
        else:
            v = -100
            if i < 99:
                v = max(v, g[i + 1][j])
            if j < 99:
                v = max(v, g[i][j + 1])
        g[i][j] = v
        check = (check * 31 + count_negatives(g) + r) % 1000000007
    print(f"300000 rounds over 50 grids of 100 by 100: checksum {check}")


main()
