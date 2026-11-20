# LeetCode #2397: Maximum Rows Covered by Columns -- a Python mirror of
# the ★ arm: each row as the mask of its 1s, every mask of numSelect
# columns tried. Prints the same output as rows.kara.

seed = 0


def maximum_rows(matrix, num_select):
    n = len(matrix[0])
    masks = []
    for row in matrix:
        mask = 0
        for c in range(n):
            if row[c] == 1:
                mask |= 1 << c
        masks.append(mask)
    best = 0
    for chosen in range(1 << n):
        if bin(chosen).count("1") != num_select:
            continue
        covered = sum(1 for mask in masks if mask & chosen == mask)
        best = max(best, covered)
    return best


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def grid(m, n, odds):
    return [[1 if next_random() % odds == 0 else 0 for _ in range(n)] for _ in range(m)]


def main():
    global seed
    print(maximum_rows([[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 0, 1]], 2))
    print(maximum_rows([[1], [0]], 1))
    print(f"{maximum_rows([[0, 0], [0, 0]], 1)} {maximum_rows([[1, 1], [0, 1]], 2)} {maximum_rows([[1, 1, 1], [1, 0, 0]], 2)}")
    seed = 2397
    sparse = grid(12, 12, 5)
    dense = grid(12, 12, 2)
    check = 0
    for k in range(1, 13):
        check = (check * 31 + maximum_rows(sparse, k)) % 1000000007
        check = (check * 31 + maximum_rows(dense, k)) % 1000000007
    print(f"12 by 12, every choice: checksum {check}")
    check = 0
    total = 0
    for _ in range(2000):
        m = 1 + next_random() % 8
        n = 1 + next_random() % 8
        odds = 1 + next_random() % 4
        matrix = grid(m, n, odds)
        k = 1 + next_random() % n
        rows = maximum_rows(matrix, k)
        check = (check * 31 + rows) % 1000000007
        total += rows
    print(f"2000 grids: checksum {check}, {total} rows covered")


if __name__ == "__main__":
    main()
