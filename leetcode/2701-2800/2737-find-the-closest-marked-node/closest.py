# LeetCode #2737: Find the Closest Marked Node -- Python mirror of
# closest.kara (the ★ arm): Dijkstra from s with a heap, stopping at the
# first marked node taken off it.

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


def random_edges(n, m, most):
    edges = []
    for _ in range(m):
        u = next_random() % n
        v = (u + 1 + next_random() % (n - 1)) % n
        w = (next_random() * 32768 + next_random()) % most + 1
        edges.append([u, v, w])
    return edges


def random_marked(n, s, k):
    marked = []
    want = next_random() % k + 1
    while len(marked) < want:
        v = next_random() % n
        if v != s and v not in marked:
            marked.append(v)
    return marked


def main():
    print(minimum_distance(4, [[0, 1, 1], [1, 2, 3], [2, 3, 2], [0, 3, 4]], 0, [2, 3]))
    print(minimum_distance(5, [[0, 1, 2], [0, 2, 4], [1, 3, 1], [2, 3, 3], [3, 4, 2]], 1, [0, 4]))
    print(minimum_distance(4, [[0, 1, 1], [1, 2, 3], [2, 3, 2]], 3, [0, 1]))
    print(minimum_distance(500, [[i, i + 1, 1000000] for i in range(499)], 0, [499]))
    total = 0
    check = 0
    for c in range(2020):
        if c < 2000:
            n, m, most = next_random() % 9 + 2, next_random() % 21, 20
        else:
            n, m, most = 500, 10000, 1000000
        edges = random_edges(n, m, most)
        s = next_random() % n
        marked = random_marked(n, s, n - 1)
        distance = minimum_distance(n, edges, s, marked)
        total += distance
        check = (check * 31 + distance + 1) % 1000000007
        if c == 1999:
            print(f"2000 small graphs: distances sum to {total}, checksum {check}")
            total = 0
            check = 0
    print(f"20 graphs of 500 nodes: distances sum to {total}, checksum {check}")


main()
