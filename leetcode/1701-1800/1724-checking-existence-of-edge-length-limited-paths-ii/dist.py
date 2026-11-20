# LeetCode #1724: Checking Existence of Edge Length Limited Paths II --
# the Python mirror of the ★ arm, dist.kara: a union-find by rank, never
# compressed, each node keeping the weight of the edge that hung it under
# its parent; a query climbs while the links stay below the limit.

I32_MAX = 2147483647


def root(parent, x):
    while parent[x] != x:
        x = parent[x]
    return x


class DistanceLimitedPathsExist:
    def __init__(self, n, edge_list):
        edges = sorted(edge_list, key=lambda e: e[2])
        self.parent = list(range(n))
        self.joined = [I32_MAX] * n
        rank = [0] * n
        for e in edges:
            a = root(self.parent, e[0])
            b = root(self.parent, e[1])
            if a == b:
                continue
            if rank[a] < rank[b]:
                a, b = b, a
            self.parent[b] = a
            self.joined[b] = e[2]
            if rank[a] == rank[b]:
                rank[a] += 1

    def root_below(self, x, limit):
        while self.joined[x] < limit:
            x = self.parent[x]
        return x

    def query(self, p, q, limit):
        return self.root_below(p, limit) == self.root_below(q, limit)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def wide(seed):
    return next_random(seed) * 32768 + next_random(seed)


def batch(count, nodes, edges, top, queries, seed):
    yes = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % (nodes - 1) + 2
        m = wide(seed) % (edges + 1)
        edge_list = []
        for _ in range(m):
            u = wide(seed) % n
            v = wide(seed) % (n - 1)
            if v >= u:
                v += 1
            edge_list.append([u, v, wide(seed) % top + 1])
        graph = DistanceLimitedPathsExist(n, edge_list)
        for _ in range(queries):
            p = wide(seed) % n
            q = wide(seed) % (n - 1)
            if q >= p:
                q += 1
            limit = wide(seed) % (top + 1) + 1
            answer = graph.query(p, q, limit)
            if answer:
                yes += 1
            check = (check * 31 + (2 if answer else 1)) % 1000000007
    print(f"{count} graphs of up to {nodes} nodes and {edges} edges, {queries} queries each: {yes} paths, checksum {check}")


def main():
    graph = DistanceLimitedPathsExist(6, [[0, 2, 4], [0, 3, 2], [1, 2, 3], [2, 3, 1], [4, 5, 5]])
    for p, q, limit in [(2, 3, 2), (1, 3, 3), (2, 0, 3), (0, 5, 6), (4, 5, 5), (4, 5, 6)]:
        print("true" if graph.query(p, q, limit) else "false")
    seed = [1724]
    batch(3000, 8, 10, 6, 10, seed)
    batch(100, 1000, 1500, 1000000000, 100, seed)
    batch(4, 3000, 10000, 1000000000, 1000, seed)


main()
