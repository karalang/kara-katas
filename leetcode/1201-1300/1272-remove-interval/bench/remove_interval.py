# LeetCode #1272 bench, in Python: the ★ arm (one pass; an interval the cut
# misses kept whole, one it meets keeping its parts before and after) on 20
# random lists of 10,000 intervals drawn once, each cut three ways, 40
# rounds; every interval kept folded into a checksum. Each interval is its
# own two-element array, as LeetCode's `int[][]` is.


def remove_interval(intervals, to_be_removed):
    lo, hi = to_be_removed
    out = []
    for a, b in intervals:
        if b <= lo or a >= hi:
            out.append([a, b])
            continue
        if a < lo:
            out.append([a, lo])
        if b > hi:
            out.append([hi, b])
    return out


seed = 1272


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


lists = []
for _ in range(20):
    lst = []
    at = -1000000
    for _ in range(10000):
        a = at + next_random() % 50
        b = a + 1 + next_random() % 50
        lst.append([a, b])
        at = b
    lists.append(lst)
check = 0
for rnd in range(40):
    for lst in lists:
        for cut in [[-990000, -800000], [-700000, -699990], [-1000000, 1000000]]:
            kept = remove_interval(lst, cut)
            check = (check * 131 + len(kept) + rnd) % 1000000007
            for a, b in kept:
                check = (check * 131 + a + b + 2000000) % 1000000007
print(f"40 rounds of 20 lists cut 3 ways: checksum {check}")
