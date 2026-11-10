# LeetCode #2093: Minimum Cost to Reach City With Discounts -- Python mirror
# of the ★ arm's benchmark (discounts.kara): the same 60 maps, each asked by
# the same Dijkstra over (city, used) states with `heapq`.
import heapq

I64_MAX = 2**63 - 1
seed = 2093


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def minimum_cost(n, highways, discounts):
    roads = [[] for _ in range(n)]
    for a, b, toll in highways:
        roads[a].append((b, toll))
        roads[b].append((a, toll))
    k = discounts + 1
    best = [I64_MAX] * (n * k)
    heap = [(0, 0, 0)]
    best[0] = 0
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


def main():
    n = 20000
    total = 0
    check = 0
    for g in range(60):
        highways = []
        for a in range(n):
            for base in (1, 1667, 3333):
                b = (a + base + next_random() % 1666) % n
                hi = next_random()
                toll = (hi * 32768 + next_random()) % 100001
                highways.append((a, b, toll))
        c = minimum_cost(n, highways, g % 12 * 2)
        total += c
        check = (check * 31 + c + 2) % 1000000007
    print(f"60 answers: sum {total}, checksum {check}")


main()
