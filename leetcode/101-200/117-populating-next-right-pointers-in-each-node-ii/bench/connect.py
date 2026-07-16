#!/usr/bin/env python3
"""LeetCode #117 — Python bench mirror (smaller K, timed separately, NOT cross-checked).
Same O(1)-space dummy-head algorithm as connect.kara; K = 800 (pure-Python is ~20x slower per rep).
Its wall-clock is not comparable to the compiled mirrors."""

import sys

MOD = 1000000007


class Node:
    __slots__ = ("val", "left", "right", "next")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.next = None


def insert(root, v):
    if root is None:
        return Node(v)
    if v < root.val:
        root.left = insert(root.left, v)
    else:
        root.right = insert(root.right, v)
    return root


def build_bst(count, base):
    root = None
    s = 88172645
    for _ in range(count):
        s = (s * 1103515245 + 12345) % 2147483648
        root = insert(root, (s % 100000) + base)
    return root


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
    for _ in range(800):
        base = acc % 100
        root = build_bst(500, base)
        connect(root)
        h = level_hash(root)
        acc = (acc * 131 + h) % MOD
    print(acc)


if __name__ == "__main__":
    main()
