#!/usr/bin/env python3
"""Ground-truth cross-check for #112.

The recursive DFS verdict (path_sum.py) must equal two *independent* references on a case
battery and 20,000 randomised (tree, target) pairs, zero disagreements:

  1. Iterative (node, remaining) stack (the second Kāra solver's mechanism).
  2. Brute-force set membership: enumerate the sums of *every* root-to-leaf path and test
     whether target is among them — the literal definition, exercising the leaf-only rule
     (an internal node hitting the remainder must NOT count).
"""

import random
import sys

from path_sum import TreeNode, insert, has_path_sum, build_balanced, leftmost_path_sum


def iter_has_path_sum(root, target):
    """Independent iterative reference (mirrors path_sum_iter.kara)."""
    stack = []
    if root is not None:
        stack.append((root, target))
    while stack:
        node, rem = stack.pop()
        r = rem - node.val
        if node.left is None and node.right is None:
            if r == 0:
                return True
        else:
            if node.left is not None:
                stack.append((node.left, r))
            if node.right is not None:
                stack.append((node.right, r))
    return False


def all_path_sums(root):
    """Every root-to-leaf path sum (empty tree -> no paths)."""
    sums = []
    if root is None:
        return sums
    stack = [(root, root.val)]
    while stack:
        node, s = stack.pop()
        if node.left is None and node.right is None:
            sums.append(s)
        if node.left is not None:
            stack.append((node.left, s + node.left.val))
        if node.right is not None:
            stack.append((node.right, s + node.right.val))
    return sums


def check(root, target):
    v = has_path_sum(root, target)
    brute = target in set(all_path_sums(root))
    return v == iter_has_path_sum(root, target) and v == brute


def random_tree(n, rng):
    root = None
    for _ in range(n):
        root = insert(root, rng.randint(-20, 20))
    return root


def main():
    sys.setrecursionlimit(100000)
    rng = random.Random(20260715)

    checked = 0
    # Battery: known trees, targets both achievable and not.
    for n in (1, 2, 3, 7, 15):
        root = build_balanced(0, n - 1)
        sums = all_path_sums(root)
        for tgt in set(sums) | {min(sums) - 1, max(sums) + 1, 0, 10**9}:
            assert check(root, tgt), f"battery mismatch n={n} tgt={tgt}"
            checked += 1

    FUZZ = 20000
    for _ in range(FUZZ):
        root = random_tree(rng.randint(0, 30), rng)
        sums = all_path_sums(root)
        # Mix achievable targets (a real path sum) with random ones.
        if sums and rng.random() < 0.5:
            tgt = rng.choice(sums)
        else:
            tgt = rng.randint(-60, 60)
        assert check(root, tgt), f"fuzz mismatch tgt={tgt}"
        checked += 1

    print(f"ground truth OK: DFS == iterative == brute-force set-membership on {checked} "
          f"(tree,target) pairs (battery + {FUZZ} fuzz)")


if __name__ == "__main__":
    main()
