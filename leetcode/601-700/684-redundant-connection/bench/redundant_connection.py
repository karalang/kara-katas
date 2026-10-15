# LeetCode #684: Redundant Connection -- union-find. Bench.
#
# 100 random trees of 20,000 vertices, each with one more edge, are
# built once; then 30 rounds answer every graph.


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


seed = 684


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 100
    n = 20000
    rounds = 30
    graphs = []
    for _ in range(count):
        name = list(range(1, n + 1))
        i = n - 1
        while i > 0:
            j = next_random() % (i + 1)
            name[i], name[j] = name[j], name[i]
            i -= 1
        up = [0] * n
        edges = []
        for v in range(1, n):
            up[v] = next_random() % v
            edges.append((name[up[v]], name[v]))
        while True:
            x = next_random() % n
            y = next_random() % n
            lo, hi = (x, y) if x < y else (y, x)
            if lo != hi and up[hi] != lo:
                edges.append((name[lo], name[hi]))
                break
        k = n - 1
        while k > 0:
            j = next_random() % (k + 1)
            edges[k], edges[j] = edges[j], edges[k]
            k -= 1
        for e in range(n):
            if next_random() % 2 == 0:
                a, b = edges[e]
                edges[e] = (b, a)
        graphs.append(edges)
    total = 0
    for r in range(rounds):
        for c in range(count):
            a, b = find_redundant_connection(graphs[c])
            total = (total * 31 + a * 20011 + b + r) % 1000000007
    print(f"{count * rounds} graphs answered, checksum {total}")


main()
