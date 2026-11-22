# LeetCode #2714: Find Shortest Path with K Hops -- the bench (hops.kara in
# Python): Dijkstra's search over states of a node and the hops spent,
# a `heapq` of (distance, node, hops).
import heapq


def shortest_path_with_hops(n, edges, s, d, k):
    adjacent = [[] for _ in range(n)]
    for u, v, w in edges:
        adjacent[u].append((v, w))
        adjacent[v].append((u, w))
    far = 2**63 - 1
    dist = [[far] * (k + 1) for _ in range(n)]
    dist[s][0] = 0
    queue = [(0, s, 0)]
    while queue:
        here, u, hops = heapq.heappop(queue)
        if here > dist[u][hops]:
            continue
        if u == d:
            return here
        for v, w in adjacent[u]:
            if here + w < dist[v][hops]:
                dist[v][hops] = here + w
                heapq.heappush(queue, (here + w, v, hops))
            if hops < k and here < dist[v][hops + 1]:
                dist[v][hops + 1] = here
                heapq.heappush(queue, (here, v, hops + 1))
    return -1


seed = 2714


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


graphs, rounds = 50, 10
problems = []
for _ in range(graphs):
    n = 500
    joined = set()
    edges = []
    for v in range(1, n):
        u = next_random() % v
        joined.add((u, v))
        edges.append([u, v, wide() % 1000000 + 1])
    for _ in range(9501):
        a = next_random() % n
        b = next_random() % n
        u, v = min(a, b), max(a, b)
        if u != v and (u, v) not in joined:
            joined.add((u, v))
            edges.append([v, u, wide() % 1000000 + 1])
    s = next_random() % n
    d = (s + 1 + next_random() % (n - 1)) % n
    k = next_random() % 50
    problems.append((edges, s, d, k))
total = 0
check = 0
for r in range(rounds):
    for edges, s, d, k in problems:
        length = shortest_path_with_hops(500, edges, s, d, k)
        total += length
        check = (check * 31 + length + r) % 1000000007
print(f"{graphs} graphs of 500 nodes, {rounds} rounds: lengths sum to {total}, checksum {check}")
