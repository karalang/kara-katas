# LeetCode #2764: Is Array a Preorder of Some Binary Tree -- the bench
# (preorder.kara in Python): a stack of the nodes whose subtrees are
# still open, each node closing every subtree above its parent.


def is_preorder(nodes):
    stack = []
    for node_id, parent in nodes:
        while stack and stack[-1] != parent:
            stack.pop()
        if not stack and parent != -1:
            return False
        stack.append(node_id)
    return True


seed = 2764


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def tree(n):
    # a random binary tree of n nodes, ids spread over 0 to 100000, listed
    # in a random preorder; then, half the time, two places swapped
    shift = wide() % 100001
    ids = [(k * 37 + shift) % 100001 for k in range(n)]
    kids = [[] for _ in range(n)]
    for k in range(1, n):
        p = wide() % k
        while len(kids[p]) == 2:
            p = wide() % k
        kids[p].append(k)
    parent = [-1] * n
    for p in range(n):
        for c in kids[p]:
            parent[c] = p
    order = []
    stack = [0]
    while stack:
        u = stack.pop()
        order.append(u)
        ks = list(kids[u])
        if len(ks) == 2 and next_random() % 2 == 1:
            ks[0], ks[1] = ks[1], ks[0]
        for c in reversed(ks):
            stack.append(c)
    nodes = [[ids[u], ids[parent[u]] if parent[u] >= 0 else -1] for u in order]
    if next_random() % 2 == 1 and n > 1:
        i = wide() % n
        j = wide() % n
        nodes[i], nodes[j] = nodes[j], nodes[i]
    return nodes


def main():
    count, rounds = 20, 100
    cases = [tree(100000) for _ in range(count)]
    good = check = 0
    for r in range(rounds):
        for c, nodes in enumerate(cases):
            if is_preorder(nodes):
                good += 1
                check = (check * 31 + c + r) % 1000000007
    print(f"{count} trees of 100000, {rounds} rounds: {good} preorders, checksum {check}")


main()
