# LeetCode #1761: Minimum Degree of a Connected Trio in a Graph -- the ★ arm
# in Python, with the same harness.
def min_trio_degree(n, edges):
    joined = [[False] * (n + 1) for _ in range(n + 1)]
    degree = [0] * (n + 1)
    for u, v in edges:
        joined[u][v] = joined[v][u] = True
        degree[u] += 1
        degree[v] += 1
    best = None
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if not joined[u][v]:
                continue
            for w in range(v + 1, n + 1):
                if joined[u][w] and joined[v][w]:
                    d = degree[u] + degree[v] + degree[w] - 6
                    best = d if best is None or d < best else best
    return -1 if best is None else best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_graph(n, density):
    edges = []
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if next_random() % 1000 < density:
                edges.append([u, v])
    return edges


def main():
    global seed
    print(f"{min_trio_degree(6, [[1, 2], [1, 3], [3, 2], [4, 1], [5, 2], [3, 6]])} {min_trio_degree(7, [[1, 3], [4, 1], [4, 3], [2, 5], [5, 6], [6, 7], [7, 5], [2, 6]])}")
    print(" ".join(str(min_trio_degree(n, e)) for n, e in [
        (3, [[1, 2], [2, 3]]), (3, [[1, 2], [2, 3], [1, 3]]), (4, [[1, 2], [2, 3], [3, 4], [4, 1]]),
        (5, [[1, 2], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5], [3, 4], [3, 5], [4, 5]]),
        (5, [[1, 2], [2, 3], [1, 3], [3, 4], [4, 5]])]))
    seed = 1761
    sparse = random_graph(400, 4)
    middling = random_graph(400, 50)
    dense = random_graph(400, 500)
    print(f"400 nodes: {min_trio_degree(400, sparse)} {min_trio_degree(400, middling)} {min_trio_degree(400, dense)}")
    check = 0
    for _ in range(3000):
        n = 2 + next_random() % 11
        density = next_random() % 1001
        edges = random_graph(n, density)
        check = (check * 31 + min_trio_degree(n, edges) + 1) % 1000000007
    print(f"3000 random graphs: checksum {check}")


main()
