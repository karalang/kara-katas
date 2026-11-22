# LeetCode #2737: Find the Closest Marked Node -- the bench (closest.kara
# in Python): Dijkstra from s with heapq, stopping at the first marked
# node taken off it.

import heapq


def minimum_distance(n, edges, s, marked):
    out = [[] for _ in range(n)]
    for u, v, w in edges:
        out[u].append((v, w))
    is_marked = [False] * n
    for v in marked:
        is_marked[v] = True
    dist = [float("inf")] * n
    dist[s] = 0
    queue = [(0, s)]
    while queue:
        d, u = heapq.heappop(queue)
        if d > dist[u]:
            continue
        if is_marked[u]:
            return d
        for v, w in out[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(queue, (d + w, v))
    return -1


seed = 2737


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    graphs, n, m, rounds = 50, 500, 10000, 20
    problems = []
    for _ in range(graphs):
        edges = []
        for _ in range(m):
            u = next_random() % n
            v = (u + 1 + next_random() % (n - 1)) % n
            w = (next_random() * 32768 + next_random()) % 1000000 + 1
            edges.append((u, v, w))
        s = next_random() % n
        marked = []
        want = next_random() % 3 + 1
        while len(marked) < want:
            v = next_random() % n
            if v != s and v not in marked:
                marked.append(v)
        problems.append((edges, s, marked))
    total = 0
    check = 0
    for r in range(rounds):
        for edges, s, marked in problems:
            distance = minimum_distance(n, edges, s, marked)
            total += distance
            check = (check * 31 + distance + 1 + r) % 1000000007
    print(f"{graphs} graphs of {n} nodes and {m} edges, {rounds} rounds: distances sum to {total}, checksum {check}")


main()
