# LeetCode #2065: Maximum Path Quality of a Graph -- Python mirror of the ★
# arm's benchmark (quality.kara): 1000 graphs of 1000 nodes, 2000 edges
# tried, each from a node to one of the next three and of time 10 or 11,
# and the time 100, so that walks run to 10 edges through nodes of up to
# four.
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


def main():
    total = 0
    check = 0
    for _ in range(1000):
        n = 1000
        values = [(next_random() * 32768 + next_random()) % 100000001 for _ in range(n)]
        degree = [0] * n
        seen = set()
        edges = []
        for _ in range(2000):
            u = next_random() % n
            v = (u + 1 + next_random() % 3) % n
            t = next_random() % 2 + 10
            key = (min(u, v), max(u, v))
            if degree[u] < 4 and degree[v] < 4 and key not in seen:
                seen.add(key)
                degree[u] += 1
                degree[v] += 1
                edges.append((u, v, t))
        a = maximal_path_quality(values, edges, 100)
        total += a
        check = (check * 31 + a % 1000000007) % 1000000007
    print(f"1000 graphs: sum {total}, checksum {check}")


main()
