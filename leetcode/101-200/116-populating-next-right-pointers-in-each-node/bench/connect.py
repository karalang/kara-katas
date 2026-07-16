#!/usr/bin/env python3
"""LeetCode #116 — Python bench mirror (smaller K, timed separately, NOT cross-checked).
Same O(1)-space algorithm as connect.kara; runs K = 2000 (1/20 of the compiled K) since pure-Python
is ~20x slower per rep. Its wall-clock is not comparable to the compiled mirrors."""

import sys

MOD = 1000000007


class Node:
    __slots__ = ("val", "left", "right", "next")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.next = None


def build_perfect(idx, max_idx, base):
    if idx > max_idx:
        return None
    node = Node(idx + base)
    node.left = build_perfect(2 * idx, max_idx, base)
    node.right = build_perfect(2 * idx + 1, max_idx, base)
    return node


def connect(root):
    leftmost = root
    while leftmost is not None and leftmost.left is not None:
        head = leftmost
        while head is not None:
            head.left.next = head.right
            if head.next is not None:
                head.right.next = head.next.left
            head = head.next
        leftmost = leftmost.left


def level_hash(root):
    h = 1
    leftmost = root
    while leftmost is not None:
        cur = leftmost
        while cur is not None:
            h = (h * 131 + cur.val + 1) % MOD
            cur = cur.next
        h = (h * 31 + 7) % MOD
        leftmost = leftmost.left
    return h


def main():
    sys.setrecursionlimit(100000)
    max_idx = 511  # depth-9 perfect tree
    acc = 0
    for _ in range(2000):
        base = acc % 100
        root = build_perfect(1, max_idx, base)
        connect(root)
        h = level_hash(root)
        acc = (acc * 131 + h) % MOD
    print(acc)


if __name__ == "__main__":
    main()
