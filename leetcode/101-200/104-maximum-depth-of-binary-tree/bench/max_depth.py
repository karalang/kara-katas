#!/usr/bin/env python3
# Benchmark workload for LeetCode #104 — max depth, Python mirror.
# Runs a SMALLER K (pure-Python recursion is slow); timed separately, NOT cross-checked.
import sys

MOD = 1000000007


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


def max_depth(n):
    if n is None:
        return 0
    lh = max_depth(n.left)
    rh = max_depth(n.right)
    return 1 + (lh if lh > rh else rh)


def main():
    base = [16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30]
    bn = len(base)
    pool = []
    for t in range(8):
        root = None
        for k in range(bn):
            root = insert(root, base[(k + t) % bn])
        pool.append(root)
    acc = 1
    K = 200000
    for _ in range(K):
        idx = acc % 8
        d = max_depth(pool[idx])
        acc = (acc * 131 + d + 1) % MOD
    print(acc)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
