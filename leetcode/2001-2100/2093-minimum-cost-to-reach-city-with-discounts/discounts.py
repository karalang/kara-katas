# LeetCode #2093: Minimum Cost to Reach City With Discounts -- Python mirror
# of the ★ arm (discounts.kara): Dijkstra over (city, used) states with a
# heap of (cost, city, used), smallest first.
import heapq

I64_MAX = 2**63 - 1


def minimum_cost(n, highways, discounts):
    roads = [[] for _ in range(n)]
    for a, b, toll in highways:
        roads[a].append((b, toll))
        roads[b].append((a, toll))
    k = discounts + 1
    best = [I64_MAX] * (n * k)
    heap = []
    best[0] = 0
    heapq.heappush(heap, (0, 0, 0))
    while heap:
        cost, city, used = heapq.heappop(heap)
        if city == n - 1:
            return cost
        if cost > best[city * k + used]:
            continue
        for other, toll in roads[city]:
            full = cost + toll
            if full < best[other * k + used]:
                best[other * k + used] = full
                heapq.heappush(heap, (full, other, used))
            if used < discounts:
                half = cost + toll // 2
                if half < best[other * k + used + 1]:
                    best[other * k + used + 1] = half
                    heapq.heappush(heap, (half, other, used + 1))
    return -1


# ---- test harness -----------------------------------------------------------

class Seed:
    def __init__(self, v):
        self.v = v


def next_random(seed):
    seed.v = (seed.v * 1103515245 + 12345) % 2147483648
    return seed.v // 65536


def random_highways(n, m, top, seed):
    seen = set()
    highways = []
    for _ in range(m):
        a = next_random(seed) % n
        b = (a + 1 + next_random(seed) % (n - 1)) % n
        hi = next_random(seed)
        toll = (hi * 32768 + next_random(seed)) % top
        key = (min(a, b), max(a, b))
        if key not in seen:
            seen.add(key)
            highways.append((a, b, toll))
    return highways


def main():
    examples = [
        (5, [(0, 1, 4), (2, 1, 3), (1, 4, 11), (3, 2, 3), (3, 4, 2)], 1),
        (4, [(1, 3, 17), (1, 2, 7), (3, 2, 5), (0, 1, 6), (3, 0, 20)], 20),
        (4, [(0, 1, 3), (2, 3, 2)], 0),
        (2, [(0, 1, 7)], 0),
        (2, [(0, 1, 7)], 1),
        (3, [(0, 1, 1), (1, 2, 1), (0, 2, 5)], 1),
        (4, [(0, 1, 9), (1, 2, 9), (2, 3, 9), (0, 3, 40)], 2),
    ]
    for n, highways, discounts in examples:
        print(f"{n} cities, {len(highways)} highways, {discounts} discounts -> {minimum_cost(n, highways, discounts)}")
    seed = Seed(2093)
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random(seed) % 29 + 2
        m = next_random(seed) % 40 + 1
        top = [10, 100, 100001][next_random(seed) % 3]
        highways = random_highways(n, m, top, seed)
        discounts = next_random(seed) % 6
        c = minimum_cost(n, highways, discounts)
        total += c
        check = (check * 31 + c + 2) % 1000000007
    print(f"2000 maps: sum {total}, checksum {check}")
    big = random_highways(1000, 1000, 100001, seed)
    print(f"1000 cities: {minimum_cost(1000, big, 0)} with none, {minimum_cost(1000, big, 3)} with 3, {minimum_cost(1000, big, 500)} with 500")
    road = [(i, i + 1, 100000) for i in range(999)]
    print(f"a road of 999: {minimum_cost(1000, road, 0)} with none, {minimum_cost(1000, road, 500)} with 500")


main()
