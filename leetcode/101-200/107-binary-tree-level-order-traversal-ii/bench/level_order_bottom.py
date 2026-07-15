#!/usr/bin/env python3
# Benchmark workload for LeetCode #107 — bottom-up level order, Python mirror.
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


def dfs(node, depth, rows):
    if node is None:
        return
    if depth == len(rows):
        rows.append([])
    rows[depth].append(node.val)
    dfs(node.left, depth + 1, rows)
    dfs(node.right, depth + 1, rows)


def level_order_bottom(root):
    rows = []
    dfs(root, 0, rows)
    out = []
    for d in range(len(rows) - 1, -1, -1):
        out.append(list(rows[d]))
    return out


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
    K = 50000
    for _ in range(K):
        idx = acc % 8
        levels = level_order_bottom(pool[idx])
        acc = (acc * 131 + len(levels)) % MOD
        for lvl in levels:
            acc = (acc * 131 + len(lvl)) % MOD
            for v in lvl:
                acc = (acc * 131 + v) % MOD
    print(acc)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
