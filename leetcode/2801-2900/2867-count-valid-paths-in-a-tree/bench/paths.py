# LeetCode #2867: Count Valid Paths in a Tree -- the bench, as
# paths.kara: 10 trees of 10^5 nodes, each answered 10 times by the
# disjoint-set arm.

def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    at = x
    while parent[at] != root:
        nxt = parent[at]
        parent[at] = root
        at = nxt
    return root


def count_paths(n, edges):
    prime = [True] * (n + 1)
    prime[0] = False
    prime[1] = False
    i = 2
    while i * i <= n:
        if prime[i]:
            for j in range(i * i, n + 1, i):
                prime[j] = False
        i += 1
    parent = list(range(n + 1))
    size = [1] * (n + 1)
    around = [[] for _ in range(n + 1)]
    for a, b in edges:
        if prime[a] or prime[b]:
            around[a].append(b)
            around[b].append(a)
        else:
            ra, rb = find(parent, a), find(parent, b)
            if ra != rb:
                parent[ra] = rb
                size[rb] += size[ra]
    count = 0
    for p in range(2, n + 1):
        if prime[p]:
            before = 0
            for v in around[p]:
                if not prime[v]:
                    s = size[find(parent, v)]
                    count += s + s * before
                    before += s
    return count


seed = 2867


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 10, 10, 100000
    trees = []
    for c in range(count):
        edges = []
        for v in range(2, n + 1):
            reach = min(v - 1, 5) if c % 2 == 1 else v - 1
            edges.append([v - 1 - wide() % reach, v])
        trees.append(edges)
    total = 0
    check = 0
    for r in range(rounds):
        for edges in trees:
            paths = count_paths(n, edges)
            total += paths
            check = (check * 31 + paths % 1000000007 + r) % 1000000007
    print(f"{count} trees of {n}, {rounds} rounds: {total} paths, checksum {check}")


main()
