#!/usr/bin/env python3
"""Ground-truth cross-check for #113.

The backtracking DFS (path_sum_ii.py) must equal two *independent* references — same list of
paths, same order — on a battery and 20,000 randomised (tree, target) pairs, zero disagreements:

  1. Return-based collect (the second Kāra solver's mechanism): each subtree returns its qualifying
     paths with the node prepended.
  2. Brute-force: enumerate EVERY root-to-leaf path, keep those summing to target. The literal
     definition — exercises the leaf-only rule (an internal node hitting the remainder must not
     count) and the left-to-right ordering.
"""

import random
import sys

from path_sum_ii import (
    TreeNode,
    path_sum,
    build_perfect,
    build_balanced,
    leftmost_path_sum,
)


def collect(node, target):
    """Return-based reference (mirrors path_sum_ii_return.kara)."""
    res = []
    if node is None:
        return res
    rem = target - node.val
    if node.left is None and node.right is None:
        if rem == 0:
            res.append([node.val])
    else:
        for sp in collect(node.left, rem):
            res.append([node.val] + sp)
        for sp in collect(node.right, rem):
            res.append([node.val] + sp)
    return res


def all_root_to_leaf(node):
    """Every root-to-leaf path (values), left-to-right DFS order."""
    if node is None:
        return []
    if node.left is None and node.right is None:
        return [[node.val]]
    out = []
    for sp in all_root_to_leaf(node.left):
        out.append([node.val] + sp)
    for sp in all_root_to_leaf(node.right):
        out.append([node.val] + sp)
    return out


def brute(node, target):
    return [p for p in all_root_to_leaf(node) if sum(p) == target]


def insert(root, v):
    if root is None:
        return TreeNode(v)
    if v < root.val:
        root.left = insert(root.left, v)
    else:
        root.right = insert(root.right, v)
    return root


def random_tree(n, rng):
    root = None
    for _ in range(n):
        root = insert(root, rng.randint(-8, 8))
    return root


def check(root, target):
    a = path_sum(root, target)
    return a == collect(root, target) and a == brute(root, target)


def main():
    sys.setrecursionlimit(100000)
    rng = random.Random(20260716)

    checked = 0
    # Battery: perfect uniform trees (multiplicity) + balanced distinct trees.
    for depth in (1, 2, 3, 4):
        for val in (-2, 0, 3):
            root = build_perfect(depth, val)
            for tgt in {depth * val, depth * val + 1, depth * val - 1, 0}:
                assert check(root, tgt), f"battery perfect depth={depth} val={val} tgt={tgt}"
                checked += 1
    for n in (1, 3, 7, 15):
        root = build_balanced(0, n - 1)
        for tgt in {leftmost_path_sum(root), 0, 10**9}:
            assert check(root, tgt), f"battery balanced n={n} tgt={tgt}"
            checked += 1

    FUZZ = 20000
    for _ in range(FUZZ):
        root = random_tree(rng.randint(0, 20), rng)
        paths = all_root_to_leaf(root)
        # Mix achievable targets (a real path sum) with random ones.
        if paths and rng.random() < 0.6:
            tgt = sum(rng.choice(paths))
        else:
            tgt = rng.randint(-30, 30)
        assert check(root, tgt), f"fuzz mismatch tgt={tgt}"
        checked += 1

    print(
        f"ground truth OK: backtracking == return-based == brute-force on {checked} "
        f"(tree,target) pairs (battery + {FUZZ} fuzz)"
    )


if __name__ == "__main__":
    main()
