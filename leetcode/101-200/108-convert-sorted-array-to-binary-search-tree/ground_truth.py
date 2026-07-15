#!/usr/bin/env python3
"""Ground-truth cross-check for #108.

A correct answer must satisfy the problem's two defining properties on every input, checked
independently of how the tree was built — on a case battery and 20,000 randomised sorted
arrays, zero violations:

  1. Valid BST recovering the input: an inorder walk of the built tree yields the original
     sorted array back (every value placed, in order).
  2. Height-balanced: at every node, |height(left) - height(right)| <= 1.

Plus a mechanism cross-check: the recursive middle-pick and an independent *iterative* stack
construction (the second Kāra solver's mechanism) build the byte-identical tree.
"""

import random

from sorted_to_bst import TreeNode, sorted_to_bst


def iter_build(arr):
    """Independent iterative reference (mirrors sorted_to_bst_iter.kara), same mid choice."""
    n = len(arr)
    if n == 0:
        return None
    root = TreeNode(0)
    stack = [(root, 0, n - 1)]
    while stack:
        node, lo, hi = stack.pop()
        mid = (lo + hi) // 2
        node.val = arr[mid]
        if lo <= mid - 1:
            node.left = TreeNode(0)
            stack.append((node.left, lo, mid - 1))
        if mid + 1 <= hi:
            node.right = TreeNode(0)
            stack.append((node.right, mid + 1, hi))
    return root


def inorder(node, out):
    if node is None:
        return
    inorder(node.left, out)
    out.append(node.val)
    inorder(node.right, out)


def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def is_balanced(node):
    if node is None:
        return True
    if abs(height(node.left) - height(node.right)) > 1:
        return False
    return is_balanced(node.left) and is_balanced(node.right)


def same_tree(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and same_tree(a.left, b.left) and same_tree(a.right, b.right)


def check(arr):
    root = sorted_to_bst(arr)
    out = []
    inorder(root, out)
    assert out == arr, f"inorder != sorted input: {out} != {arr}"
    assert is_balanced(root), f"not height-balanced on {arr}"
    assert same_tree(root, iter_build(arr)), f"recursive != iterative on {arr}"


def main():
    rng = random.Random(20260715)

    battery = [
        [1],
        [1, 2],
        [1, 2, 3],
        [-10, -3, 0, 5, 9],
        list(range(1, 16)),
        list(range(-7, 8)),
    ]

    checked = 0
    for arr in battery:
        check(arr)
        checked += 1

    FUZZ = 20000
    for _ in range(FUZZ):
        n = rng.randint(1, 80)   # >=1: an empty array yields the empty tree, trivially out of scope
        # a strictly-ascending array of distinct values
        arr = sorted(rng.sample(range(-10000, 10000), n))
        check(arr)
        checked += 1

    print(f"ground truth OK: inorder==sorted-input AND height-balanced AND recursive==iterative "
          f"on {checked} arrays ({len(battery)} battery + {FUZZ} fuzz)")


if __name__ == "__main__":
    main()
