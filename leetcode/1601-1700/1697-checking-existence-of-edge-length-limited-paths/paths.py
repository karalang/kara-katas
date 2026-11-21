# LeetCode #1697: Checking Existence of Edge Length Limited Paths --
# mirrors paths.kara, the ★ arm: the queries answered offline, by rising
# limit, over a union-find.


def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    at = x
    while parent[at] != root:
        nxt = parent[at]
        parent[at] = root
        at = nxt
    return root


def distance_limited_paths_exist(n, edge_list, queries):
    edges = sorted(edge_list, key=lambda e: e[2])
    order = sorted(range(len(queries)), key=lambda i: queries[i][2])
    parent = list(range(n))
    answer = [False] * len(queries)
    joined = 0
    for i in order:
        limit = queries[i][2]
        while joined < len(edges) and edges[joined][2] < limit:
            a = find(parent, edges[joined][0])
            b = find(parent, edges[joined][1])
            parent[a] = b
            joined += 1
        answer[i] = find(parent, queries[i][0]) == find(parent, queries[i][1])
    return answer


def show(answer):
    return "[" + ", ".join("true" if a else "false" for a in answer) + "]"


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, top, seed):
    trues = 0
    check = 0
    for _ in range(count):
        n = seed.next() % (most - 1) + 2
        edges = []
        for _ in range(seed.next() % (2 * most) + 1):
            u = seed.next() % n
            v = (u + 1 + seed.next() % (n - 1)) % n
            edges.append([u, v, (seed.next() * 32768 + seed.next()) % top + 1])
        queries = []
        for _ in range(seed.next() % most + 1):
            p = seed.next() % n
            q = (p + 1 + seed.next() % (n - 1)) % n
            queries.append([p, q, (seed.next() * 32768 + seed.next()) % top + 1])
        for a in distance_limited_paths_exist(n, edges, queries):
            if a:
                trues += 1
            check = (check * 31 + (2 if a else 1)) % 1000000007
    print(f"{count} graphs of up to {most} nodes, lengths up to {top}: {trues} true, checksum {check}")


def main():
    print(show(distance_limited_paths_exist(3, [[0, 1, 2], [1, 2, 4], [2, 0, 8], [1, 0, 16]], [[0, 1, 2], [0, 2, 5]])))
    print(show(distance_limited_paths_exist(5, [[0, 1, 10], [1, 2, 5], [2, 3, 9], [3, 4, 13]], [[0, 4, 14], [1, 4, 13]])))
    print(show(distance_limited_paths_exist(2, [[0, 1, 3]], [[0, 1, 3], [1, 0, 4]])))
    print(show(distance_limited_paths_exist(2, [[0, 1, 7], [1, 0, 2]], [[0, 1, 3], [0, 1, 2]])))
    seed = Seed(1697)
    batch(3000, 6, 5, seed)
    batch(300, 100, 100, seed)
    batch(10, 2000, 1000000000, seed)


main()
