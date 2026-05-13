"""LeetCode #226: Invert Binary Tree — iterative BFS.

Algorithmic mirror of iterative.kara. Walks the tree level-order via a queue,
swapping each visited node's children in place. Output matches recursive.py
and the two .kara siblings line-for-line.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def invert(root: TreeNode | None) -> TreeNode | None:
    if root is None:
        return None
    queue: deque[TreeNode] = deque([root])
    while queue:
        current = queue.popleft()
        current.left, current.right = current.right, current.left
        if current.left is not None:
            queue.append(current.left)
        if current.right is not None:
            queue.append(current.right)
    return root


def report(root: TreeNode | None) -> None:
    inverted = invert(root)
    if inverted is None:
        return
    queue: deque[TreeNode] = deque([inverted])
    while queue:
        current = queue.popleft()
        print(current.val)
        if current.left is not None:
            queue.append(current.left)
        if current.right is not None:
            queue.append(current.right)


def main() -> None:
    tree1 = TreeNode(
        4,
        TreeNode(2, TreeNode(1), TreeNode(3)),
        TreeNode(7, TreeNode(6), TreeNode(9)),
    )
    report(tree1)

    tree2 = TreeNode(2, TreeNode(1), TreeNode(3))
    report(tree2)

    report(None)


if __name__ == "__main__":
    main()
