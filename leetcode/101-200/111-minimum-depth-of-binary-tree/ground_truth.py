#!/usr/bin/env python3
"""Ground-truth cross-check for #111.

The recursive-DFS minimum depth (min_depth.py) must equal two *independent* references on a
case battery and 20,000 randomised trees, zero disagreements:

  1. BFS first-leaf (the second Kāra solver's mechanism): level-order the tree, return the
     depth of the first leaf dequeued.
  2. Brute-force shortest root-to-leaf path: enumerate every root-to-leaf path and take the
     minimum node count — the literal definition, testing the one-child subtlety directly.
"""

import random
import sys
from collections import deque

from min_depth import TreeNode, insert, min_depth, build_balanced, build_chain


def bfs_min_depth(root):
    if root is None:
        return 0
    depth = 0
    q = deque([root])
    while q:
        depth += 1
        for _ in range(len(q)):
            node = q.popleft()
            if node.left is None and node.right is None:
                return depth
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)
    return depth


def brute_min_depth(root):
    """Enumerate every root-to-leaf path; take the minimum node count (0 for empty tree)."""
    if root is None:
        return 0
    best = [10**9]
    stack = [(root, 1)]
    while stack:
        node, d = stack.pop()
        if node.left is None and node.right is None:
            best[0] = min(best[0], d)
        if node.left is not None:
            stack.append((node.left, d + 1))
        if node.right is not None:
            stack.append((node.right, d + 1))
    return best[0]


def check(root):
    d = min_depth(root)
    return d == bfs_min_depth(root) and d == brute_min_depth(root)


def random_tree(n, rng):
    root = None
    for _ in range(n):
        root = insert(root, rng.randint(-1000, 1000))
    return root


def main():
    sys.setrecursionlimit(100000)
    rng = random.Random(20260715)

    battery = [None]
    for n in (1, 2, 3, 7, 15, 31):
        battery.append(build_balanced(0, n - 1))
        battery.append(build_chain(n))

    checked = 0
    for root in battery:
        assert check(root), "battery mismatch"
        checked += 1

    FUZZ = 20000
    for _ in range(FUZZ):
        assert check(random_tree(rng.randint(0, 40), rng)), "fuzz mismatch"
        checked += 1

    print(f"ground truth OK: DFS == BFS-first-leaf == brute-force shortest path on {checked} "
          f"trees ({len(battery)} battery + {FUZZ} fuzz)")


if __name__ == "__main__":
    main()
