# LeetCode #1786: Number of Restricted Paths From First to Last Node -- the
# bench in Python, mirroring count_restricted_paths.kara: Dijkstra from node
# n with heapq, then the paths summed in the order the nodes settled.
import heapq


def count_restricted_paths(n, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = [-1] * (n + 1)
    order = []
    queue = [(0, n)]
    while queue:
        d, u = heapq.heappop(queue)
        if dist[u] != -1:
            continue
        dist[u] = d
        order.append(u)
        for v, w in adj[u]:
            if dist[v] == -1:
                heapq.heappush(queue, (d + w, v))
    ways = [0] * (n + 1)
    ways[n] = 1
    for u in order:
        for v, _ in adj[u]:
            if dist[v] < dist[u]:
                ways[u] = (ways[u] + ways[v]) % 1000000007
    return ways[1]


seed = 1786


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_graph(n, extra):
    edges = []
    joined = set()
    for v in range(2, n + 1):
        u = 1 + next_random() % (v - 1)
        w = 1 + next_random() % 100000
        joined.add((u, v))
        edges.append([u, v, w])
    for _ in range(extra):
        a = 1 + next_random() % n
        b = 1 + next_random() % n
        u, v = (a, b) if a < b else (b, a)
        if u == v or (u, v) in joined:
            continue
        w = 1 + next_random() % 100000
        joined.add((u, v))
        edges.append([u, v, w])
    return edges


def main():
    graphs = [random_graph(2000, 2001) for _ in range(200)]
    check = 0
    for call in range(1000):
        edges = graphs[(check + call) % 200]
        check = (check * 31 + count_restricted_paths(2000, edges)) % 1000000007
    print(f"1000 calls over 200 graphs: checksum {check}")


main()
