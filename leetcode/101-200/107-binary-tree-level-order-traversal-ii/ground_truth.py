#!/usr/bin/env python3
"""Ground-truth cross-check for #107 (bottom-up level order).

The DFS-with-depth bottom-up traversal (level_order_bottom.py) must equal an *independent*
reference built from a plain BFS: a queue that dequeues a whole level per iteration to build
top-down rows, reversed. Two genuinely different mechanisms (recursive depth-indexed DFS +
row reverse vs iterative queue-per-level BFS + row reverse) must agree exactly, level for
level, on a case battery and 20,000 randomised fuzz trees.
"""

import random
from collections import deque

from level_order_bottom import TreeNode, insert, build, level_order_bottom


def bfs_bottom(root):
    """Independent reference: classic BFS top-down, then reverse the row order."""
    if root is None:
        return []
    rows = []
    q = deque([root])
    while q:
        row = []
        for _ in range(len(q)):
            node = q.popleft()
            row.append(node.val)
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)
        rows.append(row)
    rows.reverse()
    return rows


def check(root):
    return level_order_bottom(root) == bfs_bottom(root)


def main():
    random.seed(20260715)

    battery = [
        [],
        [1],
        [8, 4, 12, 2, 6, 10, 14],
        [1, 2, 3, 4, 5, 6, 7],      # right-leaning chain
        [7, 6, 5, 4, 3, 2, 1],      # left-leaning chain
        [5, 3, 8, 1, 4, 7, 9, 2, 6],
        [50, 30, 70, 20, 40, 60, 80],
    ]

    checked = 0
    for vals in battery:
        root = build(vals) if vals else None
        assert check(root), f"battery mismatch on {vals}"
        checked += 1

    FUZZ = 20000
    for _ in range(FUZZ):
        n = random.randint(0, 40)
        root = None
        for _ in range(n):
            root = insert(root, random.randint(-50, 50))
        assert check(root), "fuzz mismatch"
        checked += 1

    print(f"ground truth OK: DFS-depth bottom-up == BFS-then-reverse bottom-up on {checked} "
          f"trees ({len(battery)} battery + {FUZZ} fuzz)")


if __name__ == "__main__":
    main()
