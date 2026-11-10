# LeetCode #2064: Minimized Maximum of Products Distributed to Any Store --
# Python mirror of the ★ arm (stores.kara): a binary search for the least
# load `x` at which every product type fits, `ceil(q / x)` stores to a type,
# in `n` stores.


def minimized_maximum(n, quantities):
    lo, hi = 1, max(quantities)
    while lo < hi:
        mid = (lo + hi) // 2
        if sum((q + mid - 1) // mid for q in quantities) <= n:
            hi = mid
        else:
            lo = mid + 1
    return lo


seed = 2064


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(qs):
    return "[" + ", ".join(str(q) for q in qs) + "]"


def main():
    examples = [(6, [11, 6]), (7, [15, 10, 10]), (1, [100000]), (3, [1, 1, 1]),
                (5, [1, 1, 1]), (100000, [100000]), (4, [7, 7]), (10, [1, 2, 3, 4, 5])]
    for n, qs in examples:
        print(f"n = {n}, {show(qs)} -> {minimized_maximum(n, qs)}")
    # 500 problems of 1 to 20 types, quantities from 1 to 1, 10, 1000 or
    # 100000, and from as many stores as types to ten times as many
    total = 0
    check = 0
    for _ in range(500):
        m = next_random() % 20 + 1
        top = [1, 10, 1000, 100000][next_random() % 4]
        qs = [(next_random() * 32768 + next_random()) % top + 1 for _ in range(m)]
        n = m + next_random() % (9 * m + 1)
        a = minimized_maximum(n, qs)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"500 problems: sum {total}, checksum {check}")
    # the constraints' largest: 100000 stores, 50000 types
    qs = [(next_random() * 32768 + next_random()) % 100000 + 1 for _ in range(50000)]
    print(f"n = 100000, 50000 types -> {minimized_maximum(100000, qs)}")


main()
