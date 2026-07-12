"""LeetCode #99: Recover Binary Search Tree — inorder scan + value swap.

Mirror of recover.kara. Collect nodes inorder, find the (≤2) descents, swap the two
misplaced values back. Same tree-build, corruption, and fold as the Kāra version so
the files diff line-for-line.
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


def inorder_collect(node: Optional[TreeNode], out: list) -> None:
    if node is None:
        return
    inorder_collect(node.left, out)
    out.append(node)
    inorder_collect(node.right, out)


def corrupt(root: Optional[TreeNode], trial: int) -> Optional[TreeNode]:
    ns: list = []
    inorder_collect(root, ns)
    a = trial % len(ns)
    b = (trial * 3 + 2) % len(ns)
    if a != b:
        ns[a].val, ns[b].val = ns[b].val, ns[a].val
    return root


def recover(root: Optional[TreeNode]) -> Optional[TreeNode]:
    nodes: list = []
    inorder_collect(root, nodes)
    fi = si = -1
    for i in range(1, len(nodes)):
        if nodes[i - 1].val > nodes[i].val:
            if fi < 0:
                fi = i - 1
            si = i
    if fi >= 0:
        nodes[fi].val, nodes[si].val = nodes[si].val, nodes[fi].val
    return root


def serialize(node: Optional[TreeNode], out: list) -> None:
    if node is None:
        out.append("#,")
    else:
        out.append(f"{node.val},")
        serialize(node.left, out)
        serialize(node.right, out)


def main() -> None:
    vals = [5, 3, 8, 2, 4, 7, 9, 1, 6]
    acc = 0
    for trial in range(8):
        root: Optional[TreeNode] = None
        for k in range(len(vals)):
            idx = (k + trial) % len(vals)
            root = insert(root, vals[idx])
        root = corrupt(root, trial)
        root = recover(root)
        out: list = []
        serialize(root, out)
        s = "".join(out)
        for ch in s.encode():
            acc = (acc * 131 + ch) % 1000000007
        print(f"trial {trial}: {s}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
