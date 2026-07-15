#!/usr/bin/env python3
"""Ground-truth cross-check for #103.

The reconstruction is correct iff the rebuilt tree's own preorder and inorder traversals
reproduce the exact input arrays it was built from — the defining round-trip property. We
verify it two ways on a battery of hand cases and 20,000 randomised fuzz trees:

  1. Round-trip: preorder_of(build_tree(pre, ino)) == pre  AND  inorder_of(...) == ino.
  2. Structural identity: the rebuilt tree is byte-identical (shape + values) to the
     original tree the (pre, ino) pair was read off — an independent second check that the
     reconstruction recovers the *same* tree, not merely some tree with matching traversals.

Node values are distinct within each tree (the problem's guarantee), which is what makes
the (preorder, inorder) pair determine a unique tree.
"""

import random
import sys

from build_tree import (
    TreeNode, build_tree, preorder_of, inorder_of, insert_all, bst_insert,
)


def same_tree(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and same_tree(a.left, b.left) and same_tree(a.right, b.right)


def check_tree(orig):
    pre, ino = [], []
    preorder_of(orig, pre)
    inorder_of(orig, ino)
    rebuilt = build_tree(pre, ino)
    # 1. round-trip
    rpre, rino = [], []
    preorder_of(rebuilt, rpre)
    inorder_of(rebuilt, rino)
    assert rpre == pre, f"preorder round-trip failed: {rpre} != {pre}"
    assert rino == ino, f"inorder round-trip failed: {rino} != {ino}"
    # 2. structural identity to the original
    assert same_tree(rebuilt, orig), "rebuilt tree differs from original"


def build_random_distinct_tree(n, rng):
    # Insert a random permutation of n distinct values into a BST → distinct-value tree.
    vals = rng.sample(range(-1000, 1001), n)
    root = None
    for v in vals:
        root = bst_insert(root, v)
    return root


def main():
    sys.setrecursionlimit(10000)
    rng = random.Random(20260715)

    battery = [
        [8, 4, 12, 2, 6, 10, 14],
        [1, 2, 3, 4, 5],          # right chain
        [5, 4, 3, 2, 1],          # left chain
        [50, 30, 70, 20, 40, 60, 80, 10],
        [42],
    ]

    checked = 0
    for vals in battery:
        check_tree(insert_all(vals))
        checked += 1

    FUZZ = 20000
    for _ in range(FUZZ):
        n = rng.randint(1, 60)   # >=1: an empty tree has no preorder root, out of kata scope
        check_tree(build_random_distinct_tree(n, rng))
        checked += 1

    print(f"ground truth OK: preorder+inorder round-trip AND structural identity on "
          f"{checked} trees ({len(battery)} battery + {FUZZ} fuzz)")


if __name__ == "__main__":
    main()
