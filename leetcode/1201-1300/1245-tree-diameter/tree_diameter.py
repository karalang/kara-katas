# LeetCode #1245: Tree Diameter -- mirrors tree_diameter.kara.
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
    first = tree_diameter([[0, 1], [0, 2]])
    second = tree_diameter([[0, 1], [1, 2], [2, 3], [1, 4], [4, 5]])
    print(f"{first} {second}")
    total = 0
    check = 0
    for t in range(1000):
        n = next_random() % 300 + 1
        d = tree_diameter(random_tree(n, t % 3))
        total += d
        check = (check * 131 + d) % 1000000007
    print(f"1000 random trees: total {total}, checksum {check}")
    path = [[v - 1, v] for v in range(1, 10000)]
    tops = [tree_diameter(path)]
    for shape in range(3):
        tops.append(tree_diameter(random_tree(10000, shape)))
    print(f"10000 nodes: path {tops[0]}, random {tops[1]}, stringy {tops[2]}, bushy {tops[3]}")


main()
