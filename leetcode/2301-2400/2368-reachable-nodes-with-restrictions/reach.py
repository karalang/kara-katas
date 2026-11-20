# LeetCode #2368: Reachable Nodes With Restrictions -- the Python mirror of
# the ★ arm: adjacency lists, the restricted nodes marked, and a
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
    # LeetCode's two examples; one node; a path of 10^5 nodes, open and
    # cut at its middle; a star of 10^5 nodes with every odd leaf
    # restricted; then 2000 random trees of 2 to 40 nodes, each node
    # joined to an earlier one, with up to n - 1 restricted nodes
    print(reachable_nodes(7, [(0, 1), (1, 2), (3, 1), (4, 0), (0, 5), (5, 6)], [4, 5]))
    print(reachable_nodes(7, [(0, 1), (0, 2), (0, 5), (0, 4), (3, 2), (6, 5)], [4, 2, 1]))
    print(reachable_nodes(1, [], []))
    n = 100000
    path = [(i - 1, i) for i in range(1, n)]
    print(f"{reachable_nodes(n, path, [])} {reachable_nodes(n, path, [n // 2])}")
    star = [(i, 0) for i in range(1, n)]
    odd = [i for i in range(1, n) if i % 2 == 1]
    print(reachable_nodes(n, star, odd))
    check = 0
    alone = 0
    for _ in range(2000):
        n = 2 + next_random() % 39
        edges = [(next_random() % i, i) for i in range(1, n)]
        k = next_random() % n
        restricted = [1 + next_random() % (n - 1) for _ in range(k)]
        unique = sorted(set(restricted))
        t = reachable_nodes(n, edges, unique)
        check = (check * 31 + t) % 1000000007
        if t == 1:
            alone += 1
    print(f"2000 trees: checksum {check}, {alone} with node 0 alone")


main()
