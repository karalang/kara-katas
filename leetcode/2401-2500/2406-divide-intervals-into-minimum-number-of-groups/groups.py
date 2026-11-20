# LeetCode #2406: Divide Intervals Into Minimum Number of Groups -- the
# mirror of the ★ arm: the intervals in order of left end, a heap of each
# group's last right end, the smallest first.

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


def intervals(count, span, longest):
    out = []
    for _ in range(count):
        left = 1 + (next_random() * 32768 + next_random()) % span
        out.append((left, left + (next_random() * 32768 + next_random()) % longest))
    return out


def main():
    print(min_groups([(5, 10), (6, 8), (1, 5), (2, 3), (1, 10)]))
    print(min_groups([(1, 3), (5, 6), (8, 10), (11, 13)]))
    print(min_groups([(1000000, 1000000)]))
    print(min_groups([(1, 2), (2, 3)]))
    print(min_groups([(4, 7)] * 10))
    print(min_groups(intervals(100000, 999900, 100)))
    print(min_groups(intervals(100000, 900000, 100000)))
    check = 0
    total = 0
    for _ in range(2000):
        count = 1 + next_random() % 30
        a = min_groups(intervals(count, 40, 1 + next_random() % 20))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
