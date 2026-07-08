"""LeetCode #98: Validate Binary Search Tree — recursive (min, max) bounds.

Mirror of validate_bst.kara: a node is valid iff its value lies strictly inside
the open interval (lo, hi) inherited from its ancestors; the left child tightens
the upper bound to the node value, the right child tightens the lower bound.
`None` bounds mean "unbounded on that side" (the root starts unbounded), avoiding
any sentinel a node could equal. Same ten trees and the same output shape (one
`valid=…` per tree, then a `sums:` fold of 1/0) so the files diff line-for-line.
(The inorder variant lives only in Kāra; this mirror tracks the ★.)
"""

from __future__ import annotations

from typing import Optional


class TreeNode:
    def __init__(self, val: int, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def is_valid(node: Optional[TreeNode], lo: Optional[int], hi: Optional[int]) -> bool:
    if node is None:
        return True
    if lo is not None and node.val <= lo:
        return False
    if hi is not None and node.val >= hi:
        return False
    return is_valid(node.left, lo, node.val) and is_valid(node.right, node.val, hi)


def report(root: Optional[TreeNode], acc: list[str]) -> None:
    ok = is_valid(root, None, None)
    print("valid=true" if ok else "valid=false")
    acc.append("1" if ok else "0")


def leaf(v: int) -> TreeNode:
    return TreeNode(v)


def main() -> None:
    acc: list[str] = []
    report(None, acc)
    report(leaf(1), acc)
    report(TreeNode(2, leaf(1), leaf(3)), acc)
    report(TreeNode(5, leaf(1), TreeNode(4, leaf(3), leaf(6))), acc)
    report(TreeNode(1, leaf(1), None), acc)
    report(TreeNode(5, leaf(4), TreeNode(6, leaf(3), leaf(7))), acc)
    report(TreeNode(8, TreeNode(4, leaf(2), leaf(6)), TreeNode(12, leaf(10), leaf(14))), acc)
    report(TreeNode(5, TreeNode(4, TreeNode(3, TreeNode(2, leaf(1), None), None), None), None), acc)
    report(TreeNode(1, None, TreeNode(2, None, TreeNode(3, None, leaf(4)))), acc)
    report(TreeNode(2, leaf(1), leaf(2)), acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()
