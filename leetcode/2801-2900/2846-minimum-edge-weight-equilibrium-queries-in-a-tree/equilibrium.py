# LeetCode #2846: Minimum Edge Weight Equilibrium Queries in a Tree --
# the Python mirror of the ★ arm: weight counts from the root by a
# breadth-first walk, and each query's lowest common ancestor by binary
# lifting.
from collections import deque


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
        for v in range(n):
            up[j][v] = up[j - 1][up[j - 1][v]]

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


# ---- the harness: the same in every arm --------------------------------

seed = 2846


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def tree(n, kinds):
    label = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        label[i], label[j] = label[j], label[i]
    edges = []
    for i in range(1, n):
        a = label[i]
        b = label[next_random() % i]
        edges.append([a, b, next_random() % kinds + 1])
    return edges


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    m = min_operations_queries
    print(show(m(7, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 2], [4, 5, 2], [5, 6, 2]], [[0, 3], [3, 6], [2, 6], [0, 6]])))
    print(show(m(8, [[1, 2, 6], [1, 3, 4], [2, 4, 6], [2, 5, 3], [3, 6, 6], [3, 0, 8], [7, 0, 2]], [[4, 6], [0, 4], [6, 5], [7, 4]])))
    print(show(m(1, [], [[0, 0]])))
    path = [[i - 1, i, i // 300 % 26 + 1] for i in range(1, 2000)]
    print(show(m(2000, path, [[0, 1999], [1999, 0], [1000, 1000], [999, 1300]])))
    check = 0
    total = 0
    for c in range(2020):
        short = c < 2000
        n = next_random() % 10 + 1 if short else next_random() % 2000 + 1
        edges = tree(n, 3 if short else 26)
        asked = 5 if short else 500
        queries = []
        for _ in range(asked):
            a = next_random() % n
            queries.append([a, next_random() % n])
        for ops in m(n, edges, queries):
            total += ops
            check = (check * 31 + ops) % 1000000007
        if c == 1999:
            print(f"2000 small trees: {total} operations, checksum {check}")
            total = 0
            check = 0
    print(f"20 large trees: {total} operations, checksum {check}")


main()
