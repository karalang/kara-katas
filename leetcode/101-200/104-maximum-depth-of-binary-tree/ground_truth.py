#!/usr/bin/env python3
"""Ground-truth cross-check for #104 (maximum depth).

The recursive DFS depth (max_depth.py) must equal two *independent* references on a case
battery and 20,000 randomised fuzz trees, zero mismatches:

  1. BFS level count — a queue that dequeues a whole level per iteration; the number of
     levels seen is the depth (the second Kāra solver's mechanism).
  2. Longest explicit root-to-leaf path — enumerate every root-to-leaf path and take the
     max node count. A wholly different computation (path enumeration vs a recurrence /
     level queue) that must agree exactly.
"""

import random
import sys
from collections import deque

from max_depth import TreeNode, insert, max_depth


def bfs_depth(root):
    if root is None:
        return 0
    depth = 0
    q = deque([root])
    while q:
        depth += 1
        for _ in range(len(q)):
            node = q.popleft()
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)
    return depth


def longest_path(root):
    """Max node count over all root-to-leaf paths (independent of both solvers)."""
    if root is None:
        return 0
    best = 0
    stack = [(root, 1)]
    while stack:
        node, d = stack.pop()
        if node.left is None and node.right is None:
            best = max(best, d)
        if node.left is not None:
            stack.append((node.left, d + 1))
        if node.right is not None:
            stack.append((node.right, d + 1))
    return best


def check(root):
    d = max_depth(root)
    return d == bfs_depth(root) and d == longest_path(root)


def main():
    sys.setrecursionlimit(10000)
    rng = random.Random(20260715)

    battery = [
        [],
        [1],
        [8, 4, 12, 2, 6, 10, 14],
        [1, 2, 3, 4, 5, 6, 7],      # right chain -> depth 7
        [7, 6, 5, 4, 3, 2, 1],      # left chain -> depth 7
        [5, 3, 8, 1, 4, 7, 9, 2, 6],
    ]

    checked = 0
    for vals in battery:
        root = None
        for v in vals:
            root = insert(root, v)
        assert check(root), f"battery mismatch on {vals}"
        checked += 1

    FUZZ = 20000
    for _ in range(FUZZ):
        n = rng.randint(0, 60)
        root = None
        for _ in range(n):
            root = insert(root, rng.randint(-100, 100))
        assert check(root), "fuzz mismatch"
        checked += 1

    print(f"ground truth OK: DFS depth == BFS level count == longest root-to-leaf path on "
          f"{checked} trees ({len(battery)} battery + {FUZZ} fuzz)")


if __name__ == "__main__":
    main()
