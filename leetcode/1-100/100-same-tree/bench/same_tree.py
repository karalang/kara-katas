"""Benchmark workload for LeetCode #100 — same tree, Python mirror.
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


def is_same(p, q):
    if p is None:
        return q is None
    if q is None:
        return False
    return p.val == q.val and is_same(p.left, q.left) and is_same(p.right, q.right)


def main():
    base = [16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30]
    bn = len(base)
    pool_p = []
    pool_q = []
    for i in range(8):
        p = q = None
        for k in range(bn):
            p = insert(p, base[k])
            bump = 1 if (i % 2) == 1 and k == (i % bn) else 0
            q = insert(q, base[k] + bump)
        pool_p.append(p)
        pool_q.append(q)
    acc = 1
    for _ in range(300000):
        idx = acc % 8
        same = is_same(pool_p[idx], pool_q[idx])
        acc = (acc * 131 + (1 if same else 0) + 1) % 1000000007
    print(acc)


if __name__ == "__main__":
    main()
