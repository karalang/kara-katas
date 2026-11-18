# LeetCode #1192 bench: the ★ arm in Python, over the same 4 networks and
# 10 rounds as the Kāra bench.


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


seed = 1192


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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



path = [[i, i + 1] for i in range(99999)]
ring = path + [[99999, 0]]
networks = [
    (50000, random_network(50000, 50001)),
    (100000, random_network(100000, 0)),
    (100000, path),
    (100000, ring),
]
check = 0
for _ in range(10):
    for n, edges in networks:
        bridges = critical_connections(n, edges)
        check = (check * 131 + len(bridges)) % 1000000007
        for a, b in bridges:
            check = (check * 131 + a * 100003 + b) % 1000000007
print(f"10 rounds of 4 networks of up to 100000 servers: checksum {check}")
