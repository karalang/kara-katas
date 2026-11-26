# LeetCode #1786: Number of Restricted Paths From First to Last Node -- the
# ★ arm in Python: Dijkstra from node n with heapq, then each node's paths
# summed from its strictly nearer neighbours in the order they settled.
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


def random_graph(n, extra, most_w):
    edges = []
    joined = set()
    for v in range(2, n + 1):
        u = 1 + next_random() % (v - 1)
        w = 1 + next_random() % most_w
        joined.add((u, v))
        edges.append([u, v, w])
    for _ in range(extra):
        a = 1 + next_random() % n
        b = 1 + next_random() % n
        u, v = (a, b) if a < b else (b, a)
        if u == v or (u, v) in joined:
            continue
        w = 1 + next_random() % most_w
        joined.add((u, v))
        if next_random() % 2 == 0:
            edges.append([u, v, w])
        else:
            edges.append([v, u, w])
    return edges


def main():
    first = [[1, 2, 3], [1, 3, 3], [2, 3, 1], [1, 4, 2], [5, 2, 2], [3, 5, 1], [5, 4, 10]]
    second = [[1, 3, 1], [4, 1, 2], [7, 3, 4], [2, 5, 3], [5, 6, 1], [6, 7, 2], [7, 5, 3], [2, 6, 4]]
    print(f"{count_restricted_paths(5, first)} {count_restricted_paths(7, second)}")
    triangle = [[1, 2, 1], [2, 3, 1], [1, 3, 2]]
    square = [[1, 2, 1], [1, 3, 1], [2, 4, 1], [3, 4, 1], [2, 3, 5]]
    print(f"{count_restricted_paths(1, [])} {count_restricted_paths(2, [[1, 2, 7]])} {count_restricted_paths(3, triangle)} {count_restricted_paths(4, square)}")
    line = [[v, v + 1, 100000] for v in range(1, 20000)]
    ladder = []
    for i in range(1, 10001):
        ladder.append([i, i + 10000, 1])
        if i < 10000:
            ladder.append([i, i + 1, 1])
            ladder.append([i + 10000, i + 10001, 1])
    wide = random_graph(20000, 20001, 100000)
    print(f"the most: {count_restricted_paths(20000, line)} {count_restricted_paths(20000, ladder)} {count_restricted_paths(20000, wide)}")
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 12
        extra = next_random() % 13
        edges = random_graph(n, extra, 4)
        check = (check * 31 + count_restricted_paths(n, edges)) % 1000000007
    print(f"2000 random graphs: checksum {check}")


main()
