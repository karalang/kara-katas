# Benchmark: LeetCode #960 Delete Columns to Make Sorted III -- the ★
# arm, longest chain, on 100 strings of 100 letters, LeetCode's largest.
# Mirrors min_deletion_size.kara, .c, .rs and go-seq/.


def min_deletion_size(strs):
    n = len(strs)
    m = len(strs[0])
    longest = [1] * m
    best = 0
    for j in range(m):
        for k in range(j):
            before = True
            for i in range(n):
                if strs[i][k] > strs[i][j]:
                    before = False
                    break
            if before:
                longest[j] = max(longest[j], longest[k] + 1)
        best = max(best, longest[j])
    return m - best


seed = 960


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def nearly_sorted(n, m, letters, swaps):
    out = []
    for _ in range(n):
        b = sorted(ord("a") + next_random() % letters for _ in range(m))
        for _ in range(swaps):
            p = next_random() % (m - 1)
            b[p], b[p + 1] = b[p + 1], b[p]
        out.append(bytes(b))
    return out


def main():
    rounds = 40
    cases = [nearly_sorted(100, 100, 2 + i % 25, i % 10) for i in range(50)]
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(50):
            d = min_deletion_size(cases[(r + i) % 50])
            total += d
            check = (check * 31 + d + i) % 1000000007
    print(f"{rounds} rounds over 50 cases of 100 strings of 100 letters: {total} columns deleted, checksum {check}")


main()
