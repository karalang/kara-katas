# LeetCode #2732: Find a Good Subset of the Matrix -- the bench
# (subset.kara in Python): a row of zeros alone, or the first rows of two
# disjoint masks among the 32.


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


def main():
    grids, m, n, rounds = 100, 10000, 5, 10
    every = []
    for g in range(grids):
        kind = g % 3
        column = next_random() % n
        free = next_random() % m
        grid = []
        for r in range(m):
            row = [next_random() % 2 for _ in range(n)]
            if kind == 1 or (kind == 2 and r != free):
                row[column] = 1
            grid.append(row)
        every.append(grid)
    found = 0
    check = 0
    for r in range(rounds):
        for grid in every:
            rows = good_subsetof_binary_matrix(grid)
            if rows:
                found += 1
            check = (check * 31 + sum(rows) + len(rows) + r) % 1000000007
    print(f"{grids} grids of {m} rows, {rounds} rounds: {found} good subsets found, checksum {check}")


main()
