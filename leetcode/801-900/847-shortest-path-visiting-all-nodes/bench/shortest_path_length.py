# Benchmark for #847: Shortest Path Visiting All Nodes -- Python twin of the
# Kāra ★ arm (breadth-first search over (visited set, node) states).
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


seed = 847


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 64
    rounds = 4000
    n = 12
    graphs = []
    for g in range(count):
        edge = [False] * (n * n)
        for v in range(1, n):
            w = next_random() % v
            edge[v * n + w] = True
            edge[w * n + v] = True
        for _ in range(g % 16 * 3):
            v = next_random() % n
            w = next_random() % n
            if v != w:
                edge[v * n + w] = True
                edge[w * n + v] = True
        graphs.append([[w for w in range(n) if edge[v * n + w]] for v in range(n)])
    total = 0
    checksum = 0
    for round_ in range(rounds):
        length = shortest_path_length(graphs[round_ % count])
        total += length
        checksum = (checksum * 31 + length) % 1000000007
    print(f"{rounds} rounds of {count} graphs: lengths sum to {total}, checksum {checksum}")


main()
