# LeetCode #2316: Count Unreachable Pairs of Nodes in an Undirected
# Graph -- the bench, the ★ arm in Python. Union-find with union by size
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


n = 100000
graphs = []
for g in range(10):
    edges = []
    for i in range(1, n):
        if next_random() % (g + 3) != 0:
            hi = next_random()
            j = (hi * 32768 + next_random()) % i
            edges.append((i, j))
    graphs.append(edges)
check = 0
for p in range(50):
    for a in range(10):
        check = (check * 31 + count_pairs(n, graphs[(a + p) % 10]) % 1000000007) % 1000000007
print(f"50 passes over 10 graphs of 10^5 nodes: checksum {check}")
