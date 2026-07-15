#!/usr/bin/env python3
"""Ground-truth cross-check for #110.

The bottom-up single-pass verdict (is_balanced.py) must equal two *independent* references on
a case battery and 20,000 randomised trees, zero disagreements:

  1. Top-down height-recompute (the second Kāra solver's mechanism): balanced iff every node's
     two subtree heights differ by <= 1 and both subtrees are balanced.
  2. Brute-force definition: compute height() at *every* node from scratch and require
     |height(left) - height(right)| <= 1 at all of them.
"""

import random
import sys

from is_balanced import TreeNode, insert, is_balanced, build_balanced, build_chain


def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def topdown_balanced(node):
    if node is None:
        return True
    if abs(height(node.left) - height(node.right)) > 1:
        return False
    return topdown_balanced(node.left) and topdown_balanced(node.right)


def brute_balanced(node):
    """Independent: every node must satisfy the height difference constraint."""
    ok = True
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur is None:
            continue
        if abs(height(cur.left) - height(cur.right)) > 1:
            ok = False
        stack.append(cur.left)
        stack.append(cur.right)
    return ok


def check(root):
    v = is_balanced(root)
    return v == topdown_balanced(root) and v == brute_balanced(root)


def random_tree(n, rng):
    """A random-shaped tree of n nodes (random BST-insert order gives varied balance)."""
    root = None
    for _ in range(n):
        root = insert(root, rng.randint(-1000, 1000))
    return root


def main():
    sys.setrecursionlimit(100000)
    rng = random.Random(20260715)

    battery = [None]
    for n in (1, 2, 3, 7, 15, 31):
        battery.append(build_balanced(0, n - 1))   # balanced
        battery.append(build_chain(n))             # skewed

    checked = 0
    for root in battery:
        assert check(root), "battery mismatch"
        checked += 1

    FUZZ = 20000
    for _ in range(FUZZ):
        assert check(random_tree(rng.randint(0, 40), rng)), "fuzz mismatch"
        checked += 1

    print(f"ground truth OK: bottom-up == top-down == brute-force on {checked} trees "
          f"({len(battery)} battery + {FUZZ} fuzz)")


if __name__ == "__main__":
    main()
