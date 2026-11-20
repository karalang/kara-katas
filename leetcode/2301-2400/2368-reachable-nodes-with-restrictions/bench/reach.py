# LeetCode #2368: Reachable Nodes With Restrictions -- the bench, the ★
# arm in Python: adjacency lists, the restricted nodes marked, and a
# breadth-first search from node 0 that never enters a marked node.


def reachable_nodes(n, edges, restricted):
    nxt = [[] for _ in range(n)]
    for a, b in edges:
        nxt[a].append(b)
        nxt[b].append(a)
    seen = [False] * n
    for r in restricted:
        seen[r] = True
    seen[0] = True
    queue = [0]
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        for v in nxt[u]:
            if not seen[v]:
                seen[v] = True
                queue.append(v)
    return len(queue)


SEED = [2368]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # tree a: 10^5 nodes, node i joined to one of the 4^a nodes before it,
    # and each node but 0 restricted with a chance of 1 in 2^(a + 4)
    n = 100000
    trees = []
    width = 1
    for a in range(10):
        edges = [(i - 1 - next_random() % min(width, i), i) for i in range(1, n)]
        restricted = [i for i in range(1, n) if next_random() % (16 << a) == 0]
        trees.append((edges, restricted))
        width *= 4
    check = 0
    for p in range(20):
        for edges, restricted in trees:
            check = (check * 31 + reachable_nodes(n, edges, restricted) + p) % 1000000007
    print(f"20 passes over 10 trees of 10^5 nodes: checksum {check}")


main()
