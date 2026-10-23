# LeetCode #872: Leaf-Similar Trees -- the leaves of each, collected by
# recursion; a mirror of leaf_similar_trees.kara, its output
# byte-identical.

import collections
import sys

sys.setrecursionlimit(10000)


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


# ---- test harness ----------------------------------------------------------

seed = 0
largest = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = collections.deque([root])
    i = 1
    while i < len(vals):
        node = queue.popleft()
        if vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals):
            if vals[i] is not None:
                node.right = TreeNode(vals[i])
                queue.append(node.right)
            i += 1
    return root


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


def leaf_nodes(node, out):
    if node is not None:
        if node.left is None and node.right is None:
            out.append(node)
        else:
            leaf_nodes(node.left, out)
            leaf_nodes(node.right, out)


def tree_with_leaves(vals, lo, hi, limit, chains):
    if hi - lo == 1:
        leaf = TreeNode(vals[lo])
        if chains and next_random() % 3 == 0:
            if next_random() % 2 == 0:
                return TreeNode(next_random() % limit, leaf, None)
            return TreeNode(next_random() % limit, None, leaf)
        return leaf
    mid = lo + 1 + next_random() % (hi - lo - 1)
    left = tree_with_leaves(vals, lo, mid, limit, chains)
    right = tree_with_leaves(vals, mid, hi, limit, chains)
    return TreeNode(next_random() % limit, left, right)


def leaf_similar_to(root, limit, chains):
    nodes = []
    leaf_nodes(root, nodes)
    vals = [n.val for n in nodes]
    return tree_with_leaves(vals, 0, len(vals), limit, chains)


def size(node):
    return 0 if node is None else 1 + size(node.left) + size(node.right)


def show(vals1, vals2):
    text1 = ", ".join("null" if v is None else str(v) for v in vals1)
    text2 = ", ".join("null" if v is None else str(v) for v in vals2)
    answer = leaf_similar(from_level_order(vals1), from_level_order(vals2))
    print(f"root1 = [{text1}], root2 = [{text2}] -> {str(answer).lower()}")


def main():
    global seed, largest
    show([3, 5, 1, 6, 2, 9, 8, None, None, 7, 4], [3, 5, 1, 6, 7, 4, 2, None, None, None, None, None, None, 9, 8])
    show([1, 2, 3], [1, 3, 2])
    show([1], [1])
    show([1], [2])
    show([1, 2], [2])
    show([1, 2], [3, None, 2])
    show([1, 2, 3], [4, 2, 5, None, None, 3])
    show([1, 2, 3], [1, 2, 3, 3])
    show([1, 12, 3], [1, 1, 23])
    show([0, 200, 200], [200, 200, 200, 0, 200])
    seed = 872
    similar = 0
    for k in range(3000):
        n1 = k % 12 + 1
        a = random_tree(n1, 4)
        b = leaf_similar_to(a, 4, True) if k % 2 == 0 else random_tree(next_random() % 12 + 1, 4)
        if leaf_similar(a, b):
            similar += 1
    print(f"3000 pairs of up to 12 nodes: {similar} leaf-similar")
    similar = 0
    check = 0
    for k in range(200):
        a = random_tree(200, 201)
        b = random_tree(200, 201) if k % 4 == 0 else leaf_similar_to(a, 201, False)
        largest = max(largest, size(b))
        if k % 4 == 1:
            bl = []
            leaf_nodes(b, bl)
            i = next_random() % len(bl)
            bl[i].val = (bl[i].val + 1) % 201
        answer = leaf_similar(a, b)
        if answer:
            similar += 1
        check = (check * 3 + (1 if answer else 2)) % 1000000007
    print(f"200 pairs of 200 nodes: {similar} leaf-similar, checksum {check}")
    print(f"largest second tree: {largest}", file=sys.stderr)


main()
