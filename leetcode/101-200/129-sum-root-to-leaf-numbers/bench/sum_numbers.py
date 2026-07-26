"""Benchmark harness for LeetCode #129 — Sum Root to Leaf Numbers.

Mirrors sum_numbers.kara algorithm-for-algorithm. Committed as the correctness
oracle; not a measured lane.
"""

import sys

NP = 4
N = 2047
ITERS = 40000

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def sum_dfs(node, acc):
    if node is None:
        return 0
    cur = acc * 10 + node.val
    if node.left is None and node.right is None:
        return cur
    return sum_dfs(node.left, cur) + sum_dfs(node.right, cur)


def digit(i, seed):
    return ((i * 7 + seed * 3) % 9) + 1


def build_balanced(lo, hi, seed):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    left = build_balanced(lo, mid - 1, seed)
    right = build_balanced(mid + 1, hi, seed)
    return TreeNode(digit(mid, seed), left, right)


def main():
    trees = [build_balanced(0, N - 1, j + 1) for j in range(NP)]

    sink = 0
    for it in range(ITERS):
        idx = (it * 3) % NP
        sink = (sink + sum_dfs(trees[idx], 0)) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
