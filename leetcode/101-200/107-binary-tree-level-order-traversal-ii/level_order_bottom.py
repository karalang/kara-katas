#!/usr/bin/env python3
"""LeetCode #107: Binary Tree Level Order Traversal II — DFS carrying the depth, then reverse
the row order (mirror of level_order_bottom.kara).

Bottom-up level order is ordinary level order with the rows emitted deepest-first (values
within each row still read left-to-right). Collect the levels with a depth-indexed DFS, then
emit the rows in reverse depth order.
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


def dfs(node, depth, rows):
    if node is None:
        return
    if depth == len(rows):
        rows.append([])
    rows[depth].append(node.val)
    dfs(node.left, depth + 1, rows)
    dfs(node.right, depth + 1, rows)


def level_order_bottom(root):
    rows = []
    dfs(root, 0, rows)
    out = []
    for d in range(len(rows) - 1, -1, -1):
        out.append(list(rows[d]))
    return out


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
        levels = level_order_bottom(root)
        acc = (acc * 131 + len(levels)) % 1000000007
        for lvl in levels:
            acc = (acc * 131 + len(lvl)) % 1000000007
            for v in lvl:
                acc = (acc * 131 + v) % 1000000007
        print(f"tree {t}: {len(levels)} levels")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
