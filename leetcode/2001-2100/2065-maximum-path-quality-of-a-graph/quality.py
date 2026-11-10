# LeetCode #2065: Maximum Path Quality of a Graph -- Python mirror of the ★
# arm (quality.kara): a depth-first search over every walk from node 0
# that keeps within the time, a count of visits per node so that a node's
# value is added on its first visit only, and the best quality of a walk
# standing at node 0.
import sys

sys.setrecursionlimit(10000)


def maximal_path_quality(values, edges, max_time):
    n = len(values)
    adj = [[] for _ in range(n)]
    for u, v, t in edges:
        adj[u].append((v, t))
        adj[v].append((u, t))
    visits = [0] * n
    best = 0

    def walk(node, time, quality):
        nonlocal best
        if node == 0:
            best = max(best, quality)
        for nxt, t in adj[node]:
            if time + t <= max_time:
                visits[nxt] += 1
                gain = values[nxt] if visits[nxt] == 1 else 0
                walk(nxt, time + t, quality + gain)
                visits[nxt] -= 1

    visits[0] = 1
    walk(0, 0, values[0])
    return best


seed = 2065


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# `n` nodes, values up to `top`, about `m` edges of time 10 to 50, each
# from a node to one of the next three, no node with more than four edges
# and no edge twice
def graph_of(n, m, top):
    values = [(next_random() * 32768 + next_random()) % (top + 1) for _ in range(n)]
    degree = [0] * n
    seen = set()
    edges = []
    for _ in range(m):
        u = next_random() % n
        v = (u + 1 + next_random() % 3) % n
        t = next_random() % 41 + 10
        if u != v and degree[u] < 4 and degree[v] < 4 and (min(u, v), max(u, v)) not in seen:
            seen.add((min(u, v), max(u, v)))
            degree[u] += 1
            degree[v] += 1
            edges.append((u, v, t))
    return values, edges


def main():
    examples = [
        ([0, 32, 10, 43], [(0, 1, 10), (1, 2, 15), (0, 3, 10)], 49),
        ([5, 10, 15, 20], [(0, 1, 10), (1, 2, 10), (0, 3, 10)], 30),
        ([1, 2, 3, 4], [(0, 1, 10), (1, 2, 11), (2, 3, 12), (1, 3, 13)], 50),
        ([0, 1, 2], [(1, 2, 10)], 10),
        ([7], [], 10),
        ([1, 100], [(0, 1, 50)], 99),
        ([1, 100], [(0, 1, 50)], 100),
    ]
    for values, edges, max_time in examples:
        print(f"{len(values)} nodes, {len(edges)} edges, {max_time} -> {maximal_path_quality(values, edges, max_time)}")
    # 400 graphs of 1 to 30 nodes, 0 to 60 edges tried, values up to 10 or
    # 100000000, time 10 to 100
    total = 0
    check = 0
    for _ in range(400):
        n = next_random() % 30 + 1
        m = next_random() % 61
        top = [10, 100000000][next_random() % 2]
        values, edges = graph_of(n, m, top)
        max_time = next_random() % 91 + 10
        a = maximal_path_quality(values, edges, max_time)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"400 graphs: sum {total}, checksum {check}")
    # the constraints' largest: 1000 nodes, 2000 edges tried, time 100
    values, edges = graph_of(1000, 2000, 100000000)
    print(f"1000 nodes, {len(edges)} edges, 100 -> {maximal_path_quality(values, edges, 100)}")


main()
