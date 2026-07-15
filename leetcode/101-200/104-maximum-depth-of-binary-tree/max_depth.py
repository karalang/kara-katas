#!/usr/bin/env python3
"""LeetCode #104: Maximum Depth of Binary Tree — recursive DFS (mirror of max_depth.kara).

An empty tree has depth 0; a non-empty node's depth is 1 plus the deeper of its two subtrees.
"""


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def insert(root, v):
    if root is None:
        return TreeNode(v)
    if v < root.val:
        root.left = insert(root.left, v)
    else:
        root.right = insert(root.right, v)
    return root


def max_depth(node):
    if node is None:
        return 0
    lh = max_depth(node.left)
    rh = max_depth(node.right)
    return 1 + (lh if lh > rh else rh)


def build(nums):
    root = None
    for x in nums:
        root = insert(root, x)
    return root


def main():
    base = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7]
    acc = 0
    for t in range(8):
        nums = [base[(k + t) % len(base)] for k in range(len(base))]
        root = build(nums)
        d = max_depth(root)
        acc = (acc * 131 + d) % 1000000007
        print(f"tree {t}: depth {d}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
