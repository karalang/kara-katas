def most_profitable_path(edges, bob, amount):
    n = len(amount)
    adjacent = [[] for _ in range(n)]
    for a, b in edges:
        adjacent[a].append(b)
        adjacent[b].append(a)
    parent = [-1] * n
    depth = [0] * n
    order = [0]
    parent[0] = 0
    nxt = 0
    while nxt < len(order):
        node = order[nxt]
        nxt += 1
        for child in adjacent[node]:
            if parent[child] < 0:
                parent[child] = node
                depth[child] = depth[node] + 1
                order.append(child)
    bob_time = [n] * n
    node = bob
    t = 0
    while node != 0:
        bob_time[node] = t
        node = parent[node]
        t += 1
    bob_time[0] = t
    income = [0] * n
    best = None
    for node in order:
        if depth[node] < bob_time[node]:
            gate = amount[node]
        elif depth[node] == bob_time[node]:
            gate = int(amount[node] / 2)
        else:
            gate = 0
        income[node] = gate if node == 0 else income[parent[node]] + gate
        if node != 0 and len(adjacent[node]) == 1:
            best = income[node] if best is None else max(best, income[node])
    return best


# ---- test harness ---------------------------------------------------------

seed = 2467


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def random_tree(n, reach):
    edges = []
    for node in range(1, n):
        back = 1 + wide_random() % min(reach, node)
        other = node - back
        if next_random() % 2 == 0:
            edges.append([node, other])
        else:
            edges.append([other, node])
    for i in range(len(edges) - 1, 0, -1):
        j = wide_random() % (i + 1)
        edges[i], edges[j] = edges[j], edges[i]
    return edges


def random_amounts(n):
    return [2 * (next_random() % 10001) - 10000 for _ in range(n)]


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    cases = [
        ([[0, 1], [1, 2], [1, 3], [3, 4]], 3, [-2, 4, 2, -4, 6]),
        ([[0, 1]], 1, [-7280, 2350]),
        ([[0, 1], [1, 2], [2, 3], [3, 4]], 4, [0, 2, 10, 4, 8]),
        ([[1, 0], [0, 2], [2, 3]], 1, [6, -4, 2, 8]),
        ([[0, 1], [1, 2], [0, 3]], 2, [2, 6, -2, -10]),
        ([[0, 1], [0, 2], [2, 3]], 3, [-2, -4, -6, -8]),
    ]
    for edges, bob, amount in cases:
        print(f"bob {bob}, {show(amount)} -> {most_profitable_path(edges, bob, amount)}")
    n = 100000
    path = [[v - 1, v] for v in range(1, n)]
    print(f"path of 10^5: {most_profitable_path(path, n - 1, random_amounts(n))}")
    star = [[0, v] for v in range(1, n)]
    print(f"star of 10^5: {most_profitable_path(star, n // 2, random_amounts(n))}")
    tree = random_tree(n, n)
    print(f"random tree of 10^5: {most_profitable_path(tree, n - 1, random_amounts(n))}")
    deep = random_tree(10000, 3)
    print(f"deep random tree of 10^4: {most_profitable_path(deep, 3333, random_amounts(10000))}")
    check = 0
    for _ in range(3000):
        n = 2 + next_random() % 39
        edges = random_tree(n, 1 + next_random() % n)
        bob = 1 + next_random() % (n - 1)
        amount = random_amounts(n)
        check = (check * 31 + most_profitable_path(edges, bob, amount) + 1000000007) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
