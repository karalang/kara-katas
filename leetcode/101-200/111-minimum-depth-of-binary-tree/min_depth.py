#!/usr/bin/env python3
"""LeetCode #111: Minimum Depth of Binary Tree — recursive DFS (mirror of min_depth.kara).

Shortest root-to-leaf node count. The one-child subtlety: an empty subtree offers no leaf, so
treat its depth (0) as "no path this way" and take the other side; otherwise take the smaller.
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


def min_depth(node):
    if node is None:
        return 0
    ld = min_depth(node.left)
    rd = min_depth(node.right)
    if ld == 0:
        return 1 + rd
    if rd == 0:
        return 1 + ld
    return 1 + (ld if ld < rd else rd)


def build_balanced(lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    node = TreeNode(mid)
    node.left = build_balanced(lo, mid - 1)
    node.right = build_balanced(mid + 1, hi)
    return node


def build_chain(length):
    root = None
    for i in range(length):
        root = insert(root, i)
    return root


def main():
    acc = 0
    for t in range(8):
        n = 7 + t
        root = build_balanced(0, n - 1) if t % 2 == 0 else build_chain(n)
        d = min_depth(root)
        acc = (acc * 131 + d + 1) % 1000000007
        print(f"tree {t}: min_depth {d}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
