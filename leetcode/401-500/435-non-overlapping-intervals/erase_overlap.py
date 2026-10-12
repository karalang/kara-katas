# LeetCode #435: Non-overlapping Intervals -- mirror of
# erase_overlap.kara (greedy by end).


def erase_overlap_intervals(intervals):
    if not intervals:
        return 0
    intervals = sorted(intervals, key=lambda iv: iv[1])
    kept = 1
    end = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] >= end:
            kept += 1
            end = intervals[i][1]
    return len(intervals) - kept


def text(intervals):
    return "[" + ",".join(f"[{a},{b}]" for a, b in intervals) + "]"


def show(intervals):
    print(f"{text(intervals)}: {erase_overlap_intervals(intervals)}")


seed = 435


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([(1, 2), (2, 3), (3, 4), (1, 3)])
    show([(1, 2), (1, 2), (1, 2)])
    show([(1, 2), (2, 3)])
    show([(-50000, 50000)])
    show([(1, 10), (2, 3), (4, 5), (6, 7)])
    show([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
    show([(-50000, 50000), (-50000, -49999), (49999, 50000), (0, 1)])
    show([(1, 5), (2, 6), (3, 7), (4, 8), (5, 9)])
    show([(3, 4), (1, 2), (2, 4), (1, 3), (0, 5)])
    # 300 random sets of 1 to 40 intervals, each 1 to 30 long, starting
    # in [-50, 50).
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 40
        intervals = []
        for _ in range(n):
            start = next_random() % 100 - 50
            intervals.append((start, start + 1 + next_random() % 30))
        removed = erase_overlap_intervals(intervals)
        total += removed
        checksum = (checksum * 31 + removed) % 1000000007
    print(f"300 random sets: {total} removed, checksum {checksum}")


main()
