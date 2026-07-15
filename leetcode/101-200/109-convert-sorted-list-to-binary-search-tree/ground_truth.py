#!/usr/bin/env python3
"""Ground-truth cross-check for #109.

A correct answer must satisfy the problem's two defining properties on every input, checked
independently of how the tree was built — on a case battery and 20,000 randomised sorted
lists, zero violations:

  1. Valid BST recovering the input: an inorder walk of the built tree yields the list's
     values back in order.
  2. Height-balanced: at every node, |height(left) - height(right)| <= 1.

Plus a mechanism cross-check: the array-conversion build and an independent *inorder-
simulation* build (the second Kāra solver's mechanism, threading a list cursor) produce the
byte-identical tree.
"""

import random

from sorted_list_to_bst import ListNode, TreeNode, sorted_list_to_bst


def list_of(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def inorder_sim_build(head):
    """Independent inorder-simulation reference (mirrors sorted_list_to_bst_inorder.kara)."""
    def count(node):
        n = 0
        while node is not None:
            n += 1
            node = node.next
        return n

    cur = [head]  # boxed cursor

    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        left = build(lo, mid - 1)
        node = TreeNode(cur[0].val)
        cur[0] = cur[0].next
        node.left = left
        node.right = build(mid + 1, hi)
        return node

    return build(0, count(head) - 1)


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


def check(vals):
    root = sorted_list_to_bst(list_of(vals))
    out = []
    inorder(root, out)
    assert out == vals, f"inorder != list values: {out} != {vals}"
    assert is_balanced(root), f"not height-balanced on {vals}"
    assert same_tree(root, inorder_sim_build(list_of(vals))), f"array != inorder-sim on {vals}"


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
    for vals in battery:
        check(vals)
        checked += 1

    FUZZ = 20000
    for _ in range(FUZZ):
        n = rng.randint(1, 80)   # >=1: an empty list yields the empty tree, trivially out of scope
        vals = sorted(rng.sample(range(-10000, 10000), n))
        check(vals)
        checked += 1

    print(f"ground truth OK: inorder==list-values AND height-balanced AND array==inorder-sim "
          f"on {checked} lists ({len(battery)} battery + {FUZZ} fuzz)")


if __name__ == "__main__":
    main()
