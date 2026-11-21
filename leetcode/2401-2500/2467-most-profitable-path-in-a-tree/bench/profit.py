# LeetCode #2467: Most Profitable Path in a Tree -- the bench, the ★ arm in
# Python: breadth-first parents and depths from node 0, Bob's seconds up
# his parent chain, and each node's income its parent's plus its gate.


def most_profitable_path(edges, bob, amount):
    n = len(amount)
    adjacent = [[] for _ in range(n)]
    for a, b in edges:
        adjacent[a].append(b)
        adjacent[b].append(a)
    parent = [-1] * n
    depth = [0] * n
    order = [0]
    parent[0] = 0
    nxt = 0
    while nxt < len(order):
        node = order[nxt]
        nxt += 1
        for child in adjacent[node]:
            if parent[child] < 0:
                parent[child] = node
                depth[child] = depth[node] + 1
                order.append(child)
    bob_time = [n] * n
    node = bob
    t = 0
    while node != 0:
        bob_time[node] = t
        node = parent[node]
        t += 1
    bob_time[0] = t
    income = [0] * n
    best = -(1 << 63)
    for node in order:
        if depth[node] < bob_time[node]:
            gate = amount[node]
        elif depth[node] == bob_time[node]:
            gate = int(amount[node] / 2)
        else:
            gate = 0
        income[node] = gate if node == 0 else income[parent[node]] + gate
        if node != 0 and len(adjacent[node]) == 1:
            best = max(best, income[node])
    return best


seed = 2467


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 10 random trees of 10^4 nodes built once, each node joined to an
    # earlier one, with even amounts from -10^4 to 10^4; then 140
    # passes, each moving every tree's Bob and setting one amount from the
    # checksum so far, then answering it and folding the answer plus the
    # pass into the checksum
    n = 10000
    trees = []
    amounts = []
    for _ in range(10):
        edges = []
        for node in range(1, n):
            r = next_random()
            edges.append([node, (r * 32768 + next_random()) % node])
        trees.append(edges)
        amounts.append([2 * (next_random() % 10001) - 10000 for _ in range(n)])
    check = 0
    for p in range(140):
        for a in range(len(trees)):
            bob = 1 + check % (n - 1)
            amounts[a][(check + a) % n] = 2 * (check % 10001) - 10000
            got = most_profitable_path(trees[a], bob, amounts[a])
            check = (check * 31 + got + p) % 1000000007
    print(f"140 passes over 10 trees of 10^4: checksum {check}")


main()
