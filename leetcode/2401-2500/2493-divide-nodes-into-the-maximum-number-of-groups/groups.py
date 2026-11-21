# LeetCode #2493: Divide Nodes Into the Maximum Number of Groups -- Python
# mirror of the ★ arm (groups.kara): a breadth-first search from every
# node, an edge between two nodes at one distance answering -1, each
# part's most levels kept at its least node.


def magnificent_sets(n, edges):
    nxt = [[] for _ in range(n + 1)]
    for a, b in edges:
        nxt[a].append(b)
        nxt[b].append(a)
    most = [0] * (n + 1)
    for start in range(1, n + 1):
        depth = [-1] * (n + 1)
        depth[start] = 0
        queue = [start]
        head = 0
        least = start
        deepest = 0
        while head < len(queue):
            node = queue[head]
            head += 1
            least = min(least, node)
            deepest = max(deepest, depth[node])
            for other in nxt[node]:
                if depth[other] == -1:
                    depth[other] = depth[node] + 1
                    queue.append(other)
                elif depth[other] == depth[node]:
                    return -1
        most[least] = max(most[least], deepest + 1)
    return sum(most)


# ---- test harness -----------------------------------------------------------

seed = 2493


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_edges(n, tries, cut):
    side = [0] * (n + 1)
    for v in range(1, n + 1):
        side[v] = next_random() % 2
    taken = set()
    edges = []
    for _ in range(tries):
        a = next_random() % n + 1
        b = next_random() % n + 1
        if a != b and (not cut or side[a] != side[b]):
            key = min(a, b) * 1000 + max(a, b)
            if key not in taken:
                taken.add(key)
                edges.append([a, b])
    if not edges:
        edges.append([1, 2])
    return edges


def main():
    cases = [
        (6, [[1, 2], [1, 4], [1, 5], [2, 6], [2, 3], [4, 6]]),
        (3, [[1, 2], [2, 3], [3, 1]]),
        (2, [[1, 2]]),
        (4, [[1, 2]]),
        (4, [[1, 2], [2, 3], [3, 4], [4, 1]]),
        (5, [[1, 2], [2, 3], [3, 4], [4, 5]]),
        (7, [[1, 2], [2, 3], [3, 1], [4, 5]]),
        (8, [[1, 2], [2, 3], [3, 4], [5, 6], [6, 7], [7, 8], [8, 5]]),
        (6, [[1, 2], [1, 3], [1, 4], [1, 5], [1, 6]]),
    ]
    for n, edges in cases:
        print(f"{n} nodes, {len(edges)} edges -> {magnificent_sets(n, edges)}")
    for cut in (True, False):
        divide = 0
        check = 0
        for _ in range(2000):
            n = next_random() % 39 + 2
            tries = next_random() % 61
            answer = magnificent_sets(n, random_edges(n, tries, cut))
            if answer > 0:
                divide += 1
            check = (check * 31 + answer + 1) % 1000000007
        how = "across a cut" if cut else "drawn freely"
        print(f"2000 random {how}: {divide} divide, checksum {check}")
    n = 500
    path = [[v, v + 1] for v in range(1, n)]
    grid = []
    for r in range(20):
        for c in range(25):
            v = r * 25 + c + 1
            if c < 24:
                grid.append([v, v + 1])
            if r < 19:
                grid.append([v, v + 25])
    both = [[a, b] for a in range(1, 101) for b in range(101, 201)]
    random = random_edges(n, 10000, True)
    for name, edges in [("path", path), ("grid", grid), ("two sides", both), ("random", random)]:
        print(f"500 {name}: {len(edges)} edges -> {magnificent_sets(n, edges)}")


if __name__ == "__main__":
    main()
