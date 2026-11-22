# LeetCode #2764: Is Array a Preorder of Some Binary Tree -- the ★ arm in
# Python (preorder.kara): a stack of the nodes whose subtrees are still
# open; each node closes every subtree above its parent, and fails when
# its parent is not open at all.


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
        while True:
            p = wide() % k
            if len(kids[p]) < 2:
                break
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
        ks = kids[u]
        if len(ks) == 2 and next_random() % 2 == 1:
            ks = [ks[1], ks[0]]
        for c in reversed(ks):
            stack.append(c)
    nodes = [[ids[u], ids[parent[u]] if parent[u] >= 0 else -1] for u in order]
    if next_random() % 2 == 1 and n > 1:
        i = wide() % n
        j = wide() % n
        nodes[i], nodes[j] = nodes[j], nodes[i]
    return nodes


def show(b):
    return "true" if b else "false"


def main():
    print(show(is_preorder([[0, -1], [1, 0], [2, 0], [3, 2], [4, 2]])))
    print(show(is_preorder([[0, -1], [1, 0], [2, 0], [3, 1], [4, 1]])))
    print(show(is_preorder([[7, -1]])))
    chain = [[0, -1]] + [[k, k - 1] for k in range(1, 100000)]
    print(show(is_preorder(chain)))
    chain[1], chain[2] = chain[2], chain[1]
    print(show(is_preorder(chain)))
    print(show(is_preorder([[5, -1], [3, 5], [9, 5], [1, 3]])))
    good = 0
    check = 0
    for c in range(3000):
        n = next_random() % 12 + 1
        if is_preorder(tree(n)):
            good += 1
            check = (check * 31 + c) % 1000000007
    print(f"3000 small trees: {good} preorders, checksum {check}")
    good = 0
    check = 0
    for c in range(10):
        if is_preorder(tree(100000)):
            good += 1
            check = (check * 31 + c) % 1000000007
    print(f"10 trees of 100000: {good} preorders, checksum {check}")


main()
