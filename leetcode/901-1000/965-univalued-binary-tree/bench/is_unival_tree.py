# Benchmark: LeetCode #965 Univalued Binary Tree -- the ★ arm, depth
# first, on trees of 100 nodes, LeetCode's largest. Mirrors
# is_unival_tree.kara, .c, .rs and go-seq/.


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def holds(t, v):
    if t is None:
        return True
    return t.val == v and holds(t.left, v) and holds(t.right, v)


def is_unival_tree(root):
    if root is None:
        return True
    return holds(root.left, root.val) and holds(root.right, root.val)


seed = 965


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def attach(root, node):
    cur = root
    while True:
        if next_random() % 2 == 0:
            if cur.left is not None:
                cur = cur.left
            else:
                cur.left = node
                return
        else:
            if cur.right is not None:
                cur = cur.right
            else:
                cur.right = node
                return


def make_tree(kind, n):
    v = next_random() % 100
    vals = [v] * n
    if kind == 3:
        for i in range(n):
            vals[i] = next_random() % 2
    else:
        for _ in range(kind):
            k = next_random() % n
            vals[k] = next_random() % 100
    root = TreeNode(vals[0])
    for i in range(1, n):
        attach(root, TreeNode(vals[i]))
    return root


def main():
    rounds = 4000
    trees = [make_tree(i % 4, 100) for i in range(200)]
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(200):
            bit = 1 if is_unival_tree(trees[(r + i) % 200]) else 0
            total += bit
            check = (check * 31 + bit + 1 + i) % 1000000007
    print(f"{rounds} rounds over 200 trees of 100 nodes: {total} univalued, checksum {check}")


main()
