# LeetCode #1046: Last Stone Weight -- benchmark driver, Python mirror of
# last_stone.kara. heapq is smallest-first, so the stones go in negated.
import heapq


def last_stone_weight(stones):
    heap = [-w for w in stones]
    heapq.heapify(heap)
    while True:
        if not heap:
            return 0
        y = -heapq.heappop(heap)
        if not heap:
            return y
        x = -heapq.heappop(heap)
        if y > x:
            heapq.heappush(heap, -(y - x))


seed = 1046


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n, rounds = 1000, 3000, 3
    piles = []
    for _ in range(count):
        pile = []
        for _ in range(n):
            high = next_random()
            low = next_random()
            pile.append((high * 32768 + low) % 1000000000 + 1)
        piles.append(pile)
    total = check = 0
    for _ in range(rounds):
        for pile in piles:
            answer = last_stone_weight(pile)
            total += answer
            check = (check * 131 + answer % 1000000007 + 1) % 1000000007
    print(f"{count} piles of {n} stones, {rounds} rounds: total {total}, checksum {check}")


main()
