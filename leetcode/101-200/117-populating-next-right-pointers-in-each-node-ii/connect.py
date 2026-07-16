#!/usr/bin/env python3
"""LeetCode #117 — Python mirror of the O(1)-space `connect.kara`.

Same algorithm: a dummy-head + tail builds each next level's `next` chain while threading the current
level via its already-wired chain. Handles an arbitrary (non-perfect) binary tree. Produces the
byte-identical sink to the Kara solvers (the oracle for this kata)."""

import sys

MOD = 1000000007


class Node:
    __slots__ = ("val", "left", "right", "next")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.next = None


def connect(root):
    leftmost = root
    while leftmost is not None:
        dummy = Node(0)
        tail = dummy
        cur = leftmost
        while cur is not None:
            if cur.left is not None:
                tail.next = cur.left
                tail = cur.left
            if cur.right is not None:
                tail.next = cur.right
                tail = cur.right
            cur = cur.next
        leftmost = dummy.next


def insert(root, v):
    if root is None:
        return Node(v)
    if v < root.val:
        root.left = insert(root.left, v)
    else:
        root.right = insert(root.right, v)
    return root


def build_bst(seed, count):
    root = None
    s = seed
    for _ in range(count):
        s = (s * 1103515245 + 12345) % 2147483648
        root = insert(root, s % 500)
    return root


def level_hash(root):
    h = 1
    head = root
    while head is not None:
        cur = head
        while cur is not None:
            h = (h * 131 + cur.val + 1) % MOD
            cur = cur.next
        h = (h * 31 + 7) % MOD
        nh = None
        scan = head
        while scan is not None:
            if scan.left is not None:
                nh = scan.left
                break
            if scan.right is not None:
                nh = scan.right
                break
            scan = scan.next
        head = nh
    return h


def main():
    sys.setrecursionlimit(100000)
    acc = 0
    for t in range(8):
        root = build_bst(t * 7919 + 1, 12 + t * 3)
        connect(root)
        h = level_hash(root)
        acc = (acc * 131 + h) % MOD
        print(f"tree {t}: level_hash={h}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
