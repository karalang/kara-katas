"""Benchmark workload for LeetCode #230 — Kth Smallest Element in a BST (Python; scale lane)."""

import sys

sys.setrecursionlimit(1000000)


def insert(val, left, right, root, v):
    if root == -1:
        idx = len(val)
        val.append(v)
        left.append(-1)
        right.append(-1)
        return idx
    if v < val[root]:
        l = insert(val, left, right, left[root], v)
        left[root] = l
    else:
        r = insert(val, left, right, right[root], v)
        right[root] = r
    return root


def kth_smallest(val, left, right, root, k):
    stack = []
    cur = root
    count = 0
    while cur != -1 or stack:
        while cur != -1:
            stack.append(cur)
            cur = left[cur]
        node = stack.pop()
        count += 1
        if count == k:
            return val[node]
        cur = right[node]
    return -1


def main():
    n = 3000
    queries = 140000

    val = []
    left = []
    right = []
    root = -1
    state = 12345
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        root = insert(val, left, right, root, state)

    sink = 0
    for _ in range(queries):
        state = (state * 1103515245 + 12345) & 2147483647
        k = 1 + (state % n)
        sink += kth_smallest(val, left, right, root, k)
    print(sink)


main()
