"""LeetCode #101: Symmetric Tree — recursive mirror check.

Mirror of is_symmetric.kara. A tree is symmetric iff its two subtrees mirror: roots equal,
left.left mirrors right.right, left.right mirrors right.left. Same battery and fold as the
Kāra version so the files diff line-for-line.
"""

from __future__ import annotations

from typing import Optional


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val: int):
        self.val = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


def insert(root: Optional[TreeNode], v: int) -> TreeNode:
    if root is None:
        return TreeNode(v)
    if v < root.val:
        root.left = insert(root.left, v)
    else:
        root.right = insert(root.right, v)
    return root


def mirror(node: Optional[TreeNode]) -> Optional[TreeNode]:
    if node is None:
        return None
    m = TreeNode(node.val)
    m.left = mirror(node.right)
    m.right = mirror(node.left)
    return m


def is_mirror(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    if a is None:
        return b is None
    if b is None:
        return False
    return a.val == b.val and is_mirror(a.left, b.right) and is_mirror(a.right, b.left)


def is_symmetric(root: Optional[TreeNode]) -> bool:
    if root is None:
        return True
    return is_mirror(root.left, root.right)


def build(nums: list) -> Optional[TreeNode]:
    root: Optional[TreeNode] = None
    for v in nums:
        root = insert(root, v)
    return root


def main() -> None:
    base = [4, 2, 6, 1, 3, 5, 7]
    acc = 0
    for t in range(12):
        lv = [base[(k + t) % len(base)] for k in range(len(base))]
        sub = build(lv)
        if (t % 2) == 0:
            root = TreeNode(0)
            root.left = sub
            root.right = mirror(sub)
        else:
            root = TreeNode(0)
            root.left = sub
            root.right = sub
        sym = is_symmetric(root)
        acc = (acc * 131 + (1 if sym else 0) + 1) % 1000000007
        print(f"tree {t}: {str(sym).lower()}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
