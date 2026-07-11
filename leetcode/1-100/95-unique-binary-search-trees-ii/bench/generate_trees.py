"""LeetCode #95: Unique Binary Search Trees II — recursive divide & conquer.

Mirror of generate_trees.kara. For each root value i in [lo, hi], take the cross product
of all left subtrees (lo..i-1) and all right subtrees (i+1..hi). Same build order, same
canonical preorder serialization ('#,' for null, 'val,' for a node) and same fold (count,
each tree's serialized bytes, a '7' separator) so the files diff line-for-line.
"""

from __future__ import annotations

from typing import Optional


class TreeNode:
    def __init__(self, val: int, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def build_all(lo: int, hi: int) -> list[Optional[TreeNode]]:
    result: list[Optional[TreeNode]] = []
    if lo > hi:
        result.append(None)
        return result
    for i in range(lo, hi + 1):
        lefts = build_all(lo, i - 1)
        rights = build_all(i + 1, hi)
        for left in lefts:
            for right in rights:
                result.append(TreeNode(i, left, right))
    return result


def serialize(node: Optional[TreeNode], out: list[str]) -> None:
    if node is None:
        out.append("#,")
        return
    out.append(f"{node.val},")
    serialize(node.left, out)
    serialize(node.right, out)


def bench_report(n: int, acc: list[int]) -> None:
    trees = build_all(1, n)
    count = len(trees)
    a = (acc[0] * 131 + (count + 1)) % 1000000007
    for tree in trees:
        parts: list[str] = []
        serialize(tree, parts)
        for b in "".join(parts).encode():
            a = (a * 131 + b) % 1000000007
        a = (a * 131 + 7) % 1000000007
    acc[0] = a


def main() -> None:
    # Smaller repeat count than the compiled mirrors (pure-Python recursion is slow);
    # timed separately, not cross-checked against the sink.
    acc = [0]
    for _ in range(40):
        for n in range(1, 9):
            bench_report(n, acc)
    print(acc[0])


if __name__ == "__main__":
    main()
