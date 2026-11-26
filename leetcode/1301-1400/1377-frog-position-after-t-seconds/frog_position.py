# LeetCode #1377: Frog Position After T Seconds -- Python mirror of the ★
# arm: the chance of the frog being on each vertex, moved one second at a
# time, a vertex with unvisited neighbours handing its chance to them in
# equal shares.

import math

seed = 1377


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def tree(n, kind):
    order = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    edges = []
    for k in range(1, n):
        if kind == 0:
            back = next_random() % k
        elif kind == 1:
            back = k - 1 - next_random() % min(k, 3)
        elif kind == 2:
            back = next_random() % min(k, 3)
        else:
            back = k // 2 + next_random() % (k - k // 2)
        a, b = order[k], order[back]
        edges.append([a, b] if next_random() % 2 == 0 else [b, a])
    for i in range(len(edges) - 1, 0, -1):
        j = next_random() % (i + 1)
        edges[i], edges[j] = edges[j], edges[i]
    return edges


def main():
    example = [[1, 2], [1, 3], [1, 7], [2, 4], [2, 6], [3, 5]]
    path = [[i, i + 1] for i in range(1, 100)]
    star = [[1, i] for i in range(2, 101)]
    heap = [[i // 2, i] for i in range(2, 101)]
    shown = [
        frog_position(7, example, 2, 4),
        frog_position(7, example, 1, 7),
        frog_position(100, path, 50, 51),
        frog_position(100, path, 50, 100),
        frog_position(100, star, 1, 2),
        frog_position(100, star, 50, 2),
        frog_position(100, heap, 6, 64),
        frog_position(100, heap, 50, 100),
    ]
    print(" ".join(f"{p:.6f}" for p in shown))
    reached = 0
    check = 0
    for c in range(2000):
        n = 1 + next_random() % 100
        edges = tree(n, c % 4)
        t = 1 + next_random() % 12
        target = 1 + next_random() % n
        p = frog_position(n, edges, t, target)
        units = math.floor(p * 1048576.0 + 0.5)
        if units > 0:
            reached += 1
        check = (check * 131 + units) % 1000000007
    print(f"2000 random trees: {reached} targets reachable, checksum {check}")


main()
