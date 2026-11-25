# LeetCode #1351 -- Python mirror of the ★ arm: a staircase walk from the
# bottom-left corner.


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


seed = [1351]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def sorted_grid(m, n, top, step):
    grid = []
    for i in range(m):
        row = []
        for j in range(n):
            v = top
            if i > 0:
                v = min(v, grid[i - 1][j])
            if j > 0:
                v = min(v, row[j - 1])
            if i + j > 0:
                v -= next_random() % (step + 1)
            row.append(max(v, -100))
        grid.append(row)
    return grid


def main():
    e1 = count_negatives([[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]])
    e2 = count_negatives([[3, 2], [1, 0]])
    neg = count_negatives([[-5]])
    zero = count_negatives([[0]])
    all_ = count_negatives([[-1, -2], [-3, -4], [-5, -6]])
    big = sorted_grid(100, 100, 100, 2)
    print(e1, e2, neg, zero, all_, count_negatives(big))
    total = 0
    check = 0
    for c in range(2000):
        small = c % 10 != 0
        m = 1 + next_random() % (6 if small else 30)
        n = 1 + next_random() % (6 if small else 30)
        top = next_random() % 36 - 5
        step = 1 if c % 3 == 0 else 3 if c % 3 == 1 else 20
        got = count_negatives(sorted_grid(m, n, top, step))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random grids: {total} negatives in all, checksum {check}")


main()
