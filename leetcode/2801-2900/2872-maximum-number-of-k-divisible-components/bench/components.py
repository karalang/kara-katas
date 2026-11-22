# LeetCode #2872: Maximum Number of K-Divisible Components -- the bench,
# as components.kara: 30 trees of 3 * 10^4 nodes, each answered 20 times
# by the breadth-first arm.

def max_k_divisible_components(n, edges, values, k):
    adjacent = [[] for _ in range(n)]
    for a, b in edges:
        adjacent[a].append(b)
        adjacent[b].append(a)
    parent = [-1] * n
    order = [0]
    head = 0
    while head < len(order):
        u = order[head]
        head += 1
        for w in adjacent[u]:
            if w != parent[u]:
                parent[w] = u
                order.append(w)
    rest = [v % k for v in values]
    parts = 0
    for u in reversed(order):
        if rest[u] == 0:
            parts += 1
        elif parent[u] >= 0:
            rest[parent[u]] = (rest[parent[u]] + rest[u]) % k
    return parts


seed = 2872


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 30, 20, 30000
    cases = []
    for c in range(count):
        k = next_random() % 9 + 2
        edges = []
        for v in range(1, n):
            reach = min(v, 5) if c % 2 == 1 else v
            edges.append([v - 1 - wide() % reach, v])
        values = [wide() % 1000000001 for _ in range(n)]
        values[0] += (k - sum(values) % k) % k
        cases.append((edges, values, k))
    total = 0
    check = 0
    for r in range(rounds):
        for edges, values, k in cases:
            parts = max_k_divisible_components(n, edges, values, k)
            total += parts
            check = (check * 31 + parts + r) % 1000000007
    print(f"{count} trees of {n}, {rounds} rounds: {total} components, checksum {check}")


main()
