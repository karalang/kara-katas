# LeetCode #2714: Find Shortest Path with K Hops -- the ★ arm (hops.kara)
# in Python: Dijkstra's search over states of a node and the hops spent.
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


def random_graph(n, extra, heaviest):
    joined = set()
    edges = []
    for v in range(1, n):
        u = next_random() % v
        joined.add((u, v))
        edges.append([u, v, wide() % heaviest + 1])
    for _ in range(extra):
        a = next_random() % n
        b = next_random() % n
        u, v = min(a, b), max(a, b)
        if u != v and (u, v) not in joined:
            joined.add((u, v))
            edges.append([v, u, wide() % heaviest + 1])
    return edges


print(shortest_path_with_hops(4, [[0, 1, 4], [0, 2, 2], [2, 3, 6]], 1, 3, 2))
print(shortest_path_with_hops(7, [[3, 1, 9], [3, 2, 4], [4, 0, 9], [0, 5, 6], [3, 6, 2], [6, 0, 4], [1, 2, 4]], 4, 1, 2))
print(shortest_path_with_hops(5, [[0, 4, 2], [0, 1, 3], [0, 2, 1], [2, 1, 4], [1, 3, 4], [3, 4, 7]], 2, 3, 1))
path = [[i, i + 1, 1000000] for i in range(499)]
print(shortest_path_with_hops(500, path, 0, 499, 0))
print(shortest_path_with_hops(500, path, 0, 499, 10))
print(shortest_path_with_hops(50, path[0:49], 49, 0, 49))
dense = random_graph(500, 9501, 1000000)
print(f"{len(dense)} edges: {shortest_path_with_hops(500, dense, 0, 499, 1)}")
total = 0
check = 0
for c in range(1020):
    if c < 1000:
        n = next_random() % 9 + 2
        extra, heaviest = next_random() % (n * 2), 20
    else:
        n, extra, heaviest = next_random() % 99 + 2, next_random() % 900, 1000000
    edges = random_graph(n, extra, heaviest)
    s = next_random() % n
    d = (s + 1 + next_random() % (n - 1)) % n
    k = next_random() % min(n, 12)
    length = shortest_path_with_hops(n, edges, s, d, k)
    total += length
    check = (check * 31 + length) % 1000000007
    if c == 999:
        print(f"1000 small graphs: lengths sum to {total}, checksum {check}")
        total = 0
        check = 0
print(f"20 graphs up to 100 nodes: lengths sum to {total}, checksum {check}")
