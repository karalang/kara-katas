"""LeetCode #100: Same Tree — recursive structural comparison.

Mirror of same_tree.kara. Two trees match iff both empty, or both non-empty with equal
root values and matching left and right subtrees. Same battery and fold as the Kāra
version so the files diff line-for-line.
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


def is_same(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    if p is None:
        return q is None
    if q is None:
        return False
    return p.val == q.val and is_same(p.left, q.left) and is_same(p.right, q.right)


def build(nums: list) -> Optional[TreeNode]:
    root: Optional[TreeNode] = None
    for v in nums:
        root = insert(root, v)
    return root


def main() -> None:
    bases = [
        [5, 3, 8, 1, 4, 7, 9],
        [2, 1, 3, 0, 0, 0, 0],
        [10, 5, 15, 3, 7, 12, 20],
        [1, 2, 3, 4, 5, 6, 7],
    ]
    acc = 0
    for t in range(12):
        base = bases[t % len(bases)]
        pseq: list = []
        qseq: list = []
        for k in range(len(base)):
            pseq.append(base[k])
            bump = (t % 3) if k == (t % 7) else 0
            qseq.append(base[k] + bump)
        p = build(pseq)
        q = build(qseq)
        same = is_same(p, q)
        acc = (acc * 131 + (1 if same else 0) + 1) % 1000000007
        print(f"pair {t}: {str(same).lower()}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
