# LeetCode #684: Redundant Connection -- union-find.
# Mirrors the ★ arm (redundant_connection.kara) and its test harness.


def find(parent, x):
    v = x
    while parent[v] != v:
        parent[v] = parent[parent[v]]
        v = parent[v]
    return v


def find_redundant_connection(edges):
    n = len(edges)
    parent = list(range(n + 1))
    size = [1] * (n + 1)
    for a, b in edges:
        ra = find(parent, a)
        rb = find(parent, b)
        if ra == rb:
            return (a, b)
        if size[ra] < size[rb]:
            parent[ra] = rb
            size[rb] += size[ra]
        else:
            parent[rb] = ra
            size[ra] += size[rb]
    return (0, 0)


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(edges):
    print(f"{edges} -> {find_redundant_connection(edges)}")


# Whether the edges connect the vertices 1 to n.
def connects(edges, n):
    label = list(range(n + 1))
    for a, b in edges:
        frm, to = label[a], label[b]
        if frm != to:
            for v in range(1, n + 1):
                if label[v] == frm:
                    label[v] = to
    return all(label[v] == label[1] for v in range(2, n + 1))


# A random tree on 1 to n with one more edge, the edges in a random order
# and each written either way round.
def random_graph(rng, n):
    name = list(range(1, n + 1))
    i = n - 1
    while i > 0:
        j = rng.next() % (i + 1)
        name[i], name[j] = name[j], name[i]
        i -= 1
    edges = []
    joined = set()
    for v in range(1, n):
        u = rng.next() % v
        edges.append((name[u], name[v]))
        joined.add((name[u], name[v]))
        joined.add((name[v], name[u]))
    while True:
        a = name[rng.next() % n]
        b = name[rng.next() % n]
        if a != b and (a, b) not in joined:
            edges.append((a, b))
            break
    k = n - 1
    while k > 0:
        j = rng.next() % (k + 1)
        edges[k], edges[j] = edges[j], edges[k]
        k -= 1
    for e in range(n):
        if rng.next() % 2 == 0:
            a, b = edges[e]
            edges[e] = (b, a)
    return edges


def main():
    show([(1, 2), (1, 3), (2, 3)])
    show([(1, 2), (2, 3), (3, 4), (1, 4), (1, 5)])
    show([(2, 3), (1, 3), (1, 2)])
    show([(3, 1), (2, 1), (3, 2)])
    show([(1, 4), (3, 4), (1, 3), (1, 2), (4, 5)])
    show([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)])
    show([(2, 1), (3, 1), (4, 2), (1, 4)])
    show([(1, 5), (3, 4), (3, 5), (4, 5), (2, 4)])
    show([(9, 10), (5, 8), (2, 6), (1, 5), (3, 8), (4, 9), (8, 10),
          (4, 10), (6, 8), (7, 9)])

    # Every tree on 3 to 6 vertices with one more edge, the edges listed
    # in order and in reverse.
    graphs = 0
    total = 0
    for n in range(3, 7):
        pairs = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1)]
        m = len(pairs)
        for mask in range(1 << m):
            if bin(mask).count("1") == n:
                edges = [pairs[k] for k in range(m) if (mask >> k) & 1 == 1]
                if connects(edges, n):
                    graphs += 1
                    a, b = find_redundant_connection(edges)
                    c, d = find_redundant_connection(edges[::-1])
                    total = (total * 31 + a * 1000 + b * 100 + c * 10 + d) % 1000000007
    print(f"trees with one more edge on 3 to 6 vertices: {graphs}, checksum {total}")

    # Random graphs of up to 1,000 vertices.
    rng = Rng(684)
    checksum = 0
    for _ in range(200):
        n = 3 + rng.next() % 998
        a, b = find_redundant_connection(random_graph(rng, n))
        checksum = (checksum * 31 + a * 1009 + b) % 1000000007
    print(f"200 random graphs: checksum {checksum}")


main()
