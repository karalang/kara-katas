#!/usr/bin/env python3
"""LeetCode #114: Flatten Binary Tree to Linked List — iterative Morris rewiring (mirror of
flatten.kara).

Flatten the tree in place so each node's `right` is the next node in pre-order and `left` is None.
At each node with a left child, find the left subtree's rightmost node, splice the current right
subtree onto it, move the left subtree to `right`, null `left`, and advance.
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


def flatten(root):
    curr = root
    while curr is not None:
        if curr.left is not None:
            prev = curr.left
            while prev.right is not None:
                prev = prev.right
            prev.right = curr.right
            curr.right = curr.left
            curr.left = None
        curr = curr.right


def build_balanced(lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    node = TreeNode(mid)
    node.left = build_balanced(lo, mid - 1)
    node.right = build_balanced(mid + 1, hi)
    return node


def build_bst(seed, n):
    root = None
    s = seed
    for _ in range(n):
        s = (s * 1103515245 + 12345) % 2147483648
        root = insert(root, s % 200)
    return root


def spine_hash(root):
    h = 1
    cur = root
    while cur is not None:
        h = (h * 131 + cur.val + 1000) % 1000000007
        if cur.left is not None:
            h = (h + 999983) % 1000000007
        cur = cur.right
    return h


def main():
    acc = 0
    for t in range(8):
        if t % 2 == 0:
            root = build_balanced(t * 10, t * 10 + 6 + t)
        else:
            root = build_bst(t * 7919 + 1, 8 + t)
        flatten(root)
        h = spine_hash(root)
        acc = (acc * 131 + h) % 1000000007
        print(f"tree {t}: spine_hash={h}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
