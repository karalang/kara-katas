# LeetCode #623: Add One Row to Tree -- Python mirror of the Kāra bench.
#
# The ★ arm's recursion with the level, on the same trees and rounds,
# each row taken out again by the same `undo`.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def add_one_row(root, val, depth):
    if depth == 1:
        return TreeNode(val, root, None)
    insert(root, val, depth, 1)
    return root


def insert(node, val, depth, level):
    if node is not None:
        if level == depth - 1:
            node.left = TreeNode(val, node.left, None)
            node.right = TreeNode(val, None, node.right)
        else:
            insert(node.left, val, depth, level + 1)
            insert(node.right, val, depth, level + 1)


seed = 623


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(size, lean):
    root = TreeNode(next_random() % 201 - 100)
    for _ in range(1, size):
        c = TreeNode(next_random() % 201 - 100)
        node = root
        while True:
            if next_random() % 100 < lean:
                if node.left is None:
                    node.left = c
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = c
                    break
                node = node.right
    return root


count = 0
checksum = 0


def undo(node, depth, level):
    global count, checksum
    if node is not None:
        if level == depth - 1:
            l = node.left
            r = node.right
            count += 2
            checksum = (checksum * 31 + l.val + r.val + 400000) % 1000000007
            node.left = l.left
            node.right = r.right
        else:
            undo(node.left, depth, level + 1)
            undo(node.right, depth, level + 1)


def main():
    trees = 20
    rounds = 4000
    all_trees = []
    for _ in range(trees):
        lean = 30 + next_random() % 41
        all_trees.append(random_tree(10000, lean))
    for r in range(rounds):
        depth = 2 + (r // trees) % 20
        root = add_one_row(all_trees[r % trees], r % 201 - 100, depth)
        undo(root, depth, 1)
    print(f"{trees} trees, {rounds} rounds: {count} row nodes, checksum {checksum}")


main()
