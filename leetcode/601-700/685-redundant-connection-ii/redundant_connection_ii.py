# LeetCode #685: Redundant Connection II -- union-find and two candidates.
# Mirrors the ★ arm (redundant_connection_ii.kara) and its test harness.


def find(parent, x):
    v = x
    while parent[v] != v:
        parent[v] = parent[parent[v]]
        v = parent[v]
    return v


def find_redundant_directed_connection(edges):
    n = len(edges)
    into = [-1] * (n + 1)
    first = -1
    second = -1
    for i in range(n):
        _, b = edges[i]
        if into[b] == -1:
            into[b] = i
        else:
            first = into[b]
            second = i
    parent = list(range(n + 1))
    for i in range(n):
        if i != second:
            a, b = edges[i]
            ra = find(parent, a)
            rb = find(parent, b)
            if ra == rb:
                return edges[i] if first == -1 else edges[first]
            parent[rb] = ra
    return edges[second]


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(edges):
    print(f"{edges} -> {find_redundant_directed_connection(edges)}")


# Whether the parent pointers `up` (0 for the root) make a tree: every
# vertex reaches the root within n steps.
def is_tree(up, n):
    for v in range(1, n + 1):
        w = v
        steps = 0
        while up[w] != 0:
            w = up[w]
            steps += 1
            if steps > n:
                return False
    return True


# A random rooted tree on 1 to n with one more edge, the edges in a
# random order.
def random_graph(rng, n):
    name = list(range(1, n + 1))
    i = n - 1
    while i > 0:
        j = rng.next() % (i + 1)
        name[i], name[j] = name[j], name[i]
        i -= 1
    up = [0] * (n + 1)
    edges = []
    for v in range(1, n):
        a = name[rng.next() % v]
        up[name[v]] = a
        edges.append((a, name[v]))
    while True:
        a = 1 + rng.next() % n
        b = 1 + rng.next() % n
        if a != b and up[b] != a:
            edges.append((a, b))
            break
    k = n - 1
    while k > 0:
        j = rng.next() % (k + 1)
        edges[k], edges[j] = edges[j], edges[k]
        k -= 1
    return edges


def main():
    show([(1, 2), (1, 3), (2, 3)])
    show([(1, 2), (2, 3), (3, 4), (4, 1), (1, 5)])
    show([(2, 1), (3, 1), (4, 2), (1, 4)])
    show([(3, 1), (2, 1), (4, 2), (1, 4)])
    show([(1, 2), (2, 3), (3, 1)])
    show([(3, 1), (1, 2), (2, 3)])
    show([(1, 2), (2, 1), (1, 3)])
    show([(2, 1), (1, 2), (1, 3)])
    show([(4, 1), (1, 2), (2, 3), (3, 4), (1, 5)])
    show([(5, 2), (5, 3), (2, 4), (4, 1), (3, 4)])
    show([(6, 3), (8, 4), (9, 6), (3, 2), (5, 10), (10, 7), (2, 1), (7, 6),
          (4, 5), (2, 8)])

    # Every rooted tree on 3 to 5 vertices with every edge it does not
    # have added, at a place that depends on the edge, the edges listed
    # in order and in reverse.
    graphs = 0
    total_sum = 0
    for n in range(3, 6):
        for code in range((n + 1) ** n):
            up = [0] * (n + 1)
            c = code
            for v in range(1, n + 1):
                up[v] = c % (n + 1)
                c //= n + 1
            if any(up[v] == v for v in range(1, n + 1)):
                continue
            if sum(1 for v in range(1, n + 1) if up[v] == 0) != 1 or not is_tree(up, n):
                continue
            for a in range(1, n + 1):
                for b in range(1, n + 1):
                    if a != b and up[b] != a:
                        edges = [(up[v], v) for v in range(1, n + 1) if up[v] != 0]
                        edges.insert((a * 7 + b) % n, (a, b))
                        graphs += 1
                        p, q = find_redundant_directed_connection(edges)
                        r, s = find_redundant_directed_connection(edges[::-1])
                        total_sum = (total_sum * 31 + p * 1000 + q * 100 + r * 10 + s) % 1000000007
    print(f"rooted trees with one more edge on 3 to 5 vertices: {graphs}, checksum {total_sum}")

    # Random graphs of up to 1,000 vertices.
    rng = Rng(685)
    checksum = 0
    for _ in range(200):
        n = 3 + rng.next() % 998
        a, b = find_redundant_directed_connection(random_graph(rng, n))
        checksum = (checksum * 31 + a * 1009 + b) % 1000000007
    print(f"200 random graphs: checksum {checksum}")


main()
