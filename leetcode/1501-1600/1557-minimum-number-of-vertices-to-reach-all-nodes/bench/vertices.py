# LeetCode #1557: Minimum Number of Vertices to Reach All Nodes -- bench:
# the ★ arm (the nodes no edge ends at) over 20 acyclic graphs of 100000
# nodes and up to 300000 edges, built once, each asked 20 times. Python mirror of vertices.kara.


def find_smallest_set_of_vertices(n, edges):
    reached = [False] * n
    for _, to in edges:
        reached[to] = True
    return [v for v in range(n) if not reached[v]]


seed = 1557


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 100000
    graphs = []
    for _ in range(20):
        order = list(range(n))
        for i in range(n - 1, 0, -1):
            j = (next_random() * 32768 + next_random()) % (i + 1)
            order[i], order[j] = order[j], order[i]
        edges = []
        for _ in range(300000):
            a = (next_random() * 32768 + next_random()) % n
            b = (next_random() * 32768 + next_random()) % n
            if a < b:
                edges.append((order[a], order[b]))
        graphs.append(edges)
    check = 0
    total = 0
    for p in range(20):
        for g in range(len(graphs)):
            sources = find_smallest_set_of_vertices(n, graphs[g])
            total += len(sources)
            check = mix(check, sources[(p * 7 + g) % len(sources)])
    print(f"20 passes over 20 graphs of 100000 nodes: {total} sources, checksum {check}")


main()
