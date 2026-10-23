# LeetCode #872: Leaf-Similar Trees -- Python mirror of the bench program
# (the ★ arm, the leaves of each collected by recursion).


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def leaf_similar(root1, root2):
    first, second = [], []
    leaves(root1, first)
    leaves(root2, second)
    return first == second


def leaves(node, out):
    if node is not None:
        if node.left is None and node.right is None:
            out.append(node.val)
        else:
            leaves(node.left, out)
            leaves(node.right, out)


seed = 872


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n, limit):
    nodes = []
    for k in range(n):
        node = TreeNode(next_random() % limit)
        if k > 0:
            while True:
                parent = nodes[next_random() % len(nodes)]
                if next_random() % 2 == 0:
                    if parent.left is None:
                        parent.left = node
                        break
                elif parent.right is None:
                    parent.right = node
                    break
        nodes.append(node)
    return nodes[0] if n else None


def tree_with_leaves(vals, lo, hi, limit):
    if hi - lo == 1:
        return TreeNode(vals[lo])
    mid = lo + 1 + next_random() % (hi - lo - 1)
    left = tree_with_leaves(vals, lo, mid, limit)
    right = tree_with_leaves(vals, mid, hi, limit)
    return TreeNode(next_random() % limit, left, right)


def main():
    pairs = []
    for k in range(2000):
        a = random_tree(200, 201)
        if k % 2 == 0:
            vals = []
            leaves(a, vals)
            pairs.append((a, tree_with_leaves(vals, 0, len(vals), 201)))
        else:
            pairs.append((a, random_tree(200, 201)))
    check = 0
    for _, b in pairs:
        vals = []
        leaves(b, vals)
        for v in vals:
            check = (check * 31 + v + 1) % 1000000007
    similar = 0
    for _ in range(50):
        for a, b in pairs:
            if leaf_similar(a, b):
                similar += 1
    print(f"100000 comparisons of 2000 pairs: {similar} leaf-similar, leaf checksum {check}")


main()
