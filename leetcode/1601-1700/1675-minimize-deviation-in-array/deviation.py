# LeetCode #1675: Minimize Deviation in Array -- the Python mirror of the
# ★ arm: a max-first priority queue (heapq on negated values).

import heapq


def minimum_deviation(nums):
    queue = []
    smallest = 2**31 - 1
    for x in nums:
        start = x * 2 if x % 2 == 1 else x
        heapq.heappush(queue, -start)
        smallest = min(smallest, start)
    best = 2**31 - 1
    while True:
        top = -heapq.heappop(queue)
        best = min(best, top - smallest)
        if top % 2 == 1:
            break
        smallest = min(smallest, top // 2)
        heapq.heappush(queue, -(top // 2))
    return best


seed = 1675


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, longest, most):
    total = 0
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % (longest - 1) + 2
        nums = [(next_random() * 32768 + next_random()) % most + 1 for _ in range(n)]
        deviation = minimum_deviation(nums)
        total += deviation
        check = (check * 31 + deviation + n) % 1000000007
    print(f"{count} arrays of up to {longest} values up to {most}: deviations sum to {total}, checksum {check}")


print(minimum_deviation([1, 2, 3, 4]))
print(minimum_deviation([4, 1, 5, 20, 3]))
print(minimum_deviation([2, 10, 8]))
print(minimum_deviation([3, 5]))
print(minimum_deviation([1, 1024]))
print(minimum_deviation([1000000000, 999999999]))
batch(3000, 8, 64)
batch(300, 1000, 1000000000)
batch(10, 50000, 1000000000)
