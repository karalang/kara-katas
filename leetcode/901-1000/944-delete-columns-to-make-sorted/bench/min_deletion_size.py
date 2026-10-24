# Benchmark: LeetCode #944 Delete Columns to Make Sorted -- the ★ arm,
# column by column, on grids of 100 rows of 1000 letters, LeetCode's
# largest. Mirrors min_deletion_size.kara, .c, .rs and go-seq/.


def min_deletion_size(strs):
    rows = [s.encode() for s in strs]
    n = len(rows)
    m = len(rows[0])
    deleted = 0
    for c in range(m):
        r = 1
        while r < n and rows[r - 1][c] <= rows[r][c]:
            r += 1
        if r < n:
            deleted += 1
    return deleted


seed = 944


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n, m = 150, 20, 100, 1000
    grids = []
    for _ in range(count):
        columns = []
        for _ in range(m):
            column = [next_random() % 26 + 97 for _ in range(n)]
            column.sort()
            if next_random() % 2 == 0:
                a = next_random() % n
                b = next_random() % n
                column[a], column[b] = column[b], column[a]
            columns.append(column)
        grids.append(["".join(chr(columns[c][r]) for c in range(m)) for r in range(n)])
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            d = min_deletion_size(grids[(r + i) % count])
            total += d
            check = (check * 1000003 + d * (i + 1)) % 1000000007
    print(f"{rounds} rounds over {count} grids of {n} rows of {m} letters: {total} deleted, checksum {check}")


main()
