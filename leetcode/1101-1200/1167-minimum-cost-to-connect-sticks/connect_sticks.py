# LeetCode #1167: Minimum Cost to Connect Sticks -- the ★ arm and its
# harness in Python. `python3 connect_sticks.py lit` reads the statement
# literally instead for the piles of up to 8 sticks: every way of joining
# two sticks, tried, the cheapest kept.
import heapq
import sys
from functools import lru_cache


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


@lru_cache(maxsize=None)
def every_way(pile):
    if len(pile) <= 1:
        return 0
    best = None
    for i in range(len(pile)):
        for j in range(i + 1, len(pile)):
            rest = list(pile[:i] + pile[i + 1:j] + pile[j + 1:])
            rest.append(pile[i] + pile[j])
            c = pile[i] + pile[j] + every_way(tuple(sorted(rest)))
            if best is None or c < best:
                best = c
    return best


def literal(sticks):
    return every_way(tuple(sorted(sticks))) if len(sticks) <= 8 else connect_sticks(sticks)


solve = literal if len(sys.argv) > 1 else connect_sticks
seed = 1167


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(sticks):
    print(f"[{', '.join(str(s) for s in sticks)}] -> {solve(sticks)}")


show([2, 4, 3])
show([1, 8, 3, 5])
show([5])
show([1, 1])
show([3, 3, 3, 3])
show([1, 1, 2, 4, 8, 16, 32, 64])
show([10000, 1, 2, 3])
total = 0
check = 0
for i in range(300):
    n = 1 + next_random() % 50
    top = 10 if i % 2 == 0 else 10000
    sticks = [1 + next_random() % top for _ in range(n)]
    c = solve(sticks)
    total += c
    check = (check * 31 + c) % 1000000007
print(f"300 random piles: total {total}, checksum {check}")
sticks = [1 + next_random() % 10000 for _ in range(10000)]
print(f"10000 random sticks: {solve(sticks)}")
print(f"10000 sticks of 10000: {solve([10000] * 10000)}")
