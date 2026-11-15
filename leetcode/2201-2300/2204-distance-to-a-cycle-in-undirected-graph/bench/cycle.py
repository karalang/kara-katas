# benchmark's Python mirror of cycle.kara (LeetCode #2204, the ★ arm):
# leaves peeled by degree, then one breadth-first search from the cycle.
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


def main():
    graphs = [random_graph(100000, ring) for ring in [3, 10, 100, 1000, 10000, 100000]]
    check = 0
    for _ in range(5):
        for edges in graphs:
            dist = distance_to_cycle(100000, edges)
            check = (check * 31 + sum(dist) + dist[len(dist) // 2]) % 1000000007
    print(f"5 passes over 6 graphs: checksum {check}")


main()
