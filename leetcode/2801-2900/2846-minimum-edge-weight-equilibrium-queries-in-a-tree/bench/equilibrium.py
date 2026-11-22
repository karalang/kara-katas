# LeetCode #2846: Minimum Edge Weight Equilibrium Queries in a Tree --
# the bench, mirrored from equilibrium.kara: weight counts from the
# root by a breadth-first walk, and each query's lowest common ancestor
# by binary lifting.
from collections import deque

seed = 2846


def min_operations_queries(n, edges, queries):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    levels = 15
    up = [[0] * n for _ in range(levels)]
    depth = [0] * n
    count = [[0] * 27 for _ in range(n)]
    seen = [False] * n
    seen[0] = True
    queue = deque([0])
    while queue:
        v = queue.popleft()
        for u, w in adj[v]:
            if not seen[u]:
                seen[u] = True
                up[0][u] = v
                depth[u] = depth[v] + 1
                count[u] = count[v][:]
                count[u][w] += 1
                queue.append(u)
    for j in range(1, levels):
        prev = up[j - 1]
        up[j] = [prev[prev[v]] for v in range(n)]

    def lca(a, b):
        x, y = (a, b) if depth[a] >= depth[b] else (b, a)
        for j in range(levels - 1, -1, -1):
            if depth[x] - (1 << j) >= depth[y]:
                x = up[j][x]
        if x == y:
            return x
        for j in range(levels - 1, -1, -1):
            if up[j][x] != up[j][y]:
                x = up[j][x]
                y = up[j][y]
        return up[0][x]

    answers = []
    for a, b in queries:
        c = lca(a, b)
        on_path = [count[a][w] + count[b][w] - 2 * count[c][w] for w in range(1, 27)]
        answers.append(sum(on_path) - max(on_path))
    return answers


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n, asked, rounds = 10, 10000, 20000, 5
    cases = []
    for _ in range(count):
        label = list(range(n))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            label[i], label[j] = label[j], label[i]
        edges = []
        for i in range(1, n):
            a = label[i]
            b = label[next_random() % i]
            edges.append((a, b, next_random() % 26 + 1))
        queries = []
        for _ in range(asked):
            a = next_random() % n
            queries.append((a, next_random() % n))
        cases.append((edges, queries))
    total = 0
    check = 0
    for r in range(rounds):
        for edges, queries in cases:
            for ops in min_operations_queries(n, edges, queries):
                total += ops
                check = (check * 31 + ops + r) % 1000000007
    print(f"{count} trees of {n}, {asked} queries, {rounds} rounds: {total} operations, checksum {check}")


main()
