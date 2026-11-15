# LeetCode #1168: Optimize Water Distribution in a Village -- the ★ arm's
# bench in Python: Kruskal over the pipes and a pipe from a source to every
# house, union-find by size with path halving.


def min_cost_to_supply_water(n, wells, pipes):
    edges = [(w, 0, i + 1) for i, w in enumerate(wells)]
    edges += [(p[2], p[0], p[1]) for p in pipes]
    edges.sort()
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    cost = 0
    joined = 0
    for c, a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        cost += c
        joined += 1
        if joined == n:
            break
    return cost


seed = 1168


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 10000
    wells = []
    pipes = []
    for _ in range(16):
        wells.append([next_random() % 100001 for _ in range(n)])
        ps = []
        for _ in range(10000):
            a = 1 + next_random() % n
            b = 1 + next_random() % (n - 1)
            if b >= a:
                b += 1
            ps.append([a, b, next_random() % 100001])
        pipes.append(ps)
    total = 0
    check = 0
    for _ in range(40):
        for v in range(16):
            j = next_random() % 10000
            pipes[v][j][2] = next_random() % 100001
            c = min_cost_to_supply_water(n, wells[v], pipes[v])
            total += c
            check = (check * 31 + c) % 1000000007
    print(f"40 rounds over 16 villages of 10^4 houses: total {total}, checksum {check}")


main()
