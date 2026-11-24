# LeetCode #2462: Total Cost to Hire K Workers -- the bench, the ★ arm in
# Python: two heaps of `(cost, index)` by `heapq`, the first and the last
# `candidates` workers, each session taking the cheaper top and refilling
# its heap from the untaken middle.

import heapq


def total_cost(costs, k, candidates):
    n = len(costs)
    front, back = [], []
    nxt, last = 0, n - 1
    while nxt < candidates and nxt <= last:
        heapq.heappush(front, (costs[nxt], nxt))
        nxt += 1
    while n - 1 - last < candidates and nxt <= last:
        heapq.heappush(back, (costs[last], last))
        last -= 1
    total = 0
    for _ in range(k):
        if front and (not back or front[0] <= back[0]):
            cost, _ = heapq.heappop(front)
            total += cost
            if nxt <= last:
                heapq.heappush(front, (costs[nxt], nxt))
                nxt += 1
        else:
            cost, _ = heapq.heappop(back)
            total += cost
            if nxt <= last:
                heapq.heappush(back, (costs[last], last))
                last -= 1
    return total


seed = 2462


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    # 10 lists of 10^5 costs from 1 to 10^5 built once; then 32 passes,
    # each setting one cost of every list from the checksum so far, then
    # answering every list with k of 5 10^4 and 1 + 97 p candidates,
    # folding the answer plus the pass into the checksum
    lists = [[1 + wide_random() % 100000 for _ in range(100000)] for _ in range(10)]
    check = 0
    for p in range(32):
        candidates = 1 + 97 * p
        for a in range(len(lists)):
            lists[a][(check + a) % 100000] = 1 + check % 100000
            check = (check * 31 + total_cost(lists[a], 50000, candidates) + p) % 1000000007
    print(f"32 passes over 10 lists of 10^5: checksum {check}")


main()
