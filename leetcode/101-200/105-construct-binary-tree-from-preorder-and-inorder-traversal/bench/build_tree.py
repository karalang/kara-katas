#!/usr/bin/env python3
# Benchmark workload for LeetCode #103 — construct binary tree, Python mirror.
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


def find_in(inorder, lo, hi, target):
    for i in range(lo, hi + 1):
        if inorder[i] == target:
            return i
    return -1


def build(pre, ino, plo, phi, ilo, ihi):
    if plo > phi:
        return None
    rv = pre[plo]
    mid = find_in(ino, ilo, ihi, rv)
    lsize = mid - ilo
    n = Node(rv)
    n.left = build(pre, ino, plo + 1, plo + lsize, ilo, mid - 1)
    n.right = build(pre, ino, plo + lsize + 1, phi, mid + 1, ihi)
    return n


def ser(n, acc):
    if n is None:
        return (acc * 131 + 1) % MOD
    acc = (acc * 131 + (n.val + 2)) % MOD
    acc = ser(n.left, acc)
    acc = ser(n.right, acc)
    return acc


def preorder_of(n, out):
    if n is None:
        return
    out.append(n.val)
    preorder_of(n.left, out)
    preorder_of(n.right, out)


def inorder_of(n, out):
    if n is None:
        return
    inorder_of(n.left, out)
    out.append(n.val)
    inorder_of(n.right, out)


def main():
    base = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    bn = len(base)
    pres, inos = [], []
    for t in range(8):
        root = None
        for k in range(bn):
            root = insert(root, base[(k + t) % bn])
        pre, ino = [], []
        preorder_of(root, pre)
        inorder_of(root, ino)
        pres.append(pre)
        inos.append(ino)
    acc = 1
    K = 40000
    for _ in range(K):
        idx = acc % 8
        rebuilt = build(pres[idx], inos[idx], 0, bn - 1, 0, bn - 1)
        s = ser(rebuilt, 0)
        acc = (acc * 131 + s) % MOD
    print(acc)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
