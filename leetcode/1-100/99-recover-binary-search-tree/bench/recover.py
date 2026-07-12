"""Benchmark workload for LeetCode #99 — recover BST, Python mirror.
Smaller K (pure-Python is slow); timed separately, not cross-checked."""

from __future__ import annotations

import sys
from typing import Optional

sys.setrecursionlimit(10000)


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def insert(root, v):
    if root is None:
        return Node(v)
    if v < root.val:
        root.left = insert(root.left, v)
    else:
        root.right = insert(root.right, v)
    return root


def collect(node, out):
    if node is None:
        return
    collect(node.left, out)
    out.append(node)
    collect(node.right, out)


def sum_inorder(node, acc):
    if node is None:
        return acc
    acc = sum_inorder(node.left, acc)
    acc = (acc * 131 + node.val) % 1000000007
    return sum_inorder(node.right, acc)


def recover(root):
    nodes = []
    collect(root, nodes)
    fi = si = -1
    for i in range(1, len(nodes)):
        if nodes[i - 1].val > nodes[i].val:
            if fi < 0:
                fi = i - 1
            si = i
    if fi >= 0:
        nodes[fi].val, nodes[si].val = nodes[si].val, nodes[fi].val


def corrupt2(root, a, b):
    ns = []
    collect(root, ns)
    if a != b:
        ns[a].val, ns[b].val = ns[b].val, ns[a].val


def main():
    vals = [16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]
    n = 31
    root = None
    for v in vals:
        root = insert(root, v)
    acc = 1
    for _ in range(30000):
        a = acc % n
        b = (acc * 7 + 3) % n
        corrupt2(root, a, b)
        cs = sum_inorder(root, 0)
        acc = (acc * 131 + cs) % 1000000007
        recover(root)
    print(acc)


if __name__ == "__main__":
    main()
