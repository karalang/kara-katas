# LeetCode #882: Reachable Nodes In Subdivided Graph -- Python mirror of
# the ★ arm (Dijkstra with a priority queue) and its test harness; prints
# the same output as reachable_nodes.kara.

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


# ---- test harness ----------------------------------------------------------


def text(edges):
    if len(edges) > 5:
        return f"[[{edges[0][0]}, {edges[0][1]}, {edges[0][2]}], ... ({len(edges)} edges)]"
    return "[" + ", ".join(f"[{u}, {v}, {c}]" for u, v, c in edges) + "]"


def show(edges, max_moves, n):
    print(f"edges = {text(edges)}, maxMoves = {max_moves}, n = {n} -> {reachable_nodes(edges, max_moves, n)}")


seed = 882


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(limit):
    x = next_random()
    y = next_random()
    return (x * 32768 + y) % limit


def graph(n, m, most):
    used = set()
    edges = []
    for _ in range(m):
        u = below(n)
        v = below(n)
        key = min(u, v) * n + max(u, v)
        if u != v and key not in used:
            used.add(key)
            edges.append([min(u, v), max(u, v), below(most)])
    return edges


def main():
    show([[0, 1, 10], [0, 2, 1], [1, 2, 2]], 6, 3)
    show([[0, 1, 4], [1, 2, 6], [0, 2, 8], [1, 3, 1]], 10, 4)
    show([[1, 2, 4], [1, 4, 5], [1, 3, 1], [2, 3, 4], [3, 4, 5]], 17, 5)
    show([], 5, 1)
    show([[0, 1, 3]], 0, 2)
    show([[0, 1, 3]], 4, 2)
    show([[0, 1, 3]], 2, 2)
    show([[0, 1, 0], [1, 2, 0], [2, 3, 0]], 2, 4)
    show([[0, 1, 10000]], 1000000000, 2)
    total = 0
    for _ in range(2000):
        n = next_random() % 8 + 1
        edges = graph(n, next_random() % 12, 6)
        total += reachable_nodes(edges, next_random() % 15, n)
    print(f"2000 cases of up to 8 nodes: {total} nodes reached")
    total = 0
    check = 0
    for k in range(12):
        n = 1000 + below(2001)
        edges = graph(n, 10000, 10001)
        max_moves = below(1000000001) if k % 3 == 0 else below(100000)
        reached = reachable_nodes(edges, max_moves, n)
        total += reached
        check = (check * 131 + reached) % 1000000007
    print(f"12 cases of up to 3000 nodes: {total} nodes reached, checksum {check}")


main()
