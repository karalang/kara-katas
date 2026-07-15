#!/usr/bin/env python3
# Benchmark workload for LeetCode #110 — balanced binary tree, Python mirror.
# Runs a SMALLER K (pure-Python recursion is slow); timed separately, NOT cross-checked.
import sys

MOD = 1000000007


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def build_balanced(lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    n = Node(mid)
    n.left = build_balanced(lo, mid - 1)
    n.right = build_balanced(mid + 1, hi)
    return n


def check(n):
    if n is None:
        return 0
    lh = check(n.left)
    if lh == -1:
        return -1
    rh = check(n.right)
    if rh == -1:
        return -1
    if abs(lh - rh) > 1:
        return -1
    return 1 + (lh if lh > rh else rh)


def is_balanced(root):
    return check(root) != -1


def main():
    pool = [build_balanced(t * 100, t * 100 + 30) for t in range(8)]
    acc = 1
    K = 150000
    for _ in range(K):
        idx = acc % 8
        bal = is_balanced(pool[idx])
        acc = (acc * 131 + (1 if bal else 0) + 1) % MOD
    print(acc)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
