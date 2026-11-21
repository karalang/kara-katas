# LeetCode #2497: Maximum Star Sum of a Graph -- Python mirror of the ★ arm
# (star_sum.kara): each node's neighbours' values sorted largest first and
# added while positive and fewer than k.


def max_star_sum(vals, edges, k):
    n = len(vals)
    beside = [[] for _ in range(n)]
    for a, b in edges:
        beside[a].append(vals[b])
        beside[b].append(vals[a])
    best = -(2**63)
    for centre in range(n):
        beside[centre].sort()
        beside[centre].reverse()
        total = vals[centre]
        taken = 0
        for value in beside[centre]:
            if taken == k or value <= 0:
                break
            total += value
            taken += 1
        best = max(best, total)
    return best


# ---- test harness -----------------------------------------------------------

seed = 2497


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def random_graph(n, tries, top):
    vals = [wide() % (2 * top + 1) - top for _ in range(n)]
    taken = set()
    edges = []
    for _ in range(tries):
        a = wide() % n
        b = wide() % n
        if a != b and min(a, b) * 1000000 + max(a, b) not in taken:
            taken.add(min(a, b) * 1000000 + max(a, b))
            edges.append([a, b])
    return vals, edges


def main():
    cases = [
        ([1, 2, 3, 4, 10, -10, -20], [[0, 1], [1, 2], [1, 3], [3, 4], [3, 5], [3, 6]], 2),
        ([-5], [], 0),
        ([-1, -2, -3], [[0, 1], [1, 2]], 2),
        ([5, 7, 9], [[0, 1], [1, 2], [0, 2]], 0),
        ([5, 7, 9], [[0, 1], [1, 2], [0, 2]], 2),
        ([-3, 4, 4, 4], [[0, 1], [0, 2], [0, 3]], 3),
        ([0, 0, 1], [[0, 1]], 1),
        ([2, -1, 3], [[0, 1], [1, 2]], 2),
    ]
    for vals, edges, k in cases:
        print(f"{len(vals)} nodes, {len(edges)} edges, k {k} -> {max_star_sum(vals, edges, k)}")
    for top in (20, 10000):
        check = 0
        for _ in range(2000):
            n = next_random() % 30 + 1
            tries = next_random() % 61
            k = next_random() % n
            vals, edges = random_graph(n, tries, top)
            check = (check * 31 + max_star_sum(vals, edges, k) + 1000000000) % 1000000007
        print(f"2000 random to {top}: checksum {check}")
    n = 100000
    hub = [[0, v] for v in range(1, n)]
    tens = [10000] * n
    print(f"10^5 star: {max_star_sum(tens, hub, n - 1)}")
    vals, edges = random_graph(n, 100000, 10000)
    print(f"10^5 random, {len(edges)} edges: k 50 -> {max_star_sum(vals, edges, 50)}, k 0 -> {max_star_sum(vals, edges, 0)}")
    signs = [-(v % 10000) if v % 2 == 0 else v % 10000 for v in range(n)]
    path = [[v, v + 1] for v in range(n - 1)]
    print(f"10^5 path: {max_star_sum(signs, path, 2)}")


if __name__ == "__main__":
    main()
