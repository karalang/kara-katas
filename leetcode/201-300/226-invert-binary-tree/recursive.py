"""LeetCode #226: Invert Binary Tree — recursive DFS.

Algorithmic mirror of recursive.kara. Output is the level-order traversal of
the inverted tree, one value per line, with None children skipped. Matches
recursive.kara line-for-line on the same inputs.
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
    new_left = invert(root.right)
    new_right = invert(root.left)
    root.left = new_left
    root.right = new_right
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
    # Case 1: [4,2,7,1,3,6,9] -> inverted [4,7,2,9,6,3,1]
    tree1 = TreeNode(
        4,
        TreeNode(2, TreeNode(1), TreeNode(3)),
        TreeNode(7, TreeNode(6), TreeNode(9)),
    )
    report(tree1)

    # Case 2: [2,1,3] -> [2,3,1]
    tree2 = TreeNode(2, TreeNode(1), TreeNode(3))
    report(tree2)

    # Case 3: empty tree -> nothing printed
    report(None)


if __name__ == "__main__":
    main()
