# LeetCode #2204: Distance to a Cycle in Undirected Graph -- Python mirror
# of cycle.kara (the ★ arm).
from collections import deque


def distance_to_cycle(n, edges):
    adj = [[] for _ in range(n)]
    degree = [0] * n
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        degree[a] += 1
        degree[b] += 1
    leaves = deque(v for v in range(n) if degree[v] == 1)
    peeled = [False] * n
    while leaves:
        v = leaves.popleft()
        peeled[v] = True
        for u in adj[v]:
            degree[u] -= 1
            if degree[u] == 1:
                leaves.append(u)
    dist = [-1] * n
    frontier = deque()
    for v in range(n):
        if not peeled[v]:
            dist[v] = 0
            frontier.append(v)
    while frontier:
        v = frontier.popleft()
        for u in adj[v]:
            if dist[u] < 0:
                dist[u] = dist[v] + 1
                frontier.append(u)
    return dist


seed = 2204


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    return next_random() * 32768 + next_random()


def random_graph(n, ring):
    order = list(range(n))
    for i in range(n - 1, 0, -1):
        j = wide_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    edges = []
    for i in range(ring):
        edges.append([order[i], order[(i + 1) % ring]])
    for i in range(ring, n):
        edges.append([order[i], order[wide_random() % i]])
    for i in range(n - 1, 0, -1):
        j = wide_random() % (i + 1)
        edges[i], edges[j] = edges[j], edges[i]
    for i in range(n):
        if next_random() % 2 == 1:
            edges[i] = [edges[i][1], edges[i][0]]
    return edges


def fmt(v):
    return "[" + ", ".join(fmt(x) if isinstance(x, list) else str(x) for x in v) + "]"


def show(n, edges):
    print(f"n {n}, {fmt(edges)} -> {fmt(distance_to_cycle(n, edges))}")


def main():
    show(7, [[1, 2], [2, 4], [4, 3], [3, 1], [0, 1], [5, 2], [6, 5]])
    show(9, [[0, 1], [1, 2], [0, 2], [2, 6], [6, 7], [6, 8], [0, 3], [3, 4], [3, 5]])
    show(3, [[0, 1], [1, 2], [2, 0]])
    show(6, [[5, 4], [4, 3], [3, 2], [2, 0], [0, 1], [1, 2]])
    show(8, [[0, 1], [1, 2], [2, 3], [3, 0], [4, 0], [5, 0], [6, 2], [7, 6]])
    show(5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]])
    far = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 10 + 3
        ring = next_random() % (n - 2) + 3
        for d in distance_to_cycle(n, random_graph(n, ring)):
            far = max(far, d)
            check = (check * 31 + d) % 1000000007
    print(f"2000 graphs: farthest {far}, checksum {check}")
    for ring in [3, 1000, 100000]:
        dist = distance_to_cycle(100000, random_graph(100000, ring))
        print(f"n 100000, cycle {ring}: farthest {max(dist)}, total {sum(dist)}")
    path = [[0, 1], [1, 2], [2, 0]] + [[v - 1, v] for v in range(3, 100000)]
    dist = distance_to_cycle(100000, path)
    print(f"n 100000, a path off a triangle: farthest {dist[99999]}, total {sum(dist)}")


main()
