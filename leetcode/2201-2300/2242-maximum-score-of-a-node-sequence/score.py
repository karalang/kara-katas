# LeetCode #2242: Maximum Score of a Node Sequence -- the Python mirror of
# score.kara: each node's neighbours sorted by score, largest first, and
# cut to three; every edge, both ways round, tries the nine pairs of a
# neighbour of one end and a neighbour of the other, all four distinct.


def maximum_score(scores, edges):
    n = len(scores)
    best3 = [[] for _ in range(n)]
    for a, b in edges:
        best3[a].append(b)
        best3[b].append(a)
    for node in range(n):
        best3[node].sort(key=lambda x: -scores[x])
        del best3[node][3:]
    best = -1
    for b, c in edges:
        for a in best3[b]:
            if a == c:
                continue
            for d in best3[c]:
                if d != a and d != b:
                    best = max(best, scores[a] + scores[b] + scores[c] + scores[d])
    return best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def graph(n, m, top):
    scores = [wide_random() % top + 1 for _ in range(n)]
    seen = set()
    edges = []
    most = n * (n - 1) // 2
    while len(edges) < min(m, most):
        a = wide_random() % n
        b = wide_random() % n
        if a != b and (min(a, b), max(a, b)) not in seen:
            seen.add((min(a, b), max(a, b)))
            edges.append((a, b))
    return scores, edges


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    global seed
    examples = [
        ([5, 2, 9, 8, 4], [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (2, 4)]),
        ([9, 20, 6, 4, 11, 12], [(0, 3), (5, 3), (2, 4), (1, 3)]),
        ([1, 2, 3, 4], [(0, 1), (1, 2), (2, 3)]),
        ([7, 1, 1, 1, 1], [(0, 1), (0, 2), (0, 3), (0, 4)]),
        ([1, 5, 5, 5, 9], [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)]),
        ([100000000] * 4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
    ]
    for scores, edges in examples:
        print(f"{show(scores)} {show(edges)} -> {maximum_score(scores, edges)}")
    seed = 2242
    found = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 9 + 4
        m = next_random() % 20 + 1
        top = next_random() % 100 + 1
        scores, edges = graph(n, m, top)
        best = maximum_score(scores, edges)
        if best >= 0:
            found += 1
        check = (check * 31 + best + 1) % 1000000007
    print(f"2000 small graphs: {found} with a sequence, checksum {check}")
    scores, edges = graph(50000, 50000, 100000000)
    print(f"50000 nodes, 50000 edges: {maximum_score(scores, edges)}")
    hub_scores = [(i * 7919) % 100000000 + 1 for i in range(50000)]
    hub_edges = [(0, i) for i in range(1, 50000)]
    hub_edges.append((1, 2))
    print(f"a hub of 49999 spokes: {maximum_score(hub_scores, hub_edges)}")


main()
