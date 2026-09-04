"""LeetCode #314: Binary Tree Vertical Order Traversal — BFS with a column index.

Reference mirror of vertical_order.kara: a breadth-first walk tagging each node
with its column, appended to that column's list. BFS order IS the required
within-column order (top to bottom, then left to right), so no sorting is
needed; the columns are read out from the smallest key to the largest.
"""
from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def node(v, l=None, r=None):
    return TreeNode(v, l, r)


def leaf(v):
    return TreeNode(v)


def vertical_order(root):
    cols = {}
    q = deque()
    if root is not None:
        q.append((root, 0))
    while q:
        n, c = q.popleft()
        cols.setdefault(c, []).append(n.val)
        if n.left is not None:
            q.append((n.left, c - 1))
        if n.right is not None:
            q.append((n.right, c + 1))
    return [cols[k] for k in sorted(cols)]


def fmt(cols):
    return "[" + ",".join("[" + ",".join(str(v) for v in col) + "]" for col in cols) + "]"


def left_spine(n):
    if n <= 0:
        return None
    return node(-n, left_spine(n - 1), None)


def main():
    trees = [
        node(3, leaf(9), node(20, leaf(15), leaf(7))),
        node(3, node(9, leaf(4), leaf(0)), node(8, leaf(1), leaf(7))),
        node(3, node(9, leaf(4), node(0, None, leaf(2))),
             node(8, node(1, leaf(5), None), leaf(7))),
        node(1, node(2, None, node(4, None, leaf(6))), node(3, leaf(5), None)),
        None,
        leaf(7),
        left_spine(5),
        node(1, node(1, leaf(1), leaf(1)), node(1, leaf(1), leaf(1))),
    ]
    acc = 0
    for t, tree in enumerate(trees):
        cols = vertical_order(tree)
        for col in cols:
            acc = (acc * 131 + len(col)) % 1000000007
            for v in col:
                acc = (acc * 131 + v + 1000) % 1000000007
        print(f"tree {t}: {fmt(cols)}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
