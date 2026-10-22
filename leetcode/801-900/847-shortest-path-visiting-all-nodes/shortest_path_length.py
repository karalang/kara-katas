# LeetCode #847: Shortest Path Visiting All Nodes -- Python mirror of the ★ arm and its harness.
from collections import deque


def shortest_path_length(graph):
    n = len(graph)
    all_ = (1 << n) - 1
    seen = [False] * (n << n)
    queue = deque()
    for v in range(n):
        seen[(1 << v) * n + v] = True
        queue.append((1 << v, v, 0))
    while queue:
        mask, v, steps = queue.popleft()
        if mask == all_:
            return steps
        for w in graph[v]:
            nxt = mask | (1 << w)
            if not seen[nxt * n + w]:
                seen[nxt * n + w] = True
                queue.append((nxt, w, steps + 1))
    return 0


def show(graph):
    print(f"{graph} -> {shortest_path_length(graph)}")


seed = 847


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def lists(n, edge):
    return [[w for w in range(n) if edge[v * n + w]] for v in range(n)]


def connect(n, edge, v, w):
    edge[v * n + w] = True
    edge[w * n + v] = True


def random_graph(n, extra):
    edge = [False] * (n * n)
    for v in range(1, n):
        w = next_random() % v
        connect(n, edge, v, w)
    if n > 1:
        for _ in range(extra):
            v = next_random() % n
            w = next_random() % n
            if v != w:
                connect(n, edge, v, w)
    return lists(n, edge)


def main():
    for g in [[[1, 2, 3], [0], [0], [0]], [[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]], [[]],
              [[1], [0]], [[1, 2], [0, 2], [0, 1]], [[1], [0, 2], [1, 3], [2]],
              [[1, 3], [0, 2], [1, 3], [0, 2]], [[1, 2, 3, 4], [0], [0], [0, 5], [0], [3]],
              [[1], [0, 2, 3], [1], [1, 4, 5], [3], [3]]]:
        show(g)
    n = 12
    path = [False] * (n * n)
    cycle = [False] * (n * n)
    hub = [False] * (n * n)
    complete = [False] * (n * n)
    broom = [False] * (n * n)
    for v in range(n):
        if v + 1 < n:
            connect(n, path, v, v + 1)
        connect(n, cycle, v, (v + 1) % n)
        if v > 0:
            connect(n, hub, 0, v)
        for w in range(v + 1, n):
            connect(n, complete, v, w)
        if 0 < v < 6:
            connect(n, broom, v - 1, v)
        elif v >= 6:
            connect(n, broom, 5, v)
    print(f"a path of 12: {shortest_path_length(lists(n, path))}")
    print(f"a cycle of 12: {shortest_path_length(lists(n, cycle))}")
    print(f"a hub and 11 spokes: {shortest_path_length(lists(n, hub))}")
    print(f"12 nodes all joined: {shortest_path_length(lists(n, complete))}")
    print(f"a handle of 6 and 6 bristles: {shortest_path_length(lists(n, broom))}")
    for extra in [0, 4, 30]:
        graph = random_graph(12, extra)
        print(f"12 nodes, a tree and {extra} random edges: {shortest_path_length(graph)}")
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 9
        extra = next_random() % (2 * n)
        graph = random_graph(n, extra)
        length = shortest_path_length(graph)
        total += length
        check = (check * 31 + length) % 1000000007
    print(f"300 random graphs: lengths sum to {total}, checksum {check}")


main()
