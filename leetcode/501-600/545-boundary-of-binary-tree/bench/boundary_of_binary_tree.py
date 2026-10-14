# Benchmark for #545: Python mirror of the ★ arm (three walks); see
# boundary_of_binary_tree.kara.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def is_leaf(n):
    return n.left is None and n.right is None


def leaves(node, out):
    if node is not None:
        if is_leaf(node):
            out.append(node.val)
        else:
            leaves(node.left, out)
            leaves(node.right, out)


def boundary_of_binary_tree(root):
    out = []
    if root is None:
        return out
    out.append(root.val)
    if is_leaf(root):
        return out
    node = root.left
    while node is not None and not is_leaf(node):
        out.append(node.val)
        node = node.left if node.left is not None else node.right
    leaves(root.left, out)
    leaves(root.right, out)
    right = []
    node = root.right
    while node is not None and not is_leaf(node):
        right.append(node.val)
        node = node.right if node.right is not None else node.left
    out.extend(reversed(right))
    return out


seed = 545


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 random trees of 10,000 nodes (the problem's most) with values
    # from -1,000 to 1,000, each new node walking down from the root and
    # going left with chance 50 to 88 in 100, built once, the nodes kept
    # in the order they were added. Then 200 times over every tree the
    # subtree at one of its first 16 nodes, picked by the round and the
    # tree, is answered; every value on the boundary goes into the
    # checksum.
    trees = 20
    all_trees = []
    for g in range(trees):
        lean = 50 + 2 * g
        root = TreeNode(next_random() % 2001 - 1000)
        nodes = [root]
        for _ in range(1, 10000):
            c = TreeNode(next_random() % 2001 - 1000)
            node = root
            while True:
                if next_random() % 100 < lean:
                    if node.left is not None:
                        node = node.left
                    else:
                        node.left = c
                        break
                else:
                    if node.right is not None:
                        node = node.right
                    else:
                        node.right = c
                        break
            nodes.append(c)
        all_trees.append(nodes)
    total = 0
    checksum = 0
    for r in range(200):
        for t in range(trees):
            b = boundary_of_binary_tree(all_trees[t][(r * 37 + t * 11) % 16])
            total += len(b)
            for v in b:
                checksum = (checksum * 31 + v + 1001) % 1000000007
    print(f"{trees} trees, 200 times each: {total} on the boundary, checksum {checksum}")


main()
