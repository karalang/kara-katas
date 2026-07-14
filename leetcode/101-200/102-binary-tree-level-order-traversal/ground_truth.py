#!/usr/bin/env python3
"""Ground-truth cross-check for #102.

The DFS-with-depth level order (level_order.py) must equal an *independent* BFS
level order — a queue that dequeues a whole level at a time — on a battery of
hand cases and on thousands of randomised fuzz trees. Two genuinely different
mechanisms (recursive depth-indexed DFS vs iterative queue-per-level BFS) must
agree exactly, node-for-node, for every tree.
"""

import random
from collections import deque

from level_order import TreeNode, insert, build, level_order


def bfs_level_order(root):
    """Independent reference: classic BFS, one level per outer iteration."""
    if root is None:
        return []
    out = []
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
        out.append(row)
    return out


def build_from_shape(vals):
    """Build an explicit tree from a level-order-ish value list via BST insert."""
    return build(vals)


def check(root):
    a = level_order(root)
    b = bfs_level_order(root)
    return a == b


def main():
    random.seed(20260714)

    battery = [
        [],
        [1],
        [8, 4, 12, 2, 6, 10, 14],
        [1, 2, 3, 4, 5, 6, 7],           # right-leaning chain
        [7, 6, 5, 4, 3, 2, 1],           # left-leaning chain
        [5, 3, 8, 1, 4, 7, 9, 2, 6],
        [50, 30, 70, 20, 40, 60, 80],
    ]

    checked = 0
    for vals in battery:
        root = build(vals) if vals else None
        assert check(root), f"battery mismatch on {vals}"
        checked += 1

    # Fuzz: random-size trees of random distinct-ish values.
    FUZZ = 20000
    for _ in range(FUZZ):
        n = random.randint(0, 40)
        vals = [random.randint(-50, 50) for _ in range(n)]
        root = None
        for v in vals:
            root = insert(root, v)
        assert check(root), f"fuzz mismatch on {vals}"
        checked += 1

    print(f"ground truth OK: DFS-depth level order == BFS level order on {checked} trees "
          f"({len(battery)} battery + {FUZZ} fuzz)")


if __name__ == "__main__":
    main()
