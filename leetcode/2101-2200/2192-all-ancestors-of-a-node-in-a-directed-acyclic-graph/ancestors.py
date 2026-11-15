# Python mirror of ancestors.kara (LeetCode #2192, the ★ arm): a walk
# down the edges from every node in turn, by a stack; every node reached
# gets the start as an ancestor.


def get_ancestors(n, edges):
    children = [[] for _ in range(n)]
    for a, b in edges:
        children[a].append(b)
    ancestors = [[] for _ in range(n)]
    for start in range(n):
        seen = [False] * n
        seen[start] = True
        stack = [start]
        while stack:
            u = stack.pop()
            for v in children[u]:
                if not seen[v]:
                    seen[v] = True
                    ancestors[v].append(start)
                    stack.append(v)
    return ancestors


seed = 2192


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_dag(n, want):
    order = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    taken = set()
    edges = []
    if n < 2:
        return edges
    for _ in range(want):
        a = next_random() % n
        b = next_random() % n
        if a != b:
            lo, hi = min(a, b), max(a, b)
            if lo * n + hi not in taken:
                taken.add(lo * n + hi)
                edges.append([order[lo], order[hi]])
    return edges


def checksum(lists, c):
    for lst in lists:
        c = (c * 31 + len(lst)) % 1000000007
        for a in lst:
            c = (c * 31 + a + 1) % 1000000007
    return c


def fmt(xs):
    return "[" + ", ".join(fmt(x) if isinstance(x, list) else str(x) for x in xs) + "]"


def show(n, edges):
    print(f"{n}, {fmt(edges)} -> {fmt(get_ancestors(n, edges))}")


show(8, [[0, 3], [0, 4], [1, 3], [2, 4], [2, 7], [3, 5], [3, 6], [3, 7], [4, 6]])
show(5, [[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]])
show(1, [])
show(3, [])
show(4, [[3, 2], [2, 1], [1, 0]])
show(5, [[4, 0], [3, 0], [2, 4], [1, 3], [2, 1]])
total = check = 0
for rnd in range(300):
    n = next_random() % 25 + 1
    want = n if rnd % 2 == 0 else n * n // 2
    edges = random_dag(n, want)
    lists = get_ancestors(n, edges)
    total += sum(len(x) for x in lists)
    check = checksum(lists, check)
print(f"300 DAGs: {total} ancestors, checksum {check}")
edges = random_dag(1000, 2000)
lists = get_ancestors(1000, edges)
most = max(len(x) for x in lists)
print(f"1000 nodes, {len(edges)} edges: most ancestors {most}, checksum {checksum(lists, 0)}")
