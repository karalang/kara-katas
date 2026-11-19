# LeetCode #1627: Graph Connectivity With Threshold -- the bench's Python
# mirror: the ★ arm on 100 problems of 10000 cities, thresholds 0 to 99,
# each asked the same 100000 queries, all drawn first.


def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        nxt = parent[x]
        parent[x] = root
        x = nxt
    return root


def are_connected(n, threshold, queries):
    parent = list(range(n + 1))
    for z in range(threshold + 1, n + 1):
        for m in range(2 * z, n + 1, z):
            a, b = find(parent, z), find(parent, m)
            if a != b:
                parent[b] = a
    return [find(parent, a) == find(parent, b) for a, b in queries]


seed = 1627


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


n = 10000
thresholds = [next_random() % 100 for _ in range(100)]
queries = []
for _ in range(100000):
    a = next_random() % n + 1
    b = next_random() % n + 1
    queries.append((a, b))
check = 0
total = 0
for threshold in thresholds:
    yes = sum(1 for answer in are_connected(n, threshold, queries) if answer)
    total += yes
    check = (check * 31 + yes + 1) % 1000000007
print(f"100 problems of 10000 cities and 100000 queries: {total} connected, checksum {check}")
