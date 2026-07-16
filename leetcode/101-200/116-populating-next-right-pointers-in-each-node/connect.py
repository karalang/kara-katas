#!/usr/bin/env python3
"""LeetCode #116 — Python mirror of the O(1)-space `connect.kara`.

Same algorithm: thread each already-wired level via its `next` chain to stitch the level below.
Produces the byte-identical sink to the Kara solvers (the oracle for this kata)."""

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
    while leftmost is not None and leftmost.left is not None:
        head = leftmost
        while head is not None:
            head.left.next = head.right
            if head.next is not None:
                head.right.next = head.next.left
            head = head.next
        leftmost = leftmost.left


def build_perfect(idx, max_idx, base):
    if idx > max_idx:
        return None
    node = Node(idx + base)
    node.left = build_perfect(2 * idx, max_idx, base)
    node.right = build_perfect(2 * idx + 1, max_idx, base)
    return node


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
    acc = 0
    for t in range(8):
        depth = 2 + (t % 8)
        max_idx = (1 << depth) - 1
        root = build_perfect(1, max_idx, t * 100)
        connect(root)
        h = level_hash(root)
        acc = (acc * 131 + h) % MOD
        print(f"tree {t}: level_hash={h}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
