# Benchmark: LeetCode #986 Interval List Intersections -- the ★ arm, two pointers,
# on pairs of LeetCode's largest lists, 1000 intervals each.
# Mirrors interval_intersection.kara, .rs, .c and go-seq/.


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


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def random_list():
    out = []
    pos = wide_random() % 499999
    for _ in range(1000):
        start = pos
        end = start + 1 + wide_random() % 499999
        out.append((start, end))
        pos = end + 1 + wide_random() % 499999
    return out


def main():
    rounds = 1000
    lists = [random_list() for _ in range(21)]
    found = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            k = (r + i) % 20
            answer = interval_intersection(lists[k], lists[k + 1])
            found += len(answer)
            lo, hi = answer[len(answer) // 2]
            check = (check * 31 + len(answer) + lo % 1000 + hi % 1000) % 1000000007
    print(f"{rounds} rounds over 20 pairs of 1000 intervals: {found} intersections, checksum {check}")


main()
