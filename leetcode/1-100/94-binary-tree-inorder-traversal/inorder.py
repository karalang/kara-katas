"""LeetCode #94: Binary Tree Inorder Traversal — recursive DFS.

Mirror of inorder.kara. Visit left subtree, then node, then right subtree, appending
each value to a threaded list. Same nine trees and output shape (each traversal as a
bracketed space-separated list, then a `sink:` fold) so the files diff line-for-line.
"""

from __future__ import annotations

from typing import Optional


class TreeNode:
    def __init__(self, val: int, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def inorder(node: Optional[TreeNode], out: list[int]) -> None:
    if node is None:
        return
    inorder(node.left, out)
    out.append(node.val)
    inorder(node.right, out)


def traverse(root: Optional[TreeNode]) -> list[int]:
    out: list[int] = []
    inorder(root, out)
    return out


def leaf(v: int) -> TreeNode:
    return TreeNode(v)


def report(root: Optional[TreeNode], acc: list[int]) -> None:
    vals = traverse(root)
    n = len(vals)
    print("[" + " ".join(str(v) for v in vals) + "]")
    a = (acc[0] * 131 + (n + 1)) % 1000000007
    for v in vals:
        a = (a * 131 + (v + 1000)) % 1000000007
    acc[0] = a


def main() -> None:
    acc = [0]

    report(None, acc)                                              # []
    report(leaf(1), acc)                                           # [1]

    # LeetCode example: [1,null,2,3].
    report(TreeNode(1, None, TreeNode(2, leaf(3), None)), acc)     # [1 3 2]

    # Balanced [2,1,3].
    report(TreeNode(2, leaf(1), leaf(3)), acc)                     # [1 2 3]

    # Full 7-node BST [4,2,6,1,3,5,7].
    report(TreeNode(4, TreeNode(2, leaf(1), leaf(3)),
                    TreeNode(6, leaf(5), leaf(7))), acc)           # [1 2 3 4 5 6 7]

    # Left-skewed chain 4->3->2->1.
    report(TreeNode(4, TreeNode(3, TreeNode(2, leaf(1), None), None), None), acc)  # [1 2 3 4]

    # Right-skewed chain 1->2->3->4.
    report(TreeNode(1, None, TreeNode(2, None, TreeNode(3, None, leaf(4)))), acc)  # [1 2 3 4]

    # Negative values.
    report(TreeNode(0, TreeNode(-3, leaf(-10), leaf(-1)),
                    TreeNode(9, leaf(5), None)), acc)              # [-10 -3 -1 0 5 9]

    # Irregular.
    report(TreeNode(5, TreeNode(3, leaf(2), TreeNode(4, None, None)), leaf(8)), acc)  # [2 3 4 5 8]

    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()
