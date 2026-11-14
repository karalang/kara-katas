# LeetCode #1557: Minimum Number of Vertices to Reach All Nodes -- the
# Python mirror of vertices.kara, the ★ arm: the nodes no edge ends at.
# Prints byte-identical output.


def find_smallest_set_of_vertices(n, edges):
    reached = [False] * n
    for _, to in edges:
        reached[to] = True
    return [v for v in range(n) if not reached[v]]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def answer(n, edges):
    return sorted(find_smallest_set_of_vertices(n, edges))


def batch(count, most, wide):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % (most - 1) + 2
        order = list(range(n))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            order[i], order[j] = order[j], order[i]
        draws = next_random() % (wide * n) + 1
        taken = set()
        edges = []
        for _ in range(draws):
            a = next_random() % n
            b = next_random() % n
            if a < b and (a, b) not in taken:
                taken.add((a, b))
                edges.append((order[a], order[b]))
        if not edges:
            edges.append((order[0], order[1]))
        found = answer(n, edges)
        total += len(found)
        for v in found:
            check = mix(check, v)
        check = mix(check, -1)
    print(f"{count} graphs of up to {most} nodes: {total} sources, checksum {check}")


def show_edges(edges):
    return "[" + ", ".join(f"({a}, {b})" for a, b in edges) + "]"


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    global seed
    examples = [
        (6, [(0, 1), (0, 2), (2, 5), (3, 4), (4, 2)]),
        (5, [(0, 1), (2, 1), (3, 1), (1, 4), (2, 4)]),
        (2, [(1, 0)]),
        (3, [(0, 1), (1, 2)]),
        (4, [(0, 3), (1, 3), (2, 3)]),
        (4, [(3, 0), (3, 1), (3, 2)]),
        (5, [(0, 1), (2, 3)]),
    ]
    for n, edges in examples:
        print(f"n = {n}, edges {show_edges(edges)} -> {show(answer(n, edges))}")
    seed = 1557
    batch(3000, 8, 2)
    batch(300, 1000, 3)
    batch(30, 100000, 1)


main()
