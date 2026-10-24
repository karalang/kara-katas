# LeetCode #944: Delete Columns to Make Sorted -- column by column.
# Mirrors min_deletion_size.kara (the ★ arm) and its harness.


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


def random_grid(n, m, letters):
    strs = []
    for _ in range(n):
        strs.append("".join(chr(next_random() % letters + 97) for _ in range(m)))
    return strs


def shape(strs):
    n = len(strs)
    m = len(strs[0])
    rs = "" if n == 1 else "s"
    ls = "" if m == 1 else "s"
    return f"{n} row{rs} of {m} letter{ls}"


def main():
    examples = [
        ["cba", "daf", "ghi"],
        ["a", "b"],
        ["zyx", "wvu", "tsr"],
        ["abc"],
        ["a", "a", "a"],
        ["b", "a"],
        ["ab", "ba", "ab"],
        ["aaa", "aab", "aba", "baa"],
    ]
    for strs in examples:
        print(f"{shape(strs)}: {min_deletion_size(strs)} deleted")
    rows = 0
    columns = 0
    deleted = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 20
        m = 1 + next_random() % 30
        letters = 1 + next_random() % 26
        strs = random_grid(n, m, letters)
        d = min_deletion_size(strs)
        rows += n
        columns += m
        deleted += d
        check = (check * 31 + d) % 1000000007
    print(f"300 random grids of {rows} rows and {columns} columns: {deleted} deleted, checksum {check}")
    sets = [random_grid(100, 1000, 26), random_grid(100, 1000, 2)]
    sets.append(["".join("z" if c == r * 10 else chr(97 + r // 4) for c in range(1000)) for r in range(100)])
    sets.append(["".join(chr(122 - r // 4 - c % 2) for c in range(1000)) for r in range(100)])
    for strs in sets:
        print(f"{shape(strs)}: {min_deletion_size(strs)} deleted")


main()
