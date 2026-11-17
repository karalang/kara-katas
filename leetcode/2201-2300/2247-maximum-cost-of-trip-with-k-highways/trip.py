# LeetCode #2247: Maximum Cost of Trip With K Highways -- the Python
# mirror of trip.kara: dynamic programming over subsets, best[mask][v]
# the dearest trip visiting exactly mask and ending at v, masks in
# increasing order. O(2^n * n + 2^n * m).


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
        for v in range(n):
            cost = best[mask][v]
            if cost < 0:
                continue
            if cities == k + 1:
                answer = max(answer, cost)
                continue
            for w, toll in roads[v]:
                if mask & (1 << w) == 0:
                    nxt = mask | (1 << w)
                    best[nxt][w] = max(best[nxt][w], cost + toll)
    return answer


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_highways(n, m):
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
    for i in range(len(pairs) - 1, 0, -1):
        j = next_random() % (i + 1)
        pairs[i], pairs[j] = pairs[j], pairs[i]
    out = []
    for a, b in pairs[:m]:
        toll = next_random() % 101
        out.append([a, b, toll] if next_random() % 2 == 0 else [b, a, toll])
    return out


def main():
    global seed
    examples = [
        (5, [[0, 1, 4], [2, 1, 3], [1, 4, 11], [3, 2, 3], [3, 4, 2]], 3),
        (4, [[0, 1, 3], [2, 3, 2]], 2),
        (2, [[1, 0, 7]], 1),
        (3, [[0, 1, 5], [1, 2, 5]], 3),
        (3, [[0, 1, 1], [1, 2, 10], [2, 0, 100]], 2),
        (4, [[0, 1, 0], [1, 2, 0], [2, 3, 0]], 3),
    ]
    for n, highways, k in examples:
        print(f"n={n} {highways} k={k} -> {maximum_cost(n, highways, k)}")
    seed = 2247
    possible = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 6 + 2
        m = next_random() % (n * (n - 1) // 2) + 1
        highways = random_highways(n, m)
        k = next_random() % 7 + 1
        cost = maximum_cost(n, highways, k)
        if cost >= 0:
            possible += 1
        check = (check * 31 + cost + 1) % 1000000007
    print(f"2000 trips: {possible} possible, checksum {check}")
    highways = random_highways(15, 50)
    print(f"15 cities, k=14: {maximum_cost(15, highways, 14)}")
    print(f"15 cities, k=50: {maximum_cost(15, highways, 50)}")


main()
