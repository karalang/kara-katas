# LeetCode #1167: Minimum Cost to Connect Sticks -- the ★ arm's bench in
# Python: a heapq heap, the two shortest joined and the join pushed back.
import heapq


def connect_sticks(sticks):
    pq = list(sticks)
    heapq.heapify(pq)
    cost = 0
    while len(pq) > 1:
        a = heapq.heappop(pq)
        b = heapq.heappop(pq)
        cost += a + b
        heapq.heappush(pq, a + b)
    return cost


seed = 1167


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    piles = [[1 + next_random() % 10000 for _ in range(10000)] for _ in range(16)]
    total = 0
    check = 0
    for _ in range(40):
        for k in range(16):
            at = next_random() % 10000
            piles[k][at] = 1 + next_random() % 10000
            c = connect_sticks(piles[k])
            total += c
            check = (check * 31 + c) % 1000000007
    print(f"40 rounds over 16 piles of 10^4 sticks: total {total}, checksum {check}")


main()
