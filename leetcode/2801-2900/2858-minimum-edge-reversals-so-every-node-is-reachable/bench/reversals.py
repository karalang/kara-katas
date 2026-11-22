# LeetCode #2858: Minimum Edge Reversals So Every Node Is Reachable --
# the bench: the ★ arm over 20 random trees of 10^5 nodes, LeetCode's
# most, every other one deep, labels shuffled and each edge pointing
# either way, all drawn first, then each answered 5 times.


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


def main():
    count, rounds, n = 20, 5, 100000
    seed = 2858

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide():
        a = nr()
        return a * 32768 + nr()

    def tree(n, deep):
        label = list(range(n))
        for i in range(n - 1, 0, -1):
            j = wide() % (i + 1)
            label[i], label[j] = label[j], label[i]
        edges = []
        for i in range(1, n):
            p = i - 1 - nr() % min(i, 3) if deep else wide() % i
            if nr() % 2 == 0:
                edges.append((label[p], label[i]))
            else:
                edges.append((label[i], label[p]))
        return edges

    trees = [tree(n, c % 2 == 1) for c in range(count)]
    total = check = 0
    for r in range(rounds):
        for edges in trees:
            for a in min_edge_reversals(n, edges):
                total += a
                check = (check * 31 + a + r) % 1000000007
    print(f"{count} trees of {n}, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
