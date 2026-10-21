# Benchmark for #834: Sum of Distances in Tree -- the ★ arm (rerooting, with a stack).
#
# Mirrors sum_of_distances_in_tree.kara: one walk from node 0 on an
# explicit stack records parents and a visiting order; the order taken
# backwards gives subtree sizes and distance sums, and taken forwards
# moves the root along each edge.


def sum_of_distances_in_tree(n, edges):
    adj = []
    for _ in range(n):
        adj.append([])
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent = [-1] * n
    order = []
    seen = [False] * n
    stack = [0]
    seen[0] = True
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                stack.append(v)
    size = [1] * n
    down = [0] * n
    for j in range(n):
        u = order[n - 1 - j]
        p = parent[u]
        if p >= 0:
            size[p] += size[u]
            down[p] += down[u] + size[u]
    answer = [0] * n
    answer[0] = down[0]
    for u in order:
        p = parent[u]
        if p >= 0:
            answer[u] = answer[p] - size[u] + (n - size[u])
    return answer


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    # 16 trees drawn once, each of LeetCode's largest size, 30000 nodes:
    # node v > 0 hangs from a node among the `reach` before it, `reach`
    # running from 2 to 2^16 over the trees, with the labels shuffled.
    # Each round solves the next tree and reads one answer.
    count = 16
    rounds = 320
    n = 30000
    seed = [834]
    trees = []
    for g in range(count):
        reach = 2 << g
        label = list(range(n))
        i = n
        while i > 1:
            j = next_random(seed) % i
            i -= 1
            label[i], label[j] = label[j], label[i]
        edges = []
        for v in range(1, n):
            lo = v - reach if v > reach else 0
            u = lo + next_random(seed) % (v - lo)
            edges.append((label[u], label[v]))
        trees.append(edges)
    total = 0
    checksum = 0
    for round_ in range(rounds):
        answer = sum_of_distances_in_tree(n, trees[round_ % count])
        x = answer[round_ * 7919 % n]
        total += x
        checksum = (checksum * 131 + x) % 1000000007
    print(f"{rounds} rounds of {count} trees: answers total {total}, checksum {checksum}")


main()
