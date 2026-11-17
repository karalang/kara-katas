# LeetCode #2247: Maximum Cost of Trip With K Highways -- the benchmark's
# Python mirror of trip.kara: dynamic programming over subsets, masks in
# increasing order.


def maximum_cost(n, highways, k):
    if k + 1 > n:
        return -1
    roads = [[] for _ in range(n)]
    for a, b, toll in highways:
        roads[a].append((b, toll))
        roads[b].append((a, toll))
    full = 1 << n
    best = [[-1] * n for _ in range(full)]
    for v in range(n):
        best[1 << v][v] = 0
    answer = -1
    for mask in range(1, full):
        cities = bin(mask).count("1")
        row = best[mask]
        for v in range(n):
            cost = row[v]
            if cost < 0:
                continue
            if cities == k + 1:
                answer = max(answer, cost)
                continue
            for w, toll in roads[v]:
                if mask & (1 << w) == 0:
                    nxt = mask | (1 << w)
                    if cost + toll > best[nxt][w]:
                        best[nxt][w] = cost + toll
    return answer


seed = 2247


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(16):
        pairs = [(a, b) for a in range(15) for b in range(a + 1, 15)]
        for i in range(len(pairs) - 1, 0, -1):
            j = next_random() % (i + 1)
            pairs[i], pairs[j] = pairs[j], pairs[i]
        highways = [[a, b, next_random() % 101] for a, b in pairs[:50]]
        check = (check * 31 + maximum_cost(15, highways, 14) + 1) % 1000000007
    print(f"16 maps of 15 cities: checksum {check}")


main()
