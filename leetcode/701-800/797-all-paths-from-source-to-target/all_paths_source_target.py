# LeetCode 797 -- All Paths From Source to Target: mirrors the harness of
# all_paths_source_target.kara with the ★ arm's depth first search.
seed = 797


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def all_paths_source_target(graph):
    paths = []
    path = [0]

    def walk(node):
        if node == len(graph) - 1:
            paths.append(list(path))
            return
        for nxt in graph[node]:
            path.append(nxt)
            walk(nxt)
            path.pop()

    walk(0)
    return paths


def text(paths):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in p) + "]" for p in paths) + "]"


def checksum(paths):
    check = 0
    for path in paths:
        for v in path:
            check = (check * 131 + v + 1) % 1000000007
        check = (check * 131) % 1000000007
    return check


def show(graph):
    paths = sorted(all_paths_source_target(graph))
    print(f"{text(graph)} -> {text(paths)}")


def complete(n):
    return [list(range(i + 1, n)) for i in range(n)]


def main():
    show([[1, 2], [3], [3], []])
    show([[4, 3, 1], [3, 2, 4], [3], [4], []])
    show([[1], []])
    show([[], []])
    show([[2], [], [1]])
    allp = sorted(all_paths_source_target(complete(15)))
    print(f"every edge on 15 nodes: {len(allp)} paths, checksum {checksum(allp)}")
    count = 0
    check = 0
    for _ in range(300):
        n = 2 + next_random() % 11
        order = list(range(n))
        for i in range(1, n):
            j = next_random() % (i + 1)
            order[i], order[j] = order[j], order[i]
        at_first = order.index(0)
        at_last = order.index(n - 1)
        if at_last < at_first:
            order[at_first] = n - 1
            order[at_last] = 0
        chance = 1 + next_random() % 4
        graph = [[] for _ in range(n)]
        for a in range(n):
            for b in range(a + 1, n):
                if next_random() % 5 < chance:
                    graph[order[a]].append(order[b])
        paths = sorted(all_paths_source_target(graph))
        count += len(paths)
        check = (check * 1000003 + checksum(paths)) % 1000000007
    print(f"300 random graphs: {count} paths, checksum {check}")


main()
