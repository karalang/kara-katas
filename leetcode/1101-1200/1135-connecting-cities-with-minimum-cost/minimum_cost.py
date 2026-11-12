# LeetCode #1135: Connecting Cities With Minimum Cost -- the Python mirror
# of the ★ arm: Kruskal's algorithm, the connections taken cheapest first
# and kept when they join two parts, the parts kept in a union-find with
# path halving and union by size.


def minimum_cost(n, connections):
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    joined = 1
    for x, y, cost in sorted(connections, key=lambda c: c[2]):
        a = find(x)
        b = find(y)
        if a != b:
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]
            total += cost
            joined += 1
    return total if joined == n else -1


seed = 1135


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(cs):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in c) + "]" for c in cs) + "]"


def main():
    cases = [
        (3, [[1, 2, 5], [1, 3, 6], [2, 3, 1]]),
        (4, [[1, 2, 3], [3, 4, 4]]),
        (2, [[1, 2, 7], [2, 1, 3], [1, 2, 9]]),
        (4, [[1, 2, 1], [2, 3, 1], [3, 4, 1], [4, 1, 1]]),
        (5, [[1, 2, 10], [1, 3, 10], [1, 4, 10], [1, 5, 10], [2, 3, 1], [3, 4, 1]]),
        (5, [[1, 2, 4], [2, 3, 4], [4, 5, 4]]),
        (6, [[1, 2, 6], [2, 3, 5], [3, 4, 4], [4, 5, 3], [5, 6, 2], [6, 1, 1]]),
        (3, [[2, 3, 100000], [1, 2, 100000]]),
    ]
    for n, cs in cases:
        print(f"{n}, {show(cs)} -> {minimum_cost(n, cs)}")
    total = 0
    none = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 11 + 2
        m = next_random() % 20 + 1
        cs = []
        for _ in range(m):
            x = next_random() % n + 1
            y = next_random() % (n - 1) + 1
            if y >= x:
                y += 1
            cs.append([x, y, next_random() % 20 + 1])
        r = minimum_cost(n, cs)
        if r == -1:
            none += 1
        else:
            total += r
        check = (check * 31 + r + 1) % 1000000007
    print(f"2000 random networks: costs total {total}, {none} not connected, checksum {check}")
    tree = []
    for i in range(2, 10001):
        tree.append([next_random() % (i - 1) + 1, i, (next_random() * 32768 + next_random()) % 100000 + 1])
    tree.append([1, 10000, 1])
    print(f"10000 cities on a random tree and one more road: {minimum_cost(10000, tree)}")
    dense = []
    for _ in range(10000):
        x = next_random() % 1000 + 1
        y = next_random() % 999 + 1
        if y >= x:
            y += 1
        dense.append([x, y, (next_random() * 32768 + next_random()) % 100000 + 1])
    print(f"1000 cities and 10000 random roads: {minimum_cost(1000, dense)}")


main()
