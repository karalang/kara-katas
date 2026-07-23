"""Benchmark workload for LeetCode #173 — Binary Search Tree Iterator (Python; scale lane)."""

import sys

# vals[i], left[i], right[i] parallel arrays = index-pool BST.
vals = []
left = []
right = []


def insert(root, val):
    if root == -1:
        vals.append(val)
        left.append(-1)
        right.append(-1)
        return len(vals) - 1
    if val < vals[root]:
        left[root] = insert(left[root], val)
    else:
        right[root] = insert(right[root], val)
    return root


def main():
    sys.setrecursionlimit(100000)
    n = 4000
    passes = 30000

    root = -1
    state = 12345
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        v = state % 1000
        root = insert(root, v)

    sink = 0
    for p in range(passes):
        idx = (p * 1315423911 + 7) % n
        vals[idx] = (vals[idx] + 1) % 1000

        stack = []
        cur = root
        while cur != -1:
            stack.append(cur)
            cur = left[cur]
        pos = 1
        while stack:
            top = stack.pop()
            sink += pos * vals[top]
            pos += 1
            r = right[top]
            while r != -1:
                stack.append(r)
                r = left[r]
    print(sink)


main()
