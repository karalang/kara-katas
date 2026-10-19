# LeetCode 785 — Is Graph Bipartite?, two colours by breadth first search.
# Mirrors is_bipartite.kara (the ★ arm) and its harness.
from collections import deque


def is_bipartite(graph):
    n = len(graph)
    colour = [-1] * n
    for start in range(n):
        if colour[start] != -1:
            continue
        colour[start] = 0
        queue = deque([start])
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


def from_edges(n, edges):
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    return graph


def cycle(n):
    return from_edges(n, [(i, (i + 1) % n) for i in range(n)])


def random_graph(n, density, kind):
    side = [next_random() % 2 for _ in range(n)]
    edges = []
    for a in range(n):
        for b in range(a + 1, n):
            if (kind == 2 or side[a] != side[b]) and next_random() % 1000 < density:
                edges.append((a, b))
    if kind == 1:
        a = next_random() % n
        b = next_random() % n
        tries = 0
        while (b == a or side[b] != side[a]) and tries < n:
            b = (b + 1) % n
            tries += 1
        if b != a and side[b] == side[a]:
            edges.append((a, b))
    return from_edges(n, edges)


def text(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return "[" + ", ".join(text(x) for x in v) + "]"
    return str(v)


def show(graph):
    print(f"{text(graph)} -> {text(is_bipartite(graph))}")


def main():
    show([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]])
    show([[1, 3], [0, 2], [1, 3], [0, 2]])
    show([[]])
    show([[1], [0]])
    show([[1, 2], [0, 2], [0, 1], []])
    show(from_edges(7, [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 4)]))
    show(from_edges(7, [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6)]))
    print(f"a cycle of 100 -> {text(is_bipartite(cycle(100)))}")
    print(f"a cycle of 99 -> {text(is_bipartite(cycle(99)))}")
    edges = [(a, b) for a in range(50) for b in range(50, 100)]
    print("two sides of 50, every pair across joined -> "
          f"{text(is_bipartite(from_edges(100, edges)))}")
    edges.append((0, 49))
    print(f"that and one edge inside a side -> {text(is_bipartite(from_edges(100, edges)))}")
    tree = [(next_random() % i, i) for i in range(1, 100)]
    print(f"a random tree of 100 -> {text(is_bipartite(from_edges(100, tree)))}")
    yes = 0
    check = 0
    for g in range(300):
        n = 1 + next_random() % 100
        density = 1 + next_random() % 60
        answer = is_bipartite(random_graph(n, density, g % 3))
        if answer:
            yes += 1
        check = (check * 31 + n * (2 if answer else 1)) % 1000000007
    print(f"300 random graphs: {yes} bipartite, checksum {check}")


main()
