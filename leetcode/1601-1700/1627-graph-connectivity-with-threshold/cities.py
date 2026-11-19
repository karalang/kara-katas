# LeetCode #1627: Graph Connectivity With Threshold -- the Python mirror
# of the ★ arm: a union-find with path compression joining every z above
# the threshold to its multiples, then a query is whether its two cities
# have the same root.


def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        nxt = parent[x]
        parent[x] = root
        x = nxt
    return root


def are_connected(n, threshold, queries):
    parent = list(range(n + 1))
    for z in range(threshold + 1, n + 1):
        for m in range(2 * z, n + 1, z):
            a, b = find(parent, z), find(parent, m)
            if a != b:
                parent[b] = a
    return [find(parent, a) == find(parent, b) for a, b in queries]


# ---- the harness: the same as every arm's ---------------------------------

seed = 1627


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def show(answers):
    return "[" + ", ".join("true" if a else "false" for a in answers) + "]"


def batch(count, most, asks):
    check = 0
    yes = 0
    for _ in range(count):
        n = next_random() % most + 1
        threshold = next_random() % (n // 2 + 1)
        q = next_random() % asks + 1
        queries = []
        for _ in range(q):
            a = next_random() % n + 1
            b = next_random() % n + 1
            queries.append((a, b))
        for answer in are_connected(n, threshold, queries):
            if answer:
                yes += 1
            check = mix(check, int(answer))
    print(f"{count} problems of up to {most} cities: {yes} queries connected, checksum {check}")


print(show(are_connected(6, 2, [[1, 4], [2, 5], [3, 6]])))
print(show(are_connected(6, 0, [[4, 5], [3, 4], [3, 2], [2, 6], [1, 3]])))
print(show(are_connected(5, 1, [[4, 5], [4, 5], [3, 2], [2, 3], [3, 4]])))
print(show(are_connected(1, 0, [[1, 1]])))
print(show(are_connected(8, 8, [[2, 4], [8, 8], [3, 6]])))
batch(2000, 20, 10)
batch(200, 1000, 100)
batch(5, 10000, 10000)
