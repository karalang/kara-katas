# LeetCode #2022: Convert 1D Array Into 2D Array -- Python mirror of the ★ arm
# (convert.kara). Row `i` is the run `original[i * n:(i + 1) * n]` when the
# array holds exactly `m * n` values.


def construct_2d_array(original, m, n):
    if len(original) != m * n:
        return []
    return [original[i * n:(i + 1) * n] for i in range(m)]


# ---- test harness ----------------------------------------------------------

seed = 2022


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    if v and isinstance(v[0], list):
        return '[' + ', '.join(show(r) for r in v) + ']'
    return '[' + ', '.join(str(x) for x in v) + ']'


def fold_grid(grid, check):
    for row in grid:
        value = 0
        for v in row:
            value = (value * 100003 + v) % 1000000007
        check = (check * 31 + value) % 1000000007
    return check


def main():
    examples = [
        ([1, 2, 3, 4], 2, 2),
        ([1, 2, 3], 1, 3),
        ([1, 2], 1, 1),
        ([3], 1, 1),
        ([1, 2, 3, 4, 5, 6], 3, 2),
        ([1, 2, 3, 4, 5, 6], 2, 3),
        ([1, 2, 3, 4, 5, 6], 6, 1),
        ([1, 2, 3, 4, 5, 6], 4, 2),
    ]
    for original, m, n in examples:
        print(f"{show(original)}, {m}, {n} -> {show(construct_2d_array(original, m, n))}")
    built = 0
    check = 0
    for _ in range(3000):
        length = next_random() % 24 + 1
        original = [next_random() % 100000 + 1 for _ in range(length)]
        m = next_random() % 8 + 1
        if next_random() % 2 == 0 and length % m == 0:
            n = length // m
        else:
            n = next_random() % 8 + 1
        grid = construct_2d_array(original, m, n)
        if not grid:
            check = (check * 31 + 1000000006) % 1000000007
        else:
            built += 1
            check = fold_grid(grid, check)
    print(f"3000 arrays of up to 24 values: {built} built, checksum {check}")
    built = 0
    check = 0
    for a in range(5):
        m = [1, 50000, 200, 317, 1000][a]
        n = [50000, 1, 250, 157, 49][a]
        length = [50000, 50000, 50000, 49769, 50000][a]
        original = [next_random() % 100000 + 1 for _ in range(length)]
        grid = construct_2d_array(original, m, n)
        if not grid:
            check = (check * 31 + 1000000006) % 1000000007
        else:
            built += 1
            check = fold_grid(grid, check)
    print(f"5 arrays of up to 50000 values: {built} built, checksum {check}")


main()
