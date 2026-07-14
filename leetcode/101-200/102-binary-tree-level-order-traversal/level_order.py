#!/usr/bin/env python3
"""LeetCode #102: Binary Tree Level Order Traversal — DFS carrying the depth (mirror of level_order.kara).

Group node values by depth. A single DFS suffices if each node knows its depth: keep one
output row per depth, and when a node at depth d is visited, append its value to row d
(creating that row the first time depth d is reached). DFS visits a node before either
child and the left child before the right, so each row fills strictly left to right.
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


def dfs(node, depth, result):
    if node is None:
        return
    if depth == len(result):
        result.append([])
    result[depth].append(node.val)
    dfs(node.left, depth + 1, result)
    dfs(node.right, depth + 1, result)


def level_order(root):
    result = []
    dfs(root, 0, result)
    return result


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
        levels = level_order(root)
        acc = (acc * 131 + len(levels)) % 1000000007
        for lvl in levels:
            acc = (acc * 131 + len(lvl)) % 1000000007
            for v in lvl:
                acc = (acc * 131 + v) % 1000000007
        print(f"tree {t}: {len(levels)} levels")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
