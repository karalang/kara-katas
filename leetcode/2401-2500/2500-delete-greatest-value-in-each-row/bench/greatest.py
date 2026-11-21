# LeetCode #2500: Delete Greatest Value in Each Row -- benchmark mirror of
# the ★ arm (greatest.kara): 1000 grids of 50 by 50, built once, then the
# passes; each sets one cell of every grid from the checksum so far,
# asks, and puts it back.


def delete_greatest_value(grid):
    rows = [sorted(row) for row in grid]
    total = 0
    for j in range(len(rows[0])):
        most = 0
        for row in rows:
            most = max(most, row[j])
        total += most
    return total


seed = 2500


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    passes = 32
    grids = [[[next_random() % 100 + 1 for _ in range(50)] for _ in range(50)] for _ in range(1000)]
    check = 0
    for p in range(passes):
        for grid in grids:
            r = check % 50
            c = check // 50 % 50
            was = grid[r][c]
            grid[r][c] = (check + p) % 100 + 1
            check = (check * 31 + delete_greatest_value(grid) + p) % 1000000007
            grid[r][c] = was
    print(f"{passes} passes over 1000 grids of 50 by 50: checksum {check}")


main()
