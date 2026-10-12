# Benchmark for #436: mirror of right_interval.kara (sorted starts and
# binary search) on 100 random sets of 20,000 intervals.


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


seed = 436


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    size = 20000
    rounds = 100
    found = 0
    checksum = 0
    for _ in range(rounds):
        # Distinct starts, one in each step of 100 across the range,
        # each interval up to 32,767 long, then shuffled.
        intervals = []
        for i in range(size):
            start = -1000000 + 100 * i + next_random() % 100
            end = min(start + next_random(), 1000000)
            intervals.append((start, end))
        for i in range(size):
            j = i + next_random() % (size - i)
            intervals[i], intervals[j] = intervals[j], intervals[i]
        for j in find_right_interval(intervals):
            if j >= 0:
                found += 1
            checksum = (checksum * 31 + j + 2) % 1000000007
    print(f"{rounds} rounds of {size} intervals: {found} right intervals, checksum {checksum}")


main()
