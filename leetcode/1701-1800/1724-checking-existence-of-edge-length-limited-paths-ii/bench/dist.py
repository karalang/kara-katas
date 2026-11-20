# LeetCode #1724: Checking Existence of Edge Length Limited Paths II --
# the bench (dist.kara): a union-find by rank, never compressed, each
# node keeping the weight of the edge that hung it under its parent; a
# query climbs from each node while the links stay below the limit.

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


def main():
    count = 20
    rounds = 50
    n = 10000
    m = 10000
    asked = 10000
    top = 1000000000
    seed = [1724]
    problems = []
    for _ in range(count):
        edge_list = []
        for _ in range(m):
            u = wide(seed) % n
            v = wide(seed) % (n - 1)
            if v >= u:
                v += 1
            edge_list.append([u, v, wide(seed) % top + 1])
        queries = []
        for _ in range(asked):
            p = wide(seed) % n
            q = wide(seed) % (n - 1)
            if q >= p:
                q += 1
            queries.append((p, q, wide(seed) % top + 1))
        problems.append((edge_list, queries))
    yes = 0
    check = 0
    for r in range(rounds):
        for edge_list, queries in problems:
            graph = DistanceLimitedPathsExist(n, edge_list)
            for p, q, limit in queries:
                answer = graph.query(p, q, limit)
                if answer:
                    yes += 1
                check = (check * 31 + (2 if answer else 1) + r) % 1000000007
    print(f"{count} graphs of {n} nodes and {m} edges, {asked} queries each, {rounds} rounds: {yes} paths, checksum {check}")


main()
