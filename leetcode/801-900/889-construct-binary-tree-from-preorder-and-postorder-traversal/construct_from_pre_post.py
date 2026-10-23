# LeetCode #889: Construct Binary Tree from Preorder and Postorder
# Traversal -- Python mirror of the recursion with a table of postorder
# positions in construct_from_pre_post.kara, with the same test harness.
#
# The preorder starts with the root and then its left child, which is
# the root of the left subtree; that child's position in the postorder
# ends the left subtree there, so its size is known, and the rest of the
# preorder after it is the right subtree. A table gives each value's
# postorder position. When a node has one child the traversals cannot
# tell which side it hangs on, and LeetCode accepts either; this arm, like
# the others, puts a lone child on the left. O(n).

from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def construct_from_pre_post(preorder, postorder):
    at = [0] * (len(preorder) + 1)
    for i, v in enumerate(postorder):
        at[v] = i
    return build(preorder, at, 0, len(preorder) - 1, 0)


# the subtree whose preorder is preorder[lo..=hi] and whose postorder
# starts at post_lo
def build(preorder, at, lo, hi, post_lo):
    if lo > hi:
        return None
    node = TreeNode(preorder[lo])
    if lo < hi:
        size = at[preorder[lo + 1]] - post_lo + 1
        node.left = build(preorder, at, lo + 1, lo + size, post_lo)
        node.right = build(preorder, at, lo + size + 1, hi, post_lo + size)
    return node


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# LeetCode's level order of a tree, "null" for a missing child, with the
# trailing nulls dropped.
def to_level_order(root):
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append("null")
        else:
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] == "null":
        out.pop()
    return "[" + ", ".join(out) + "]"


def walk(node, pre, post):
    if node is not None:
        pre.append(node.val)
        walk(node.left, pre, post)
        walk(node.right, pre, post)
        post.append(node.val)


# A random tree of n nodes holding the values 1 to n in a random order,
# built as in the Kāra harness.
def random_tree(n, full):
    vals = list(range(1, n + 1))
    for i in range(1, n):
        j = next_random() % (i + 1)
        vals[i], vals[j] = vals[j], vals[i]
    nodes = [TreeNode(vals[0])]
    if full:
        leaves = [nodes[0]]
        while len(nodes) + 2 <= n:
            k = next_random() % len(leaves)
            leaf = leaves[k]
            leaves[k] = leaves[-1]
            leaves.pop()
            a = TreeNode(vals[len(nodes)])
            b = TreeNode(vals[len(nodes) + 1])
            leaf.left = a
            leaf.right = b
            nodes.append(a)
            nodes.append(b)
            leaves.append(a)
            leaves.append(b)
    else:
        for k in range(1, n):
            node = TreeNode(vals[k])
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
    return nodes[0]


def show(preorder, postorder):
    a = ", ".join(str(v) for v in preorder)
    b = ", ".join(str(v) for v in postorder)
    print(f"preorder = [{a}], postorder = [{b}] -> {to_level_order(construct_from_pre_post(preorder, postorder))}")


def main():
    global seed
    show([1, 2, 4, 5, 3, 6, 7], [4, 5, 2, 6, 7, 3, 1])
    show([1], [1])
    show([1, 2], [2, 1])
    show([1, 2, 3], [3, 2, 1])
    show([1, 2, 3], [2, 3, 1])
    show([3, 1, 2, 4], [2, 1, 4, 3])
    show([1, 2, 3, 4, 5], [3, 4, 2, 5, 1])
    # random trees of up to 30 nodes, LeetCode's largest; every third one
    # full, which the traversals fix exactly
    seed = 889
    same = 0
    check = 0
    for c in range(3000):
        full = c % 3 == 0
        n = 2 * (next_random() % 15) + 1 if full else 1 + next_random() % 30
        tree = random_tree(n, full)
        pre = []
        post = []
        walk(tree, pre, post)
        text = to_level_order(construct_from_pre_post(pre, post))
        if text == to_level_order(tree):
            same += 1
        for b in text.encode():
            check = (check * 131 + b) % 1000000007
    print(f"3000 trees of up to 30 nodes: {same} rebuilt as they were, checksum {check}")


main()
