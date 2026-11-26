# LeetCode #1377 bench -- Python: the ★ arm: the chance of the frog being
# on each vertex, moved one second at a time, a vertex with unvisited
# neighbours handing its chance to them in equal shares.

import math


def frog_position(n, edges, t, target):
    adjacent = [[] for _ in range(n + 1)]
    for a, b in edges:
        adjacent[a].append(b)
        adjacent[b].append(a)
    seen = [False] * (n + 1)
    seen[1] = True
    chance = [0.0] * (n + 1)
    chance[1] = 1.0
    level = [1]
    for _ in range(t):
        nxt = []
        for u in level:
            ahead = [v for v in adjacent[u] if not seen[v]]
            if not ahead:
                continue
            share = chance[u] / len(ahead)
            for v in ahead:
                seen[v] = True
                chance[v] = share
                nxt.append(v)
            chance[u] = 0.0
        level = nxt
    return chance[target]


seed = 1377


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 50 trees of 100 vertices built once; then 100000 rounds, each asking
    # one tree, a time and a target drawn from the checksum so far for the
    # frog's chance, counted in units of 2^-20 (see the Kāra bench)
    n = 100
    trees = []
    for c in range(50):
        order = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            order[i], order[j] = order[j], order[i]
        edges = []
        for k in range(1, n):
            back = next_random() % k if c % 2 == 0 else k - 1 - next_random() % min(k, 3)
            edges.append([order[k], order[back]])
        trees.append(edges)
    check = 0
    for r in range(100000):
        c = check % 50
        t = 1 + (check // 50) % 50
        target = 1 + (check // 2500 + r) % n
        p = frog_position(n, trees[c], t, target)
        check = (check * 31 + math.floor(p * 1048576.0 + 0.5) + r) % 1000000007
    print(f"100000 rounds over 50 trees of 100 vertices: checksum {check}")


main()
