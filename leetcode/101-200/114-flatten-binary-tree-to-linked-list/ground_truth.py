#!/usr/bin/env python3
"""Ground-truth cross-check for #114.

The iterative Morris flatten (flatten.py) must agree with two *independent* references on a battery
and 20,000 randomised trees, zero disagreements:

  1. The recursive tail-return flatten (the second Kāra solver's mechanism).
  2. The literal definition: a flattened tree's right-spine values must equal the ORIGINAL tree's
     PRE-ORDER traversal, and every `left` must be null.

Each check flattens a *fresh copy* (flatten mutates in place), then compares the resulting spine —
values AND the all-left-null invariant — three ways.
"""

import random
import sys

from flatten import TreeNode, insert, flatten, build_balanced, build_bst


def preorder(node):
    if node is None:
        return []
    return [node.val] + preorder(node.left) + preorder(node.right)


def clone(node):
    if node is None:
        return None
    n = TreeNode(node.val)
    n.left = clone(node.left)
    n.right = clone(node.right)
    return n


def flatten_recursive(node):
    """Recursive tail-return flatten (mirrors flatten_recursive.kara)."""

    def tail(n):
        if n is None:
            return None
        lt = tail(n.left)
        rt = tail(n.right)
        if lt is not None:
            lt.right = n.right
            n.right = n.left
            n.left = None
        if rt is not None:
            return rt
        if lt is not None:
            return lt
        return n

    tail(node)


def spine(node):
    """(values, all_left_null) walking the right chain after a flatten."""
    vals = []
    ok = True
    cur = node
    while cur is not None:
        vals.append(cur.val)
        if cur.left is not None:
            ok = False
        cur = cur.right
    return vals, ok


def check(root):
    want = preorder(root)  # the invariant: flattened spine == original pre-order

    a = clone(root)
    flatten(a)
    va, oka = spine(a)

    b = clone(root)
    flatten_recursive(b)
    vb, okb = spine(b)

    return va == want and oka and vb == want and okb


def random_tree(n, rng):
    root = None
    for _ in range(n):
        root = insert(root, rng.randint(-50, 50))
    return root


def main():
    sys.setrecursionlimit(100000)
    rng = random.Random(20260716)

    checked = 0
    # Battery: empty, singletons, balanced ranges, deterministic BSTs.
    assert check(None)
    checked += 1
    for n in (1, 2, 3, 7, 15, 31):
        assert check(build_balanced(0, n - 1)), f"battery balanced n={n}"
        checked += 1
    for seed in (1, 12345, 99991):
        assert check(build_bst(seed, 20)), f"battery bst seed={seed}"
        checked += 1

    FUZZ = 20000
    for _ in range(FUZZ):
        root = random_tree(rng.randint(0, 40), rng)
        assert check(root), "fuzz mismatch"
        checked += 1

    print(
        f"ground truth OK: Morris flatten == recursive flatten == original pre-order "
        f"(all lefts null) on {checked} trees (battery + {FUZZ} fuzz)"
    )


if __name__ == "__main__":
    main()
