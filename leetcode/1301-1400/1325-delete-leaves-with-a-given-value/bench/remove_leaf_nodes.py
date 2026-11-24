# LeetCode #1325 bench, Python mirror of the Kāra bench: the ★ arm (a
# recursive walk that settles both children first and deletes a leaf with
# the target's value) on 30 trees of 3000 nodes with values from 1 to 3,
# built once, every other one run deep; then 300 passes, each setting one
# node of every tree and the target from the checksum so far, linking every
# node back to its children, answering it, and folding the nodes left, the
# root's value and the pass into the checksum.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def remove_leaf_nodes(root, target):
    if root is None:
        return None
    root.left = remove_leaf_nodes(root.left, target)
    root.right = remove_leaf_nodes(root.right, target)
    if root.left is None and root.right is None and root.val == target:
        return None
    return root


def count(node):
    if node is None:
        return 0
    return 1 + count(node.left) + count(node.right)


seed = 1325


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(n, deep):
    nodes, left, right = [], [], []
    places = [(0, True), (0, False)]
    for i in range(n):
        nodes.append(TreeNode(1 + next_random() % 3))
        left.append(-1)
        right.append(-1)
        if i > 0:
            r = next_random()
            if deep and r % 4 != 0:
                at = len(places) - 1 - next_random() % 2
            else:
                at = next_random() % len(places)
            parent, is_left = places[at]
            places[at] = places[-1]
            places.pop()
            if is_left:
                left[parent] = i
            else:
                right[parent] = i
            places.append((i, True))
            places.append((i, False))
    return nodes, left, right


def main():
    n = 3000
    trees = [build(n, t % 2 == 1) for t in range(30)]
    check = 0
    for p in range(300):
        for t in range(30):
            nodes, left, right = trees[t]
            nodes[check % n].val = 1 + (check // 7) % 3
            target = 1 + (check // 11) % 3
            for i in range(n):
                node = nodes[i]
                node.left = nodes[left[i]] if left[i] >= 0 else None
                node.right = nodes[right[i]] if right[i] >= 0 else None
            root = remove_leaf_nodes(nodes[0], target)
            top = root.val if root is not None else 0
            check = (check * 31 + count(root) * 7 + top + p) % 1000000007
    print(f"300 passes over 30 trees of 3000: checksum {check}")


main()
