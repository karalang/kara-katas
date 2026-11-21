# LeetCode #2421: Number of Good Paths -- the Python mirror of the ★ arm:
# union-find over the nodes in order of value, each value's nodes joined
# to their neighbours no larger and then counted by root.

seed = 2421


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def number_of_good_paths(vals, edges):
    n = len(vals)
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent = list(range(n))
    order = sorted(range(n), key=lambda i: vals[i])
    good = n
    i = 0
    while i < n:
        j = i
        while j < n and vals[order[j]] == vals[order[i]]:
            j += 1
        for t in range(i, j):
            u = order[t]
            for v in adj[u]:
                if vals[v] <= vals[u]:
                    ru = find(parent, u)
                    rv = find(parent, v)
                    parent[ru] = rv
        count = {}
        for t in range(i, j):
            root = find(parent, order[t])
            count[root] = count.get(root, 0) + 1
        for c in count.values():
            good += c * (c - 1) // 2
        i = j
    return good


def random_tree(n, top):
    vals = [1 + (next_random() * 32768 + next_random()) % top for _ in range(n)]
    edges = []
    for i in range(1, n):
        p = next_random() % i
        if next_random() % 2 == 0:
            edges.append((p, i))
        else:
            edges.append((i, p))
    for i in range(len(edges) - 1, 0, -1):
        j = next_random() % (i + 1)
        edges[i], edges[j] = edges[j], edges[i]
    return vals, edges


def main():
    print(number_of_good_paths([1, 3, 2, 1, 3], [(0, 1), (0, 2), (2, 3), (2, 4)]))
    print(number_of_good_paths([1, 1, 2, 2, 3], [(0, 1), (1, 2), (2, 3), (2, 4)]))
    print(number_of_good_paths([1], []))
    print(number_of_good_paths([4, 4, 4, 4, 4], [(0, 1), (1, 2), (2, 3), (3, 4)]))
    print(number_of_good_paths([9, 2, 2, 2, 2], [(0, 1), (0, 2), (0, 3), (0, 4)]))
    print(number_of_good_paths([1, 2, 3, 2, 1], [(0, 1), (1, 2), (2, 3), (3, 4)]))
    print(number_of_good_paths(*random_tree(30000, 100000)))
    print(number_of_good_paths(*random_tree(30000, 3)))
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 12
        top = 1 + next_random() % 4
        a = number_of_good_paths(*random_tree(n, top))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
