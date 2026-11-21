# LeetCode #2492: Minimum Score of a Path Between Two Cities -- benchmark
# mirror of the ★ arm (score.kara): one map of 10^5 cities and 10^5 roads,
# built once, then the passes; each sets one road's distance to a value
# chosen by the checksum so far, asks, and puts it back.


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


seed = 2492


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    passes = 50
    roads = [[1, n, 10000]]
    while len(roads) < n:
        a = (next_random() * 32768 + next_random()) % n + 1
        b = (next_random() * 32768 + next_random()) % n + 1
        if a != b:
            roads.append([a, b, next_random() % 10000 + 1])
    m = len(roads)
    check = 0
    for p in range(passes):
        at = check % m
        was = roads[at][2]
        roads[at][2] = (check // m + p) % 10000 + 1
        check = (check * 31 + min_score(n, roads) + p) % 1000000007
        roads[at][2] = was
    print(f"{passes} passes over 10^5 cities and {m} roads: checksum {check}")


main()
