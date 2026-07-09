"""Benchmark workload — Validate Binary Search Tree (LeetCode #98).

Python mirror of bench/validate_bst.kara. Each iteration builds a fresh 63-node
balanced BST (object per node), runs the ★'s recursive (lo,hi)-bounds validator,
folds shift+valid into the same rolling polynomial hash. CPython is multi-second
at the compiled mirrors' K=200_000, so this runs K=20_000 (1/10th) — timed
separately and NOT cross-checked against the compiled sink. See
../README.md § Benchmarks.
"""

from __future__ import annotations

import sys
from typing import Optional

sys.setrecursionlimit(100000)


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val: int, left: "Optional[Node]", right: "Optional[Node]") -> None:
        self.val = val
        self.left = left
        self.right = right


def build(lo: int, hi: int, shift: int) -> Optional[Node]:
    if lo > hi:
        return None
    mid = lo + (hi - lo) // 2
    return Node(shift + mid, build(lo, mid - 1, shift), build(mid + 1, hi, shift))


def is_valid(n: Optional[Node], lo: Optional[int], hi: Optional[int]) -> bool:
    if n is None:
        return True
    if lo is not None and n.val <= lo:
        return False
    if hi is not None and n.val >= hi:
        return False
    return is_valid(n.left, lo, n.val) and is_valid(n.right, n.val, hi)


def main() -> None:
    total = 20_000
    modulus = 1_000_000_007
    size = 63

    acc = 0
    for k in range(total):
        shift = k % 1000
        root = build(0, size - 1, shift)
        bit = 1 if is_valid(root, None, None) else 0
        acc = (acc * 131 + shift + bit) % modulus
    print(acc)


if __name__ == "__main__":
    main()
