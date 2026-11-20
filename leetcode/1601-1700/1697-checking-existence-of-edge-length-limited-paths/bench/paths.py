# LeetCode #1697: Checking Existence of Edge Length Limited Paths -- the
# bench's Python mirror: the ★ arm on 10 random graphs of 100000 nodes,
# 100000 edges and 100000 queries, lengths and limits up to 10^9, all
# drawn first, each answered 5 times.


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


seed = 1697


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide(bound):
    hi = next_random()
    return (hi * 32768 + next_random()) % bound


def triples(count, n):
    out = []
    for _ in range(count):
        u = wide(n)
        v = (u + 1 + wide(n - 1)) % n
        out.append([u, v, wide(1000000000) + 1])
    return out


def main():
    count, rounds, n = 10, 5, 100000
    graphs = []
    for _ in range(count):
        edges = triples(n, n)
        queries = triples(n, n)
        graphs.append((edges, queries))
    trues = 0
    check = 0
    for r in range(rounds):
        for edges, queries in graphs:
            for a in distance_limited_paths_exist(n, edges, queries):
                if a:
                    trues += 1
                check = (check * 31 + (2 if a else 1) + r) % 1000000007
    print(f"{count} graphs of {n} nodes, edges and queries, {rounds} rounds: {trues} true, checksum {check}")


main()
