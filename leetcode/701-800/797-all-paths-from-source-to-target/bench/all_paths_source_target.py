# LeetCode 797 -- All Paths From Source to Target: the bench, in Python.
# Mirrors all_paths_source_target.kara: a depth first search keeping the
# path so far, copying it at node n - 1.
import sys

sys.setrecursionlimit(10000)


def all_paths_source_target(graph):
    paths = []
    path = [0]
    target = len(graph) - 1

    def walk(node):
        if node == target:
            paths.append(list(path))
            return
        for nxt in graph[node]:
            path.append(nxt)
            walk(nxt)
            path.pop()

    walk(0)
    return paths


seed = 797


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 15
    graphs = []
    for _ in range(1024):
        order = [0] + list(range(1, n - 1))
        for i in range(2, n - 1):
            j = 1 + next_random() % i
            order[i], order[j] = order[j], order[i]
        order.append(n - 1)
        chance = 1 + next_random() % 4
        graph = [[] for _ in range(n)]
        for a in range(n):
            for b in range(a + 1, n):
                if next_random() % 5 < chance:
                    graph[order[a]].append(order[b])
        graphs.append(graph)
    rounds = 40960
    count = nodes = check = 0
    for r in range(rounds):
        paths = all_paths_source_target(graphs[r % 1024])
        count += len(paths)
        for path in paths:
            nodes += len(path)
            h = 0
            for v in path:
                h = (h * 31 + v + 1) % 1000000007
            check = (check + h) % 1000000007
    print(f"{rounds} graphs: {count} paths through {nodes} nodes, checksum {check}")


main()
