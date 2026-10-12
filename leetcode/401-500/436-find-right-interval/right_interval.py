# LeetCode #436: Find Right Interval -- mirror of right_interval.kara
# (sorted starts and binary search).


def find_right_interval(intervals):
    n = len(intervals)
    order = sorted(range(n), key=lambda i: intervals[i][0])
    right = []
    for i in range(n):
        end = intervals[i][1]
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if intervals[order[mid]][0] < end:
                lo = mid + 1
            else:
                hi = mid
        right.append(order[lo] if lo < n else -1)
    return right


def text(values):
    return "[" + ",".join(f"[{a},{b}]" for a, b in values) + "]"


def show(intervals):
    right = find_right_interval(intervals)
    print(f"{text(intervals)}: [{','.join(str(j) for j in right)}]")


seed = 436


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([(1, 2)])
    show([(3, 4), (2, 3), (1, 2)])
    show([(1, 4), (2, 3), (3, 4)])
    show([(5, 5), (1, 5), (6, 9)])
    show([(-1000000, 1000000), (1000000, 1000000), (0, 0)])
    show([(0, 10), (1, 2), (3, 4), (5, 6), (7, 8)])
    show([(4, 9), (3, 8), (2, 7), (1, 6), (0, 5)])
    show([(0, 1), (1, 2), (2, 3), (3, 4)])
    # 300 random sets of 1 to 40 intervals with distinct starts in
    # [-100, 100), each 0 to 39 long.
    found = 0
    checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 40
        used = set()
        intervals = []
        while len(intervals) < n:
            start = next_random() % 200 - 100
            if start not in used:
                used.add(start)
                intervals.append((start, start + next_random() % 40))
        right = find_right_interval(intervals)
        for j in right:
            if j >= 0:
                found += 1
            checksum = (checksum * 31 + j + 2) % 1000000007
    print(f"300 random sets: {found} right intervals, checksum {checksum}")


main()
