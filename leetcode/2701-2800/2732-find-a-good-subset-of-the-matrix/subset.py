# LeetCode #2732: Find a Good Subset of the Matrix -- Python mirror of
# subset.kara (the ★ arm): a row of zeros alone, or the first rows of two
# disjoint masks of the 32.


def good_subsetof_binary_matrix(grid):
    first = [-1] * 32
    for i, row in enumerate(grid):
        mask = 0
        for j, x in enumerate(row):
            mask |= x << j
        if mask == 0:
            return [i]
        if first[mask] < 0:
            first[mask] = i
    for a in range(1, 32):
        for b in range(a + 1, 32):
            if a & b == 0 and first[a] >= 0 and first[b] >= 0:
                return [min(first[a], first[b]), max(first[a], first[b])]
    return []


seed = 2732


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(m, n, kind):
    column = next_random() % n
    free = next_random() % m
    grid = []
    for r in range(m):
        row = [next_random() % 2 for _ in range(n)]
        if kind == 1 or (kind == 2 and r != free):
            row[column] = 1
        grid.append(row)
    return grid


def is_good(grid, rows):
    for k in range(len(rows)):
        if rows[k] < 0 or rows[k] >= len(grid) or (k > 0 and rows[k] <= rows[k - 1]):
            return False
    for j in range(len(grid[0])):
        if 2 * sum(grid[r][j] for r in rows) > len(rows):
            return False
    return True


def main():
    print(good_subsetof_binary_matrix([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 1, 1]]))
    print(good_subsetof_binary_matrix([[0]]))
    print(good_subsetof_binary_matrix([[1, 1, 1], [1, 1, 1]]))
    found = bad = check = 0
    for c in range(3030):
        if c < 3000:
            m = next_random() % 10 + 1
            n = next_random() % 5 + 1
        else:
            m, n = 1000, 5
        grid = random_grid(m, n, c % 3)
        rows = good_subsetof_binary_matrix(grid)
        exists = 1 if rows else 0
        if exists and not is_good(grid, rows):
            bad += 1
        found += exists
        check = (check * 31 + exists) % 1000000007
        if c in (2999, 3029):
            count = "3000 small grids" if c == 2999 else "30 grids of 1000 rows"
            print(f"{count}: {found} with a good subset, {bad} named not good, checksum {check}")
            found = bad = check = 0


main()
