# LeetCode #1046: Last Stone Weight -- Python mirror of last_stone.kara.
#
# The same game with heapq, which is smallest-first, so the stones go in
# negated.
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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_stones(n, most):
    return [next_random() % most + 1 for _ in range(n)]


def show(stones):
    return "[" + ",".join(str(w) for w in stones) + "]"


def main():
    global seed
    examples = [
        [2, 7, 4, 1, 8, 1],
        [1],
        [2, 2],
        [3, 1],
        [1, 1, 1],
        [10, 3, 3],
        [5, 5, 5, 5],
        [9, 3, 2, 10],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [1000, 1, 1, 1, 1],
    ]
    for stones in examples:
        print(f"{show(stones)} -> {last_stone_weight(stones)}")
    cases = total = check = 0
    for n in range(1, 7):
        for code in range(4 ** n):
            stones = []
            c = code
            for _ in range(n):
                stones.append(c % 4 + 1)
                c //= 4
            answer = last_stone_weight(stones)
            cases += 1
            total += answer
            check = (check * 131 + answer + 1) % 1000000007
    print(f"every pile of 1 to 6 stones of 1 to 4: {cases} cases, total {total}, checksum {check}")
    seed = 1046
    total = check = 0
    for _ in range(1000):
        n = next_random() % 30 + 1
        answer = last_stone_weight(random_stones(n, 1000))
        total += answer
        check = (check * 131 + answer + 1) % 1000000007
    print(f"1000 random piles: total {total}, checksum {check}")
    same = [1000] * 30
    rising = list(range(1, 31))
    doubling = [1 << i for i in range(10)]
    print(f"30 stones of 1000 -> {last_stone_weight(same)}")
    print(f"1 to 30 -> {last_stone_weight(rising)}")
    print(f"1, 2, 4, ..., 512 -> {last_stone_weight(doubling)}")


main()
