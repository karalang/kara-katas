#!/usr/bin/env python3
# Benchmark workload for LeetCode #106 — construct binary tree (inorder+postorder), Python.
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


def build(post, ino, plo, phi, ilo, ihi):
    if plo > phi:
        return None
    rv = post[phi]
    mid = find_in(ino, ilo, ihi, rv)
    lsize = mid - ilo
    n = Node(rv)
    n.left = build(post, ino, plo, plo + lsize - 1, ilo, mid - 1)
    n.right = build(post, ino, plo + lsize, phi - 1, mid + 1, ihi)
    return n


def ser(n, acc):
    if n is None:
        return (acc * 131 + 1) % MOD
    acc = (acc * 131 + (n.val + 2)) % MOD
    acc = ser(n.left, acc)
    acc = ser(n.right, acc)
    return acc


def inorder_of(n, out):
    if n is None:
        return
    inorder_of(n.left, out)
    out.append(n.val)
    inorder_of(n.right, out)


def postorder_of(n, out):
    if n is None:
        return
    postorder_of(n.left, out)
    postorder_of(n.right, out)
    out.append(n.val)


def main():
    base = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    bn = len(base)
    posts, inos = [], []
    for t in range(8):
        root = None
        for k in range(bn):
            root = insert(root, base[(k + t) % bn])
        ino, post = [], []
        inorder_of(root, ino)
        postorder_of(root, post)
        posts.append(post)
        inos.append(ino)
    acc = 1
    K = 40000
    for _ in range(K):
        idx = acc % 8
        rebuilt = build(posts[idx], inos[idx], 0, bn - 1, 0, bn - 1)
        s = ser(rebuilt, 0)
        acc = (acc * 131 + s) % MOD
    print(acc)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
