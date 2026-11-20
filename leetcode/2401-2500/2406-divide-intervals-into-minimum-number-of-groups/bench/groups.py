# LeetCode #2406: Divide Intervals Into Minimum Number of Groups -- the
# bench, the ★ arm in Python: the intervals sorted by left end, and a
# heapq of each group's last right end, the smallest first.

import heapq

seed = 2406


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def min_groups(intervals):
    ends = []
    for left, right in sorted(intervals):
        if ends and ends[0] < left:
            heapq.heappop(ends)
        heapq.heappush(ends, right)
    return len(ends)


def main():
    sets = []
    for i in range(10):
        iv = []
        for _ in range(100000):
            left = 1 + (next_random() * 32768 + next_random()) % 900000
            iv.append((left, left + (next_random() * 32768 + next_random()) % (1 + 1000 * i)))
        sets.append(iv)
    check = 0
    for p in range(5):
        for iv in sets:
            check = (check * 31 + min_groups(iv) + p) % 1000000007
    print(f"5 passes over 10 sets of 10^5 intervals: checksum {check}")


main()
