# LeetCode #1245 bench, in Python: the ★ arm (two breadth-first searches
# over an adjacency list) on 100 random trees of 10000 nodes built once,
# each asked 5 times; every diameter folded into a checksum.
from collections import deque


def farthest(adj, start):
    dist = [-1] * len(adj)
    queue = deque([start])
    dist[start] = 0
    last = start
    while queue:
        node = queue.popleft()
        last = node
        for nxt in adj[node]:
            if dist[nxt] < 0:
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return last, dist[last]


def tree_diameter(edges):
    n = len(edges) + 1
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    end, _ = farthest(adj, 0)
    _, diameter = farthest(adj, end)
    return diameter


seed = 1245


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n, shape):
    label = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        label[i], label[j] = label[j], label[i]
    edges = []
    for v in range(1, n):
        if shape == 0:
            parent = next_random() % v
        elif shape == 1:
            parent = v - 1 - next_random() % min(v, 3)
        else:
            parent = next_random() % min(v, 4)
        edges.append([label[parent], label[v]])
    return edges


def main():
    trees = [random_tree(10000, t % 3) for t in range(100)]
    check = 0
    for _ in range(5):
        for edges in trees:
            check = (check * 131 + tree_diameter(edges)) % 1000000007
    print(f"5 rounds of 100 trees of 10000 nodes: checksum {check}")


main()
