# LeetCode #882 bench: Python mirror of reachable_nodes.kara (the ★ arm,
# Dijkstra with a priority queue) on the same 600 graphs.

import heapq


def reachable_nodes(edges, max_moves, n):
    adj = [[] for _ in range(n)]
    for e, (u, v, _) in enumerate(edges):
        adj[u].append(e)
        adj[v].append(e)
    dist = [max_moves + 1] * n
    dist[0] = 0
    queue = [(0, 0)]
    while queue:
        d, u = heapq.heappop(queue)
        if d > dist[u]:
            continue
        for e in adj[u]:
            v = edges[e][0] + edges[e][1] - u
            nxt = d + edges[e][2] + 1
            if nxt < dist[v]:
                dist[v] = nxt
                heapq.heappush(queue, (nxt, v))
    seen = sum(1 for u in range(n) if dist[u] <= max_moves)
    for u, v, cnt in edges:
        from_u = max(max_moves - dist[u], 0)
        from_v = max(max_moves - dist[v], 0)
        seen += min(from_u + from_v, cnt)
    return seen


seed = 882


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(limit):
    x = next_random()
    y = next_random()
    return (x * 32768 + y) % limit


def main():
    total = 0
    check = 0
    for _ in range(600):
        n = 2000 + below(1001)
        offsets = []
        while len(offsets) < 3:
            d = 1 + below(n // 2 - 1)
            if d not in offsets:
                offsets.append(d)
        edges = []
        for u in range(n):
            for k in range(3):
                edges.append([u, (u + offsets[k]) % n, below(10001)])
        max_moves = below(200000)
        reached = reachable_nodes(edges, max_moves, n)
        total += reached
        check = (check * 131 + reached) % 1000000007
    print(f"600 graphs of up to 3000 nodes: {total} nodes reached, checksum {check}")


main()
