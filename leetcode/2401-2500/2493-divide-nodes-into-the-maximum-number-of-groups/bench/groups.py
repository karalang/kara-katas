# LeetCode #2493: Divide Nodes Into the Maximum Number of Groups --
# benchmark mirror of the ★ arm (groups.kara): one graph of 500 nodes and
# about 4000 edges across a random cut, built once, then the passes; each
# asks on all but the last few edges, as many as the checksum so far
# chooses.


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


seed = 2493


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 500
    passes = 38
    side = [0] * (n + 1)
    for v in range(1, n + 1):
        side[v] = next_random() % 2
    taken = set()
    edges = []
    for _ in range(8000):
        a = next_random() % n + 1
        b = next_random() % n + 1
        if a != b and side[a] != side[b] and min(a, b) * 1000 + max(a, b) not in taken:
            taken.add(min(a, b) * 1000 + max(a, b))
            edges.append([a, b])
    m = len(edges)
    check = 0
    for p in range(passes):
        asked = edges[: m - check % 100]
        check = (check * 31 + magnificent_sets(n, asked) + p) % 1000000007
    print(f"{passes} passes over 500 nodes and {m} edges: checksum {check}")


main()
