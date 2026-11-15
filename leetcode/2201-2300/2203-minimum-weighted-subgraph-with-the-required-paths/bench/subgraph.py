# benchmark's Python mirror of subgraph.kara (LeetCode #2203, the ★ arm):
# three Dijkstras with a heap, the last over the edges turned round, and
# the least sum over the meeting node.
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


def main():
    n = 20000
    graphs = []
    for _ in range(4):
        edges = []
        while len(edges) < 60000:
            frm = wide_random() % n
            to = wide_random() % n
            if frm != to:
                edges.append((frm, to, wide_random() % 100000 + 1))
        graphs.append(edges)
    check = 0
    for _ in range(5):
        for edges in graphs:
            for t in range(4):
                weight = minimum_weight(n, edges, t * 3, t * 3 + 1, t * 3 + 2)
                check = (check * 31 + weight + 1) % 1000000007
    print(f"5 passes over 4 graphs: checksum {check}")


main()
