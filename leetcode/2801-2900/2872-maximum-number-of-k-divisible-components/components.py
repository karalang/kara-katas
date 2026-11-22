# LeetCode #2872: Maximum Number of K-Divisible Components -- the Python
# mirror of the ★ arm (components.kara): subtree sums mod k, children
# before parents in reverse breadth-first order, zeros counted.


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


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    global seed
    print(
        f"{max_k_divisible_components(5, [[0, 2], [1, 2], [1, 3], [2, 4]], [1, 8, 1, 4, 4], 6)} {max_k_divisible_components(7, [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]], [3, 0, 6, 1, 5, 2, 1], 3)}"
    )
    n = 30000
    path = [[i - 1, i] for i in range(1, n)]
    star = [[0, i] for i in range(1, n)]
    print(f"{max_k_divisible_components(n, path, [7] * n, 7)} {max_k_divisible_components(n, star, [0] * n, 1000000000)}")
    seed = 2872
    total = 0
    check = 0
    for c in range(3030):
        small = c < 3000
        n = next_random() % 10 + 1 if small else wide() % 29001 + 1000
        if small:
            k = next_random() % 5 + 1
        elif c % 2 == 1:
            k = next_random() % 9 + 2
        else:
            k = wide() % 1000000000 + 1
        edges = []
        for v in range(1, n):
            reach = min(v, 5) if not small and c % 2 == 1 else v
            edges.append([v - 1 - wide() % reach, v])
        values = [next_random() % 10 if small else wide() % 1000000001 for _ in range(n)]
        values[0] += (k - sum(values) % k) % k
        parts = max_k_divisible_components(n, edges, values, k)
        total += parts
        check = (check * 31 + parts) % 1000000007
        if c == 2999:
            print(f"3000 small trees: {total} components, checksum {check}")
            total = 0
            check = 0
    print(f"30 large trees: {total} components, checksum {check}")


main()
