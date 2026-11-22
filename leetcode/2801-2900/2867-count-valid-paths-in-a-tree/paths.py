# LeetCode #2867: Count Valid Paths in a Tree -- the Python mirror of
# the ★ arm (paths.kara): a disjoint-set union over the edges between
# non-primes, then for each prime its neighbours' component sizes
# walked, each adding itself and itself times the sizes before it.


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
    print(f"{count_paths(5, [[1, 2], [1, 3], [2, 4], [2, 5]])} {count_paths(6, [[1, 2], [1, 3], [2, 4], [3, 5], [3, 6]])}")
    n = 100000
    path = [[i, i + 1] for i in range(1, n)]
    star = [[2, i] for i in range(1, n + 1) if i != 2]
    print(f"{count_paths(n, path)} {count_paths(n, star)}")
    seed = 2867
    total = 0
    check = 0
    for c in range(3030):
        small = c < 3000
        n = next_random() % 10 + 1 if small else wide() % 90001 + 10000
        edges = []
        for v in range(2, n + 1):
            reach = min(v - 1, 5) if not small and c % 2 == 1 else v - 1
            parent = v - 1 - wide() % reach
            edges.append([parent, v])
        paths = count_paths(n, edges)
        total += paths
        check = (check * 31 + paths) % 1000000007
        if c == 2999:
            print(f"3000 small trees: {total} paths, checksum {check}")
            total = 0
            check = 0
    print(f"30 large trees: {total} paths, checksum {check}")


main()
