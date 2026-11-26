# LeetCode #1761: Minimum Degree of a Connected Trio in a Graph -- the bench
# in Python, mirroring min_trio_degree.kara: an adjacency matrix, the
# degrees, and every edge (u, v) with each w above v.
def min_trio_degree(n, edges):
    joined = [[False] * (n + 1) for _ in range(n + 1)]
    degree = [0] * (n + 1)
    for u, v in edges:
        joined[u][v] = joined[v][u] = True
        degree[u] += 1
        degree[v] += 1
    best = None
    for u in range(1, n + 1):
        ju = joined[u]
        for v in range(u + 1, n + 1):
            if not ju[v]:
                continue
            jv = joined[v]
            for w in range(v + 1, n + 1):
                if ju[w] and jv[w]:
                    d = degree[u] + degree[v] + degree[w] - 6
                    if best is None or d < best:
                        best = d
    return -1 if best is None else best


def main():
    seed = 1761
    weights = []
    for u in range(1, 401):
        for v in range(u + 1, 401):
            seed = (seed * 1103515245 + 12345) % 2147483648
            weights.append((u, v, seed // 65536 % 1000))
    check = 0
    for call in range(40):
        threshold = 300 + (check + call * 7919) % 500
        edges = [[u, v] for u, v, w in weights if w < threshold]
        check = (check * 31 + min_trio_degree(400, edges) + 1) % 1000000007
    print(f"40 calls on 400 nodes: checksum {check}")


main()
