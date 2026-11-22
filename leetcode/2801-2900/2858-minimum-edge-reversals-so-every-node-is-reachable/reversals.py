# LeetCode #2858: Minimum Edge Reversals So Every Node Is Reachable --
# the ★ arm's mirror: the reversals from node 0 counted down a walk of
# an explicit stack, then the root moved across each edge in that
# order, one more for an edge pointing away and one less for one
# pointing back.


def min_edge_reversals(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append((v, 0))
        adj[v].append((u, 1))
    parent = [-1] * n
    cost = [0] * n
    order = []
    stack = [0]
    parent[0] = 0
    root = 0
    while stack:
        u = stack.pop()
        order.append(u)
        for v, w in adj[u]:
            if parent[v] == -1:
                parent[v] = u
                cost[v] = w
                root += w
                stack.append(v)
    answer = [0] * n
    answer[0] = root
    for u in order[1:]:
        answer[u] = answer[parent[u]] + (1 if cost[u] == 0 else -1)
    return answer


seed = 2858


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def tree(n, deep):
    label = list(range(n))
    for i in range(n - 1, 0, -1):
        j = wide() % (i + 1)
        label[i], label[j] = label[j], label[i]
    edges = []
    for i in range(1, n):
        p = i - 1 - next_random() % min(i, 3) if deep else wide() % i
        if next_random() % 2 == 0:
            edges.append([label[p], label[i]])
        else:
            edges.append([label[i], label[p]])
    return edges


def fold(answer):
    check = 0
    for a in answer:
        check = (check * 31 + a) % 1000000007
    return sum(answer), check


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    print(f"{show(min_edge_reversals(4, [[2, 0], [2, 1], [1, 3]]))} {show(min_edge_reversals(3, [[1, 2], [2, 0]]))}")
    n = 100000
    on = [[i - 1, i] for i in range(1, n)]
    turns = [[i - 1, i] if i % 2 == 0 else [i, i - 1] for i in range(1, n)]
    star = [[i, 0] for i in range(1, n)]
    a, b = fold(min_edge_reversals(n, on))
    c, d = fold(min_edge_reversals(n, turns))
    e, f = fold(min_edge_reversals(n, star))
    print(f"path {a} {b}, turns {c} {d}, star {e} {f}")
    total = check = 0
    for c in range(3020):
        small = c < 3000
        n = next_random() % 8 + 2 if small else wide() % 90001 + 10000
        edges = tree(n, c % 2 == 1)
        s, h = fold(min_edge_reversals(n, edges))
        total += s
        check = (check * 31 + h) % 1000000007
        if c == 2999:
            print(f"3000 small trees: answers sum to {total}, checksum {check}")
            total = check = 0
    print(f"20 large trees: answers sum to {total}, checksum {check}")


main()
