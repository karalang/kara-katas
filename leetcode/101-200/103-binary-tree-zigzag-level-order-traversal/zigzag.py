#!/usr/bin/env python3
"""LeetCode #103: Binary Tree Zigzag Level Order Traversal — DFS carrying the depth,
then reverse the odd rows (mirror of zigzag.kara).

Zigzag level order is ordinary level order with alternating direction: row 0 left-to-right,
row 1 right-to-left, and so on. Collect the levels with a single depth-indexed DFS (each row
fills left-to-right), then emit each row, reversing every odd-indexed one.
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


def zigzag(root):
    rows = []
    dfs(root, 0, rows)
    out = []
    for d in range(len(rows)):
        if d % 2 == 0:
            out.append(list(rows[d]))
        else:
            out.append(list(reversed(rows[d])))
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
        levels = zigzag(root)
        acc = (acc * 131 + len(levels)) % 1000000007
        for lvl in levels:
            acc = (acc * 131 + len(lvl)) % 1000000007
            for v in lvl:
                acc = (acc * 131 + v) % 1000000007
        print(f"tree {t}: {len(levels)} levels")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
