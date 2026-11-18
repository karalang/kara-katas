# LeetCode #1617: Count Subtrees With Max Distance Between Cities -- the
# bench in Python, mirroring subtrees.kara: all pair distances by Floyd-Warshall,
# then every mask of two or more cities that holds one road fewer than it
# has cities, its largest distance counted.


def count_subgraphs_for_each_diameter(n, edges):
    far = n + 1
    dist = [[far] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    ends = []
    for a, b in edges:
        a, b = a - 1, b - 1
        dist[a][b] = dist[b][a] = 1
        ends.append((a, b))
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    answer = [0] * (n - 1)
    for mask in range(1, 1 << n):
        size = bin(mask).count("1")
        if size < 2:
            continue
        roads = sum(1 for a, b in ends if mask >> a & 1 and mask >> b & 1)
        if roads != size - 1:
            continue
        widest = 0
        for i in range(n):
            if mask >> i & 1:
                for j in range(i + 1, n):
                    if mask >> j & 1:
                        widest = max(widest, dist[i][j])
        answer[widest - 1] += 1
    return answer


seed = 1617


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def random_tree(n):
    name = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        name[i], name[j] = name[j], name[i]
    edges = []
    for c in range(1, n):
        p = next_random() % c
        edges.append([name[c], name[p]])
    return edges


TREES = 400
trees = [random_tree(15) for _ in range(TREES)]
check = subtrees = 0
for edges in trees:
    for x in count_subgraphs_for_each_diameter(15, edges):
        check = mix(check, x)
        subtrees += x
print(f"{TREES} trees of 15 cities: {subtrees} subtrees, checksum {check}")
