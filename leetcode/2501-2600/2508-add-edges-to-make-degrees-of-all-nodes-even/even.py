# LeetCode #2508: Add Edges to Make Degrees of All Nodes Even -- mirror of
# the ★ arm (even.kara): the degrees counted, the edges held in a set as
# one number each, and the odd-degree nodes, of which there must be none,
# two or four.


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


seed = 2508


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(top):
    return (next_random() * 32768 + next_random()) % top


def random_graph(n, wanted):
    # up to `wanted` distinct edges, drawn until that many or 4 n draws
    seen = set()
    edges = []
    for _ in range(4 * wanted):
        if len(edges) == wanted:
            break
        a = next_random() % n + 1
        b = next_random() % n + 1
        if a != b and (min(a, b), max(a, b)) not in seen:
            seen.add((min(a, b), max(a, b)))
            edges.append((a, b))
    return edges


def main():
    cases = [
        (5, [(1, 2), (2, 3), (3, 4), (4, 2), (1, 4), (2, 5)]),
        (4, [(1, 2), (3, 4)]),
        (4, [(1, 2), (1, 3), (1, 4)]),
        (3, [(1, 2)]),
        (3, [(1, 2), (2, 3), (1, 3)]),
        (4, [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4)]),
        (6, [(1, 2), (3, 4), (5, 6)]),
        (5, [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)]),
    ]
    for n, edges in cases:
        print(f"{n} nodes, {len(edges)} edges -> {str(is_possible(n, edges)).lower()}")
    for most in [8, 30]:
        check = 0
        yes = 0
        for _ in range(2000):
            n = next_random() % (most - 2) + 3
            edges = random_graph(n, next_random() % (n * (n - 1) // 2) + 1)
            a = is_possible(n, edges)
            if a:
                yes += 1
            check = (check * 2 + (1 if a else 0)) % 1000000007
        print(f"2000 random to {most} nodes: {yes} possible, checksum {check}")
    star = [(1, v) for v in range(2, 100001)]
    print(f"10^5 nodes, a star -> {str(is_possible(100000, star)).lower()}")
    path = [(v, v + 1) for v in range(1, 100000)]
    print(f"10^5 nodes, a path -> {str(is_possible(100000, path)).lower()}")
    # 33000 nodes: 3 to n in a ring, 1 and 2 joined, and both joined to
    # every node of the ring, then the same with one ring node left alone
    ring = [(v, v + 1) for v in range(3, 33000)] + [(33000, 3), (1, 2)]
    joined = ring + [(h, v) for v in range(3, 33001) for h in (1, 2)]
    print(f"33000 nodes, two odd joined to all -> {str(is_possible(33000, joined)).lower()}")
    spared = ring + [(h, v) for v in range(3, 33001) if v != 17000 for h in (1, 2)]
    print(f"33000 nodes, two odd joined to all but one -> {str(is_possible(33000, spared)).lower()}")
    big = random_graph(100000, 100000)
    print(f"10^5 nodes, {len(big)} random edges -> {str(is_possible(100000, big)).lower()}")

main()
