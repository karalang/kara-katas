#!/usr/bin/env python3
"""Ground-truth cross-check for #103 (zigzag level order).

The zigzag traversal (zigzag.py, depth-indexed DFS + reverse odd rows) must equal an
*independent* reference built from a plain BFS: dequeue whole levels with a queue, then
reverse every odd-indexed level. Two genuinely different mechanisms (recursive depth-indexed
DFS vs iterative queue-per-level BFS, each reversing odd rows) must agree exactly, level for
level, on a case battery and 20,000 randomised fuzz trees.
"""

import random
from collections import deque

from zigzag import TreeNode, insert, build, zigzag


def bfs_zigzag(root):
    """Independent reference: classic BFS level order, then reverse odd levels."""
    if root is None:
        return []
    out = []
    q = deque([root])
    depth = 0
    while q:
        row = []
        for _ in range(len(q)):
            node = q.popleft()
            row.append(node.val)
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)
        if depth % 2 == 1:
            row.reverse()
        out.append(row)
        depth += 1
    return out


def check(root):
    return zigzag(root) == bfs_zigzag(root)


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

    print(f"ground truth OK: DFS-depth zigzag == BFS-then-reverse-odd zigzag on {checked} "
          f"trees ({len(battery)} battery + {FUZZ} fuzz)")


if __name__ == "__main__":
    main()
