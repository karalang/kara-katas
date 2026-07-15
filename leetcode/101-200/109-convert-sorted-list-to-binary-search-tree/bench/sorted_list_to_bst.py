#!/usr/bin/env python3
# Benchmark workload for LeetCode #109 — sorted list to BST, Python mirror.
# Runs a SMALLER K (pure-Python recursion is slow); timed separately, NOT cross-checked.
import sys

MOD = 1000000007


class LNode:
    __slots__ = ("val", "next")

    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt


class TNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def build_list(length, off):
    head = None
    for i in range(length - 1, -1, -1):
        head = LNode(off + 1 + i, head)
    return head


def build_from_arr(arr, lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    n = TNode(arr[mid])
    n.left = build_from_arr(arr, lo, mid - 1)
    n.right = build_from_arr(arr, mid + 1, hi)
    return n


def sorted_list_to_bst(head):
    arr = []
    cur = head
    while cur is not None:
        arr.append(cur.val)
        cur = cur.next
    return build_from_arr(arr, 0, len(arr) - 1)


def ser(n, acc):
    if n is None:
        return (acc * 131 + 1) % MOD
    acc = (acc * 131 + (n.val + 2)) % MOD
    acc = ser(n.left, acc)
    acc = ser(n.right, acc)
    return acc


def main():
    pool = [build_list(15, t * 100) for t in range(8)]
    acc = 1
    K = 60000
    for _ in range(K):
        idx = acc % 8
        root = sorted_list_to_bst(pool[idx])
        s = ser(root, 0)
        acc = (acc * 131 + s) % MOD
    print(acc)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
