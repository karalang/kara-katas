# LeetCode #2462: Total Cost to Hire K Workers -- the Python mirror of
# hire.kara: two heaps of `(cost, index)`, the first `candidates` workers
# and the last `candidates` not already taken, each session taking the
# cheaper top and refilling its heap from the untaken middle.

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


# ---- test harness ---------------------------------------------------------

seed = 2462


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    cases = [
        ([17, 12, 10, 2, 7, 2, 11, 20, 8], 3, 4),
        ([1, 2, 4, 1], 3, 3),
        ([5], 1, 1),
        ([3, 1, 2], 2, 2),
        ([4, 9, 9, 4], 1, 1),
        ([6, 5, 4, 3, 2, 1], 6, 1),
        ([9, 8, 1, 1, 1, 7, 9], 4, 2),
    ]
    for costs, k, candidates in cases:
        print(f"{show(costs)}, k = {k}, candidates = {candidates} -> {total_cost(costs, k, candidates)}")
    print(f"2000 of 10^5, k = 2000, candidates = 1: {total_cost([100000] * 2000, 2000, 1)}")
    costs = [1 + wide_random() % 100000 for _ in range(2000)]
    print(f"2000 random, k = 1000, candidates = 2: {total_cost(costs, 1000, 2)}")
    print(f"2000 random, k = 2000, candidates = 1500: {total_cost(costs, 2000, 1500)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 12
        costs = [1 + next_random() % 6 for _ in range(n)]
        k = 1 + next_random() % n
        candidates = 1 + next_random() % n
        check = (check * 31 + total_cost(costs, k, candidates)) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
