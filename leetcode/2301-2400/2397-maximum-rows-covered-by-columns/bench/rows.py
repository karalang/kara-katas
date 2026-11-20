# LeetCode #2397: Maximum Rows Covered by Columns -- the bench, the ★ arm
# in Python: each row as the mask of its 1s, every mask of numSelect
# columns tried.

seed = 2397


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
        covered = 0
        for mask in masks:
            if mask & chosen == mask:
                covered += 1
        best = max(best, covered)
    return best


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def grid(m, n, odds):
    return [[1 if next_random() % odds == 0 else 0 for _ in range(n)] for _ in range(m)]


def main():
    grids = [grid(12, 12, 2 + g % 4) for g in range(200)]
    check = 0
    for p in range(10):
        for g in grids:
            for k in range(1, 13):
                check = (check * 31 + maximum_rows(g, k) + p) % 1000000007
    print(f"10 passes over 200 grids of 12 by 12, every choice: checksum {check}")


if __name__ == "__main__":
    main()
