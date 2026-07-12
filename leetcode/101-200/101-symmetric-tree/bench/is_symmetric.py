"""Benchmark workload for LeetCode #101 — symmetric tree, Python mirror.
Smaller K (pure-Python is slow); timed separately, not cross-checked."""

from __future__ import annotations

import sys

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


def mirror(n):
    if n is None:
        return None
    m = Node(n.val)
    m.left = mirror(n.right)
    m.right = mirror(n.left)
    return m


def copy_tree(n):
    if n is None:
        return None
    m = Node(n.val)
    m.left = copy_tree(n.left)
    m.right = copy_tree(n.right)
    return m


def is_mirror(a, b):
    if a is None:
        return b is None
    if b is None:
        return False
    return a.val == b.val and is_mirror(a.left, b.right) and is_mirror(a.right, b.left)


def is_symmetric(root):
    if root is None:
        return True
    return is_mirror(root.left, root.right)


def main():
    base = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    bn = len(base)
    pool = []
    for i in range(8):
        sub = None
        for k in range(bn):
            sub = insert(sub, base[(k + i) % bn])
        root = Node(0)
        root.left = sub
        root.right = mirror(sub) if (i % 2) == 0 else copy_tree(sub)
        pool.append(root)
    acc = 1
    for _ in range(400000):
        idx = acc % 8
        sym = is_symmetric(pool[idx])
        acc = (acc * 131 + (1 if sym else 0) + 1) % 1000000007
    print(acc)


if __name__ == "__main__":
    main()
