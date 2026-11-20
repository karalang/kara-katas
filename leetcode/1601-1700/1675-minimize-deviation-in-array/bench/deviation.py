# LeetCode #1675: Minimize Deviation in Array -- the bench's Python mirror:
# the ★ arm on 50 arrays of 50000 values up to 10^9, all drawn first, each
# answered 10 times, with heapq on negated values (largest first).

import heapq


def minimum_deviation(nums):
    queue = [-(x * 2 if x % 2 == 1 else x) for x in nums]
    heapq.heapify(queue)
    smallest = -max(queue)
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


def main():
    arrays, n, rounds = 50, 50000, 10
    cases = [[(next_random() * 32768 + next_random()) % 1000000000 + 1 for _ in range(n)] for _ in range(arrays)]
    total = 0
    check = 0
    for r in range(rounds):
        for nums in cases:
            deviation = minimum_deviation(nums)
            total += deviation
            check = (check * 31 + deviation + r) % 1000000007
    print(f"{arrays} arrays of {n} values, {rounds} rounds: deviations sum to {total}, checksum {check}")


main()
