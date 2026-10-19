# LeetCode 802 -- Find Eventual Safe States: the bench, mirroring
# eventual_safe_nodes.kara with the same three-colour search.
import sys

sys.setrecursionlimit(100000)
seed = 802


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def eventual_safe_nodes(graph):
    n = len(graph)
    # 0 not seen yet, 1 grey (on the search or unsafe), 2 black (safe).
    colour = [0] * n

    def is_safe(node):
        if colour[node] != 0:
            return colour[node] == 2
        colour[node] = 1
        for nxt in graph[node]:
            if not is_safe(nxt):
                return False
        colour[node] = 2
        return True

    return [node for node in range(n) if is_safe(node)]


def main():
    n = 10000
    graphs = []
    for _ in range(16):
        graph = []
        for a in range(n):
            picked = []
            edges = next_random() % 5
            for _ in range(edges):
                if next_random() % 1000 == 0:
                    b = max(a - 1 - next_random() % 50, 0)
                else:
                    b = a + 1 + next_random() % 50
                if b < n:
                    picked.append(b)
            # In increasing order with no edge twice, as LeetCode gives.
            picked.sort()
            out = []
            for b in picked:
                if not out or out[-1] != b:
                    out.append(b)
            graph.append(out)
        graphs.append(graph)
    rounds = 4000
    total = 0
    check = 0
    for r in range(rounds):
        safe = eventual_safe_nodes(graphs[r % 16])
        total += len(safe)
        check = (check * 131 + len(safe) + safe[len(safe) // 2]) % 1000000007
    print(f"{rounds} rounds of {n} nodes: {total} safe nodes in all, checksum {check}")


main()
