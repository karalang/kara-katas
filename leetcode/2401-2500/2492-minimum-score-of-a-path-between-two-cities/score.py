# LeetCode #2492: Minimum Score of a Path Between Two Cities -- Python
# mirror of the ★ arm (score.kara): a breadth-first search from 1, the
# least distance kept on every road looked at.


def min_score(n, roads):
    nxt = [[] for _ in range(n + 1)]
    for a, b, d in roads:
        nxt[a].append((b, d))
        nxt[b].append((a, d))
    seen = [False] * (n + 1)
    queue = [1]
    seen[1] = True
    head = 0
    least = 2**63 - 1
    while head < len(queue):
        city = queue[head]
        head += 1
        for other, distance in nxt[city]:
            least = min(least, distance)
            if not seen[other]:
                seen[other] = True
                queue.append(other)
    return least


# ---- test harness -----------------------------------------------------------

seed = 2492


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def random_roads(n, extra, top):
    roads = []
    at = 1
    while at != n:
        nxt = wide() % n + 1
        if nxt == at:
            nxt = n
        roads.append([at, nxt, wide() % top + 1])
        at = nxt
    for _ in range(extra):
        a = wide() % n + 1
        b = wide() % n + 1
        if b == a:
            b = a % n + 1
        roads.append([a, b, wide() % top + 1])
    return roads


def main():
    cases = [
        (4, [[1, 2, 9], [2, 3, 6], [2, 4, 5], [1, 4, 7]]),
        (4, [[1, 2, 2], [1, 3, 4], [3, 4, 7]]),
        (2, [[1, 2, 5]]),
        (4, [[1, 4, 10], [2, 3, 1]]),
        (3, [[1, 2, 8], [1, 2, 3], [2, 3, 9]]),
        (5, [[5, 4, 6], [4, 1, 7], [2, 3, 1], [3, 1, 4]]),
        (6, [[1, 6, 9], [2, 3, 1], [3, 4, 2], [4, 2, 3], [5, 6, 4]]),
    ]
    for n, roads in cases:
        print(f"{n} cities, {len(roads)} roads -> {min_score(n, roads)}")
    for top in [10000, 5]:
        check = 0
        for _ in range(2000):
            n = next_random() % 49 + 2
            extra = next_random() % 61
            roads = random_roads(n, extra, top)
            check = (check * 31 + min_score(n, roads)) % 1000000007
        print(f"2000 random to {top}: checksum {check}")
    n = 100000
    chain = [[i, i + 1, 10000 - i % 9000] for i in range(1, n)]
    star = [[1, i, i % 10000 + 1] for i in range(2, n + 1)]
    star.append([2, 3, 1])
    parted = [[r[0], r[1], r[2] + 1] for r in random_roads(n - 3, 40000, 9999)]
    parted.append([n - 3, n, 5000])
    parted.append([n - 2, n - 1, 1])
    for name, cities, roads in [("chain", n, chain), ("star", n, star), ("random", n, parted)]:
        print(f"10^5 {name}: {len(roads)} roads -> {min_score(cities, roads)}")


main()
