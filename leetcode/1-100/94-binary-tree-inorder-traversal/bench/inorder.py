"""Benchmark workload — Binary Tree Inorder Traversal (LeetCode #94).

Python mirror of bench/inorder.kara. Builds a fresh 63-node balanced tree per iteration
and folds a recursive inorder walk into a rolling hash in visit order. Smaller K
(pure-Python recursion is slow); timed separately, NOT cross-checked. See ../README.md.
"""

import sys


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def build(lo, hi, shift):
    if lo > hi:
        return None
    mid = lo + (hi - lo) // 2
    return Node(shift + mid, build(lo, mid - 1, shift), build(mid + 1, hi, shift))


def inorder_fold(node, acc):
    if node is None:
        return
    inorder_fold(node.left, acc)
    acc[0] = (acc[0] * 131 + (node.val + 1)) % 1000000007
    inorder_fold(node.right, acc)


def main():
    total = 40000
    modulus = 1000000007
    size = 63
    total_sum = 0
    for k in range(total):
        shift = k % 1000
        root = build(0, size - 1, shift)
        acc = [0]
        inorder_fold(root, acc)
        total_sum = (total_sum * 131 + acc[0]) % modulus
    print(total_sum)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
