# LeetCode #323: Number of Connected Components in an Undirected Graph.
# Python mirror of count_components.kara (union-find, union by size, path
# compression). Same cases, same LCG, same output.


class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.sets = n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        cur = x
        while self.parent[cur] != root:
            nxt = self.parent[cur]
            self.parent[cur] = root
            cur = nxt
        return root

    def merge(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.sets -= 1


def count_components(n, edges):
    ds = DisjointSet(n)
    for a, b in edges:
        ds.merge(a, b)
    return ds.sets


def show(edges):
    return "[" + ", ".join(f"({a}, {b})" for a, b in edges) + "]"


def report(n, edges):
    print(f"n={n} edges={show(edges)} -> {count_components(n, edges)}")


class Lcg:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_edges(n, m, rng):
    edges = []
    for _ in range(m):
        a = rng.next() % n
        b = rng.next() % n
        edges.append((a, b))
    return edges


def main():
    report(5, [(0, 1), (1, 2), (3, 4)])
    report(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
    report(1, [])
    report(4, [])
    report(3, [(2, 2)])
    report(3, [(0, 1), (0, 1), (1, 0)])
    report(4, [(0, 1), (1, 2), (2, 0)])
    report(6, [(0, 1), (1, 2), (3, 4), (4, 5), (5, 3), (2, 3)])
    report(7, [(3, 0), (3, 1), (3, 2), (3, 4), (3, 5)])
    report(6, [(4, 5), (3, 4), (2, 3), (1, 2)])
    report(8, [(2, 3), (4, 5)])

    rng = Lcg(323)
    for t, n in enumerate([6, 9, 12]):
        edges = random_edges(n, n // 2 + t, rng)
        report(n, edges)

    for t, n in enumerate([1000, 20000, 100000]):
        m = n // 2 + t * n // 4
        edges = random_edges(n, m, rng)
        print(f"n={n} m={m} -> {count_components(n, edges)}")


main()
