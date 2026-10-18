# LeetCode #703: Kth Largest Element in a Stream -- a min-first heap of
# k.
#
# A mirror of kth_largest_element_in_a_stream.kara (the ★ arm) and its
# harness.

import heapq

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.top = []
        for x in nums:
            self.add(x)

    def add(self, val):
        heapq.heappush(self.top, val)
        if len(self.top) > self.k:
            heapq.heappop(self.top)
        return self.top[0]


def answers(k, nums, adds):
    s = KthLargest(k, nums)
    return [s.add(v) for v in adds]


def show(k, nums, adds):
    print(f"k {k}, nums {nums}, adds {adds}: {answers(k, nums, adds)}")


def checksum(values):
    total = 0
    for v in values:
        total = (total * 31 + v + 20000) % 1000000007
    return total


def random_values(n):
    return [next_random() % 20001 - 10000 for _ in range(n)]


def main():
    global seed
    show(3, [4, 5, 8, 2], [3, 5, 10, 9, 4])
    show(4, [7, 7, 7, 7, 8, 3], [2, 10, 9, 9])
    show(1, [], [-3, -2, -4, 0, 4])
    show(2, [0], [-1, 1, -2, -4, 3])
    show(5, [1, 2, 3, 4], [5, 0, 6, 6, 1])
    show(3, [9, 9, 9], [9, 9, 1, 10])
    show(3, [100], [90, 80, 70, 60, 50])
    show(3, [-100], [-90, -80, -70, -60, -50])
    seed = 703
    for k in [1, 5000, 10000]:
        n = 9999 if k == 10000 else 10000
        nums = random_values(n)
        adds = random_values(10000)
        got = answers(k, nums, adds)
        print(f"k {k}, {n} values, 10000 adds: last {got[-1]}, checksum {checksum(got)}")
    total = 0
    for _ in range(300):
        k = 1 + next_random() % 20
        n = k - 1 + next_random() % 31
        width = 1 + next_random() % 41
        nums = [next_random() % width - width // 2 for _ in range(n)]
        adds = [next_random() % width - width // 2 for _ in range(50)]
        total = (total * 31 + checksum(answers(k, nums, adds))) % 1000000007
    print(f"300 random streams: checksum {total}")


main()
