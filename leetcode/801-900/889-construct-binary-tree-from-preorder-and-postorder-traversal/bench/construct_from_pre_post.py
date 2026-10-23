# LeetCode #889 bench: recursion with a table of postorder positions, on
# 4000 random trees of 1,000 nodes, half of them full. The same algorithm
# as construct_from_pre_post.kara.

import sys

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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    global seed
    seed = 889
    total = 0
    check = 0
    for c in range(4000):
        full = c % 2 == 0
        n = 999 if full else 1000
        tree = random_tree(n, full)
        pre = []
        post = []
        walk(tree, pre, post)
        root = construct_from_pre_post(pre, post)
        # the rebuilt tree in level order, 0 for a missing child
        queue = deque()
        if root is not None:
            check = (check * 131 + root.val) % 1000000007
            queue.append(root)
        while queue:
            node = queue.popleft()
            total += 1
            if node.left is not None:
                check = (check * 131 + node.left.val) % 1000000007
                queue.append(node.left)
            else:
                check = check * 131 % 1000000007
            if node.right is not None:
                check = (check * 131 + node.right.val) % 1000000007
                queue.append(node.right)
            else:
                check = check * 131 % 1000000007
    print(f"4000 trees of up to 1000 nodes: {total} nodes rebuilt, checksum {check}")


sys.setrecursionlimit(10000)
main()
