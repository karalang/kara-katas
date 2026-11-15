# LeetCode #2203: Minimum Weighted Subgraph With the Required Paths --
# Python mirror of subgraph.kara (the ★ arm).
import heapq


def dijkstra(adj, frm):
    dist = [-1] * len(adj)
    queue = [(0, frm)]
    while queue:
        d, u = heapq.heappop(queue)
        if dist[u] >= 0:
            continue
        dist[u] = d
        for v, w in adj[u]:
            if dist[v] < 0:
                heapq.heappush(queue, (d + w, v))
    return dist


def minimum_weight(n, edges, src1, src2, dest):
    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]
    for a, b, w in edges:
        forward[a].append((b, w))
        backward[b].append((a, w))
    one = dijkstra(forward, src1)
    two = dijkstra(forward, src2)
    home = dijkstra(backward, dest)
    best = -1
    for v in range(n):
        if one[v] >= 0 and two[v] >= 0 and home[v] >= 0:
            total = one[v] + two[v] + home[v]
            if best < 0 or total < best:
                best = total
    return best


seed = 2203


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    return next_random() * 32768 + next_random()


def random_edges(n, m, top):
    edges = []
    while len(edges) < m:
        frm = wide_random() % n
        to = wide_random() % n
        if frm != to:
            edges.append([frm, to, wide_random() % top + 1])
    return edges


def show(n, edges, src1, src2, dest):
    shown = "[" + ", ".join("[" + ", ".join(map(str, e)) + "]" for e in edges) + "]"
    print(f"n {n}, {shown}, {src1} {src2} -> {dest}: {minimum_weight(n, edges, src1, src2, dest)}")


def main():
    show(6, [[0, 2, 2], [0, 5, 6], [1, 0, 3], [1, 4, 5], [2, 1, 1], [2, 3, 3], [2, 3, 4], [3, 4, 2], [4, 5, 1]], 0, 1, 5)
    show(3, [[0, 1, 1], [2, 1, 1]], 0, 1, 2)
    show(3, [[0, 1, 4], [1, 2, 5]], 0, 1, 2)
    show(4, [[0, 3, 7], [1, 3, 2], [0, 2, 1], [2, 1, 1]], 0, 1, 3)
    show(3, [[0, 2, 9], [0, 2, 3], [1, 2, 5], [1, 2, 8]], 0, 1, 2)
    show(3, [], 0, 1, 2)
    none = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 8 + 3
        m = next_random() % 21
        edges = random_edges(n, m, 10)
        src1 = next_random() % n
        src2 = next_random() % n
        while src2 == src1:
            src2 = next_random() % n
        dest = next_random() % n
        while dest == src1 or dest == src2:
            dest = next_random() % n
        weight = minimum_weight(n, edges, src1, src2, dest)
        if weight < 0:
            none += 1
        check = (check * 31 + weight + 1) % 1000000007
    print(f"2000 graphs: {none} with no subgraph, checksum {check}")
    edges = random_edges(100000, 100000, 100000)
    print(f"n 100000, 100000 edges: {minimum_weight(100000, edges, 0, 1, 2)}")
    ringed = random_edges(100000, 90000, 100000)
    for v in range(10000):
        ringed.append([v * 10, (v * 10 + 10) % 100000, 100000])
    print(f"n 100000, a ring of 10000 and 90000 edges: {minimum_weight(100000, ringed, 0, 50000, 99990)}")


main()
