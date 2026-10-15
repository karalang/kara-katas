# LeetCode #685: Redundant Connection II -- union-find and two
# candidates. Bench.
#
# 100 random rooted trees of 20,000 vertices, each with one more directed
# edge, are built once; then 30 rounds answer every graph.


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


seed = 685


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
        up = [0] * (n + 1)
        edges = []
        for v in range(1, n):
            a = name[next_random() % v]
            up[name[v]] = a
            edges.append((a, name[v]))
        while True:
            a = 1 + next_random() % n
            b = 1 + next_random() % n
            if a != b and up[b] != a:
                edges.append((a, b))
                break
        k = n - 1
        while k > 0:
            j = next_random() % (k + 1)
            edges[k], edges[j] = edges[j], edges[k]
            k -= 1
        graphs.append(edges)
    total = 0
    for r in range(rounds):
        for c in range(count):
            a, b = find_redundant_directed_connection(graphs[c])
            total = (total * 31 + a * 20011 + b + r) % 1000000007
    print(f"{count * rounds} graphs answered, checksum {total}")


main()
