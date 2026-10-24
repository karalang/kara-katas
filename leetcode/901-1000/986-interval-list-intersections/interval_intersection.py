# LeetCode #986: Interval List Intersections -- mirror of the ★ arm
# (interval_intersection.kara), two pointers.


def interval_intersection(first, second):
    out = []
    i = j = 0
    while i < len(first) and j < len(second):
        lo = max(first[i][0], second[j][0])
        hi = min(first[i][1], second[j][1])
        if lo <= hi:
            out.append((lo, hi))
        if first[i][1] < second[j][1]:
            i += 1
        else:
            j += 1
    return out


seed = 986


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def listed(xs):
    if len(xs) > 6:
        return f"{len(xs)} intervals from {xs[0][0]} to {xs[-1][1]}"
    return "[" + ", ".join(f"[{s}, {e}]" for s, e in xs) + "]"


def show(first, second):
    print(f"{listed(first)} and {listed(second)} -> {listed(interval_intersection(first, second))}")


def wide_random():
    return next_random() * 32768 + next_random()


def random_list(n, gap, length):
    out = []
    pos = wide_random() % gap
    for _ in range(n):
        start = pos
        end = start + 1 + wide_random() % length
        out.append((start, end))
        pos = end + 1 + wide_random() % gap
    return out


def main():
    show([(0, 2), (5, 10), (13, 23), (24, 25)], [(1, 5), (8, 12), (15, 24), (25, 26)])
    show([(1, 3), (5, 9)], [])
    show([], [(1, 2)])
    show([(1, 2), (4, 7)], [(1, 2), (4, 7)])
    show([(1, 2)], [(2, 3)])
    show([(0, 100)], [(1, 2), (4, 5), (7, 9)])
    show([(1, 2), (5, 6)], [(3, 4), (7, 8)])
    show([(0, 1000000000)], [(999999999, 1000000000)])
    first = [(4 * i, 4 * i + 2) for i in range(1000)]
    second = [(4 * i + 1, 4 * i + 3) for i in range(1000)]
    show(first, second)
    first = [(3 * i, 3 * i + 1) for i in range(1000)]
    second = [(0, 1000000000)]
    show(first, second)
    for count, n, gap, length in [(300, 6, 6, 6), (3000, 50, 40, 40), (3, 1000, 499999, 499999)]:
        found = 0
        covered = 0
        check = 0
        for _ in range(count):
            a = n if count == 3 else next_random() % (n + 1)
            b = n if count == 3 else next_random() % (n + 1)
            first = random_list(a, gap, length)
            second = random_list(b, gap, length)
            for lo, hi in interval_intersection(first, second):
                found += 1
                covered += hi - lo
                check = (check * 31 + lo) % 1000000007
                check = (check * 31 + hi) % 1000000007
        print(f"{count} random pairs of up to {n} intervals: {found} intersections covering {covered}, checksum {check}")


main()
