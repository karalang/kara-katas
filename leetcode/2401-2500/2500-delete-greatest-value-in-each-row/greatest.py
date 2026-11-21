# LeetCode #2500: Delete Greatest Value in Each Row -- Python mirror of the
# ★ arm (greatest.kara): every row sorted, each column's greatest added.


def delete_greatest_value(grid):
    rows = [sorted(row) for row in grid]
    total = 0
    for j in range(len(rows[0])):
        most = 0
        for row in rows:
            most = max(most, row[j])
        total += most
    return total


# ---- test harness -----------------------------------------------------------

seed = 2500


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(m, n, top):
    return [[next_random() % top + 1 for _ in range(n)] for _ in range(m)]


def main():
    cases = [
        [[1, 2, 4], [3, 3, 1]],
        [[10]],
        [[1], [100], [7]],
        [[5, 1, 3, 2, 4]],
        [[1, 1], [1, 1]],
        [[100, 1], [1, 100]],
        [[9, 8, 7], [1, 2, 3], [4, 6, 5]],
        [[2, 50, 2, 50], [49, 3, 49, 3]],
    ]
    for grid in cases:
        print(f"{len(grid)} by {len(grid[0])} -> {delete_greatest_value(grid)}")
    for top in (100, 3):
        check = 0
        for _ in range(2000):
            m = next_random() % 12 + 1
            n = next_random() % 12 + 1
            check = (check * 31 + delete_greatest_value(random_grid(m, n, top))) % 1000000007
        print(f"2000 random to {top}: checksum {check}")
    hundreds = [[100] * 50 for _ in range(50)]
    turned = [[(c + r) % 50 + 1 for c in range(50)] for r in range(50)]
    print(f"50 by 50 hundreds -> {delete_greatest_value(hundreds)}")
    print(f"50 by 50 turned -> {delete_greatest_value(turned)}")
    check = 0
    for _ in range(20):
        check = (check * 31 + delete_greatest_value(random_grid(50, 50, 100))) % 1000000007
    print(f"20 random 50 by 50: checksum {check}")


if __name__ == "__main__":
    main()
