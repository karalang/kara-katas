# LeetCode #2421: Number of Good Paths -- the bench, the ★ arm: union-find
# over the nodes in order of value, each value's nodes joined to their
# neighbours no larger and then counted by root.

seed = 2421


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def number_of_good_paths(vals, edges):
    n = len(vals)
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent = list(range(n))
    order = sorted(range(n), key=lambda i: vals[i])
    good = n
    i = 0
    while i < n:
        j = i
        while j < n and vals[order[j]] == vals[order[i]]:
            j += 1
        for t in range(i, j):
            u = order[t]
            for v in adj[u]:
                if vals[v] <= vals[u]:
                    ru = find(parent, u)
                    rv = find(parent, v)
                    parent[ru] = rv
        count = {}
        for t in range(i, j):
            root = find(parent, order[t])
            count[root] = count.get(root, 0) + 1
        for c in count.values():
            good += c * (c - 1) // 2
        i = j
    return good


def main():
    trees = []
    for t in range(10):
        n = 30000
        vals = [1 + next_random() % (3 + 1000 * t) for _ in range(n)]
        edges = [(next_random() % i, i) for i in range(1, n)]
        trees.append((vals, edges))
    check = 0
    for p in range(20):
        for vals, edges in trees:
            check = (check * 31 + number_of_good_paths(vals, edges) + p) % 1000000007
    print(f"20 passes over 10 trees of 3 * 10^4 nodes: checksum {check}")


main()
