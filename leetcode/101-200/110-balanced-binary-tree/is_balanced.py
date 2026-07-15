#!/usr/bin/env python3
"""LeetCode #110: Balanced Binary Tree — bottom-up single pass (mirror of is_balanced.kara).

`check` returns a subtree's height, or the sentinel -1 the moment any subtree is unbalanced,
so -1 propagates straight up. `is_balanced` is then just `check(root) != -1`. O(n).
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


def check(node):
    if node is None:
        return 0
    lh = check(node.left)
    if lh == -1:
        return -1
    rh = check(node.right)
    if rh == -1:
        return -1
    if abs(lh - rh) > 1:
        return -1
    return 1 + (lh if lh > rh else rh)


def is_balanced(root):
    return check(root) != -1


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
        bal = is_balanced(root)
        acc = (acc * 131 + (1 if bal else 0) + 1) % 1000000007
        print(f"tree {t}: balanced={'true' if bal else 'false'}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
