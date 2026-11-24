# LeetCode #1319: Number of Operations to Make Network Connected -- Python
# mirror of the ★ Kāra arm: fewer than n - 1 cables can never join n
# computers; otherwise the answer is the number of groups less one, the
# groups by union-find with parent pointers halved on the way up and the
# smaller group hung under the larger.


def find(parent, x):
    at = x
    while parent[at] != at:
        parent[at] = parent[parent[at]]
        at = parent[at]
    return at


def make_connected(n, connections):
    if len(connections) < n - 1:
        return -1
    parent = list(range(n))
    size = [1] * n
    groups = n
    for c in connections:
        a = find(parent, c[0])
        b = find(parent, c[1])
        if a != b:
            big, small = (a, b) if size[a] >= size[b] else (b, a)
            parent[small] = big
            size[big] += size[small]
            groups -= 1
    return groups - 1


seed = 1319


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_cables(n, m):
    seen = set()
    cables = []
    while len(cables) < m:
        hi = next_random()
        u = (hi * 32768 + next_random()) % n
        hi = next_random()
        v = (hi * 32768 + next_random()) % n
        if u != v and (min(u, v), max(u, v)) not in seen:
            seen.add((min(u, v), max(u, v)))
            cables.append([u, v])
    return cables


def main():
    e1 = make_connected(4, [[0, 1], [0, 2], [1, 2]])
    e2 = make_connected(6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]])
    e3 = make_connected(6, [[0, 1], [0, 2], [0, 3], [1, 2]])
    e4 = make_connected(2, [[1, 0]])
    e5 = make_connected(100000, [[i - 1, i] for i in range(1, 100000)])
    e6 = make_connected(100000, random_cables(100000, 100000))
    print(f"{e1} {e2} {e3} {e4} {e5} {e6}")
    total = 0
    check = 0
    for _ in range(300):
        n = 2 + next_random() % 1999
        m = 1 + next_random() % min(3000, n * (n - 1) // 2)
        got = make_connected(n, random_cables(n, m))
        total += got
        check = (check * 31 + got + 1) % 1000000007
    print(f"300 random networks: moves total {total}, checksum {check}")


main()
