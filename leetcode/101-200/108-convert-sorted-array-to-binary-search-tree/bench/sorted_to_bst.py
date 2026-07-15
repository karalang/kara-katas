#!/usr/bin/env python3
# Benchmark workload for LeetCode #108 — sorted array to BST, Python mirror.
# Runs a SMALLER K (pure-Python recursion is slow); timed separately, NOT cross-checked.
import sys

MOD = 1000000007


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def build(arr, lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    n = Node(arr[mid])
    n.left = build(arr, lo, mid - 1)
    n.right = build(arr, mid + 1, hi)
    return n


def ser(n, acc):
    if n is None:
        return (acc * 131 + 1) % MOD
    acc = (acc * 131 + (n.val + 2)) % MOD
    acc = ser(n.left, acc)
    acc = ser(n.right, acc)
    return acc


def main():
    arrs = [[t * 100 + i for i in range(15)] for t in range(8)]
    acc = 1
    K = 60000
    for _ in range(K):
        idx = acc % 8
        root = build(arrs[idx], 0, 14)
        s = ser(root, 0)
        acc = (acc * 131 + s) % MOD
    print(acc)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
