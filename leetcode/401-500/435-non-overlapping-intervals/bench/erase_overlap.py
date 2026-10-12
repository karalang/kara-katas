# Benchmark for #435: mirror of erase_overlap.kara (greedy by end) on
# 100 windows of 100,000 intervals from one pool of 1,000,000.


def erase_overlap_intervals(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda iv: iv[1])
    kept = 1
    end = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] >= end:
            kept += 1
            end = intervals[i][1]
    return len(intervals) - kept


seed = 435


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    pool_size = 1000000
    size = 100000
    rounds = 100
    # Starts anywhere in [-50000, 50000), lengths 1 to 200.
    pool = []
    for _ in range(pool_size):
        hi = next_random()
        start = (hi * 32768 + next_random()) % 100000 - 50000
        pool.append((start, start + 1 + next_random() % 200))
    total = 0
    checksum = 0
    for _ in range(rounds):
        at = next_random() * 32768 % (pool_size - size + 1)
        window = []
        for i in range(at, at + size):
            window.append(pool[i])
        removed = erase_overlap_intervals(window)
        total += removed
        checksum = (checksum * 31 + removed) % 1000000007
    print(f"{rounds} rounds of {size} intervals: {total} removed, checksum {checksum}")


main()
