# LeetCode #1379 bench -- Python: the ★ arm: the two trees walked
# together, depth first; the clone's node where the original's is the
# target itself (`is`) is the answer.

import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def find(o, c, target):
    if o is target:
        return c
    if o.left is not None and c.left is not None:
        found = find(o.left, c.left, target)
        if found is not None:
            return found
    if o.right is not None and c.right is not None:
        return find(o.right, c.right, target)
    return None


def get_target_copy(original, cloned, target):
    return find(original, cloned, target)


seed = 1379


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def clone_tree(node):
    copy = TreeNode(node.val)
    if node.left is not None:
        copy.left = clone_tree(node.left)
    if node.right is not None:
        copy.right = clone_tree(node.right)
    return copy


def main():
    # 10 trees of 10^4 nodes built once, with their clones; then 3000
    # rounds, each asking one tree's clone for the copy of one node (see
    # the Kāra bench)
    n = 10000
    trees = []
    for _ in range(10):
        root = TreeNode(1)
        nodes = [root]
        open_places = [(root, True), (root, False)]
        for k in range(1, n):
            at = next_random() % len(open_places)
            parent, left = open_places[at]
            open_places[at] = open_places[-1]
            open_places.pop()
            node = TreeNode(k + 1)
            if left:
                parent.left = node
            else:
                parent.right = node
            open_places.append((node, True))
            open_places.append((node, False))
            nodes.append(node)
        trees.append((root, clone_tree(root), nodes))
    check = 0
    for r in range(3000):
        original, cloned, nodes = trees[check % 10]
        target = nodes[(check // 10 + r) % n]
        found = get_target_copy(original, cloned, target)
        own = 0 if found is target else 1
        check = (check * 31 + found.val * 2 + own + r) % 1000000007
    print(f"3000 rounds over 10 trees of 10000 nodes: checksum {check}")


main()
