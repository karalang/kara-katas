# LeetCode #2508: Add Edges to Make Degrees of All Nodes Even --
# benchmark mirror of the ★ arm (even.kara): four graphs built once, two
# rings of 10^5 nodes and two of 33000 nodes whose two odd nodes are
# joined to every other, then the passes; each takes out one edge of
# every graph, chosen by the checksum so far, asks, and puts it back.


def is_possible(n, edges):
    degree = [0] * (n + 1)
    present = set()
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        present.add(min(a, b) * (n + 1) + max(a, b))

    def free(a, b):
        return min(a, b) * (n + 1) + max(a, b) not in present

    odd = [v for v in range(1, n + 1) if degree[v] % 2 == 1]
    if len(odd) == 0:
        return True
    if len(odd) == 2:
        a, b = odd
        if free(a, b):
            return True
        return any(c != a and c != b and free(a, c) and free(b, c) for c in range(1, n + 1))
    if len(odd) == 4:
        a, b, c, d = odd
        return (free(a, b) and free(c, d)) or (free(a, c) and free(b, d)) or (free(a, d) and free(b, c))
    return False


def graphs():
    ring = [(v, v % 100000 + 1) for v in range(1, 100001)]
    shifted = [(v, (v + 1) % 100000 + 1) for v in range(1, 100001)]
    base = [(v, v + 1) for v in range(3, 33000)] + [(33000, 3), (1, 2)]
    joined = base + [(h, v) for v in range(3, 33001) for h in (1, 2)]
    spared = base + [(h, v) for v in range(3, 33001) if v != 17000 for h in (1, 2)]
    return [(100000, ring), (100000, shifted), (33000, joined), (33000, spared)]


def main():
    passes = 90
    check = 0
    for p in range(passes):
        for n, edges in graphs_once:
            at = check % len(edges)
            taken = edges[at]
            edges[at] = edges[-1]
            edges.pop()
            # the edge at `at` is now the old last one, or none if `at` was last
            check = (check * 31 + (2 if is_possible(n, edges) else 1) + p) % 1000000007
            edges.append(taken)
            edges[at], edges[-1] = edges[-1], edges[at]
    print(f"{passes} passes over 4 graphs: checksum {check}")


graphs_once = graphs()
main()
