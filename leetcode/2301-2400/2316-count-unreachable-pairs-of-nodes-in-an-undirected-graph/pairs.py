# LeetCode #2316: Count Unreachable Pairs of Nodes in an Undirected
# Graph -- the Python mirror of the ★ arm. Union-find with union by size
# and path halving, then each set's root, met in order, pairs its size
# with every node of the sets before it.

seed = 2316


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def count_pairs(n, edges):
    parent = list(range(n))
    size = [1] * n
    for a, b in edges:
        ra = find(parent, a)
        rb = find(parent, b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
    before = 0
    pairs = 0
    for x in range(n):
        if parent[x] == x:
            pairs += size[x] * before
            before += size[x]
    return pairs


def graph(n, count):
    edges = []
    seen = set()
    while len(edges) < count:
        a = (next_random() * 32768 + next_random()) % n
        b = (next_random() * 32768 + next_random()) % n
        if a != b and min(a, b) * n + max(a, b) not in seen:
            seen.add(min(a, b) * n + max(a, b))
            edges.append((a, b))
    return edges


print(count_pairs(3, [(0, 1), (0, 2), (1, 2)]))
print(count_pairs(7, [(0, 2), (0, 5), (2, 4), (1, 6), (5, 4)]))
print(count_pairs(1, []))
print(count_pairs(5, []))
print(count_pairs(6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]))
print(count_pairs(2000, [(i - 1, i) for i in range(1, 2000)]))
print(count_pairs(2000, graph(2000, 1000)))
check = 0
total = 0
for _ in range(300):
    n = next_random() % 30 + 1
    count = next_random() % (n + 1)
    pairs = count_pairs(n, graph(n, min(count, n * (n - 1) // 2)))
    check = (check * 31 + pairs) % 1000000007
    total += pairs
print(f"300 graphs: checksum {check}, {total} pairs in all")
