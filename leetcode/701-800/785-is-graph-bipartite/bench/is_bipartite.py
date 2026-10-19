# LeetCode 785 — Is Graph Bipartite?: the bench, in Python.
# Mirrors is_bipartite.kara: two colours by breadth first search over the
# same 64 graphs.
from collections import deque


def is_bipartite(graph):
    n = len(graph)
    colour = [-1] * n
    queue = deque()
    for start in range(n):
        if colour[start] != -1:
            continue
        colour[start] = 0
        queue.append(start)
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if colour[v] == -1:
                    colour[v] = 1 - colour[u]
                    queue.append(v)
                elif colour[v] == colour[u]:
                    return False
    return True


seed = 785


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    graphs = []
    for g in range(64):
        side = [next_random() % 2 for _ in range(100)]
        graph = [[] for _ in range(100)]
        for a in range(100):
            for b in range(a + 1, 100):
                if side[a] != side[b] and next_random() % 10 == 0:
                    graph[a].append(b)
                    graph[b].append(a)
        if g % 2 == 1:
            a = next_random() % 100
            b = (a + 1) % 100
            while side[b] != side[a]:
                b = (b + 1) % 100
            graph[a].append(b)
            graph[b].append(a)
        graphs.append(graph)
    rounds = 500000
    yes = 0
    check = 0
    for r in range(rounds):
        answer = is_bipartite(graphs[r % 64])
        if answer:
            yes += 1
        check = (check * 31 + (2 if answer else 1) + r % 7) % 1000000007
    print(f"{rounds} rounds of 100-node graphs: {yes} bipartite, checksum {check}")


main()
