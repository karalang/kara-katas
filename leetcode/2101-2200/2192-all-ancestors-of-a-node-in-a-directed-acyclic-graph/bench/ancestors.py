# benchmark's Python mirror of ancestors.kara (LeetCode #2192, the ★
# arm): a walk down from every node by a stack.


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


def random_dag():
    order = list(range(1000))
    for i in range(999, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    edges = []
    while len(edges) < 2000:
        a = next_random() % 1000
        b = next_random() % 1000
        if a < b:
            edges.append([order[a], order[b]])
        elif b < a:
            edges.append([order[b], order[a]])
    return edges


def main():
    dags = [random_dag() for _ in range(20)]
    check = 0
    for r in range(2000):
        for lst in get_ancestors(1000, dags[r % 20]):
            check = (check * 31 + len(lst)) % 1000000007
            for a in lst:
                check = (check * 31 + a + 1) % 1000000007
    print(f"2000 solves: checksum {check}")


main()
