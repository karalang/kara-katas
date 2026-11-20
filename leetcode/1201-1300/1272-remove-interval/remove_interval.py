# LeetCode #1272: Remove Interval -- Python mirror of the ★ arm (one pass;
# an interval the cut misses kept whole, one it meets keeping its parts
# before and after the cut), with the same harness.


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


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def random_intervals(n, low, step):
    out = []
    at = low
    for _ in range(n):
        a = at + wide_random() % step
        b = a + 1 + wide_random() % step
        out.append([a, b])
        at = b
    return out


M = 1000000007


def fold(check, intervals):
    c = (check * 131 + len(intervals)) % M
    for a, b in intervals:
        c = (c * 131 + (a % M + M) % M) % M if a >= 0 else (c * 131 + (-((-a) % M)) + M) % M
        c = (c * 131 + (b % M + M) % M) % M if b >= 0 else (c * 131 + (-((-b) % M)) + M) % M
    return c


def show(v):
    return "[" + ", ".join("[" + ", ".join(str(x) for x in iv) + "]" for iv in v) + "]"


print(show(remove_interval([[0, 2], [3, 4], [5, 7]], [1, 6])))
print(show(remove_interval([[0, 5]], [2, 3])))
print(show(remove_interval([[-5, -4], [-3, -2], [1, 2], [3, 5], [8, 9]], [-1, 4])))
kept = 0
check = 0
for _ in range(3000):
    n = next_random() % 30 + 1
    intervals = random_intervals(n, -100, 6)
    lo = next_random() % 400 - 110
    hi = lo + 1 + next_random() % 80
    got = remove_interval(intervals, [lo, hi])
    kept += len(got)
    check = fold(check, got)
print(f"3000 random cases: {kept} intervals kept, checksum {check}")
wide = random_intervals(10000, -1000000000, 100000)
middle = remove_interval(wide, [-300000000, 250000000])
everything = remove_interval(wide, [-1000000000, 1000000000])
print(f"{len(middle)} and {len(everything)} intervals kept, checksum {fold(fold(0, middle), everything)}")
