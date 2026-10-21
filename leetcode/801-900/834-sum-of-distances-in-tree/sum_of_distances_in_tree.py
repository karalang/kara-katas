# Python mirror of the ★ arm plus harness for kata 834.

def sum_of_distances_in_tree(n, edges):
    adj = [[] for _ in range(n)]
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

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def random_tree(n, reach):
    label = list(range(n))
    i = n
    while i > 1:
        j = next_random() % i
        i -= 1
        label[i], label[j] = label[j], label[i]
    edges = []
    for v in range(1, n):
        lo = v - reach if v > reach else 0
        u = lo + next_random() % (v - lo)
        if next_random() % 2 == 0:
            edges.append((label[u], label[v]))
        else:
            edges.append((label[v], label[u]))
    k = len(edges)
    while k > 1:
        j = next_random() % k
        k -= 1
        edges[k], edges[j] = edges[j], edges[k]
    return edges

def show(n, edges):
    print(f"n = {n}, edges = [{', '.join(f'({a}, {b})' for a, b in edges)}] -> [{', '.join(map(str, sum_of_distances_in_tree(n, edges)))}]")

def fold(check, answer):
    c = check
    for x in answer:
        c = (c * 1000003 + x) % 1000000007
    return c

def main():
    global seed
    show(6, [(0, 1), (0, 2), (2, 3), (2, 4), (2, 5)])
    show(1, [])
    show(2, [(1, 0)])
    show(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
    show(5, [(3, 0), (3, 1), (3, 2), (3, 4)])
    show(7, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    seed = 834
    n = 30000
    for reach in [1, n, 3]:
        if reach == 1:
            tree = [(v - 1, v) for v in range(1, n)]
        elif reach == n:
            tree = [(0, v) for v in range(1, n)]
        else:
            tree = random_tree(n, reach)
        answer = sum_of_distances_in_tree(n, tree)
        print(f"30000 nodes, reach {reach}: least {min(answer)}, greatest {max(answer)}, checksum {fold(0, answer)}")
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 60
        reach = 1 + next_random() % n
        answer = sum_of_distances_in_tree(n, random_tree(n, reach))
        total += sum(answer)
        check = fold(check, answer)
    print(f"300 random trees: answers total {total}, checksum {check}")

main()
