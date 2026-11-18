# LeetCode #1192: Critical Connections in a Network -- the ★ arm in Python:
# Tarjan's low-link search with an explicit stack. It also checks every
# answer for the random networks against the statement read literally: a
# connection is critical when, without it, some server cannot reach another.
import sys

sys.setrecursionlimit(10000)


def critical_connections(n, connections):
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(connections):
        adj[a].append((b, i))
        adj[b].append((a, i))
    disc = [-1] * n
    low = [0] * n
    bridges = []
    disc[0] = 0
    time = 1
    stack = [[0, -1, 0]]
    while stack:
        top = stack[-1]
        u, via, nxt = top
        if nxt < len(adj[u]):
            top[2] = nxt + 1
            v, i = adj[u][nxt]
            if i == via:
                continue
            if disc[v] == -1:
                disc[v] = low[v] = time
                time += 1
                stack.append([v, i, 0])
            else:
                low[u] = min(low[u], disc[v])
        else:
            stack.pop()
            if stack:
                p = stack[-1][0]
                low[p] = min(low[p], low[u])
                if low[u] > disc[p]:
                    bridges.append([p, u])
    return bridges


def literal(n, connections):
    out = []
    for skip in range(len(connections)):
        adj = [[] for _ in range(n)]
        for i, (a, b) in enumerate(connections):
            if i != skip:
                adj[a].append(b)
                adj[b].append(a)
        seen = {0}
        todo = [0]
        while todo:
            for v in adj[todo.pop()]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        if len(seen) < n:
            out.append(connections[skip])
    return out


seed = 1192


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def normalized(bridges):
    return sorted((min(a, b), max(a, b)) for a, b in bridges)


def fold(check, bridges):
    h = (check * 131 + len(bridges)) % 1000000007
    for a, b in bridges:
        h = (h * 131 + a * 100003 + b) % 1000000007
    return h


def random_network(n, extra):
    joined = set()
    edges = []
    for v in range(1, n):
        u = next_random() % v
        joined.add((u, v))
        edges.append([u, v])
    for _ in range(extra):
        a = next_random() % n
        b = next_random() % n
        key = (min(a, b), max(a, b))
        if a != b and key not in joined:
            joined.add(key)
            edges.append([a, b])
    return edges


def show_edges(edges):
    return "[" + ", ".join(f"[{a}, {b}]" for a, b in edges) + "]"


def show_pairs(pairs):
    return "[" + ", ".join(f"({a}, {b})" for a, b in pairs) + "]"


cases = [
    (4, [[0, 1], [1, 2], [2, 0], [1, 3]]),
    (2, [[0, 1]]),
    (5, [[0, 1], [1, 2], [2, 3], [3, 4]]),
    (5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]]),
    (6, [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5], [5, 3]]),
    (5, [[0, 1], [0, 2], [0, 3], [0, 4]]),
    (6, [[3, 4], [4, 5], [5, 3], [0, 1], [1, 2], [2, 3]]),
]
for n, edges in cases:
    got = normalized(critical_connections(n, edges))
    assert got == normalized(literal(n, edges))
    print(f"n={n} {show_edges(edges)}: {show_pairs(got)}")
check = total = 0
for _ in range(2000):
    n = next_random() % 8 + 2
    extra = next_random() % (n + 1)
    edges = random_network(n, extra)
    bridges = normalized(critical_connections(n, edges))
    assert bridges == normalized(literal(n, edges)), (n, edges)
    total += len(bridges)
    check = fold(check, bridges)
print(f"2000 random networks: {total} critical, checksum {check}")
path = [[i, i + 1] for i in range(99999)]
bridges = normalized(critical_connections(100000, path))
print(f"path of 100000: {len(bridges)} critical, checksum {fold(0, bridges)}")
ring = path + [[99999, 0]]
print(f"cycle of 100000: {len(critical_connections(100000, ring))} critical")
big = random_network(50000, 50001)
bridges = normalized(critical_connections(50000, big))
print(f"50000 servers, {len(big)} connections: {len(bridges)} critical, checksum {fold(0, bridges)}")
