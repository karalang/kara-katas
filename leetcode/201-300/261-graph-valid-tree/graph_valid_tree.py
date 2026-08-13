"""LeetCode 261 — Graph Valid Tree (Python mirror / oracle).

Mirrors graph_valid_tree.kara algorithm-for-algorithm: union-find with union by
size and path compression, rejecting the first edge whose endpoints already
share a root, then requiring a single component.
"""


def find(parent, x):
    r = x
    while parent[r] != r:
        r = parent[r]
    c = x
    while parent[c] != r:
        parent[c], c = r, parent[c]
    return r


def valid_tree(n, edges):
    parent = list(range(n))
    size = [1] * n
    components = n
    for u, v in edges:
        ra, rb = find(parent, u), find(parent, v)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            parent[ra] = rb
            size[rb] += size[ra]
        else:
            parent[rb] = ra
            size[ra] += size[rb]
        components -= 1
    return components == 1


def report(label, n, edges):
    print(f"{label} -> {'true' if valid_tree(n, edges) else 'false'}")


def main():
    report("n=1 []", 1, [])
    report("n=2 []", 2, [])
    report("n=5 star", 5, [[0, 1], [0, 2], [0, 3], [0, 4]])
    report("n=5 path", 5, [[0, 1], [1, 2], [2, 3], [3, 4]])
    report("n=4 cycle", 4, [[0, 1], [1, 2], [2, 3], [0, 3]])
    report("n=4 triangle + isolated", 4, [[0, 1], [1, 2], [0, 2]])
    report("n=5 forest", 5, [[0, 1], [2, 3], [3, 4]])
    report("n=5 path, shuffled edges", 5, [[3, 4], [0, 1], [2, 3], [1, 2]])


main()
