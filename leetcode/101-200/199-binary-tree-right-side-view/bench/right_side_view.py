"""Benchmark workload for LeetCode #199 — Binary Tree Right Side View (Python; scale lane)."""

import sys


def right_view(val, left, right, root):
    result = []
    if root == -1:
        return result
    level = [root]
    while len(level) > 0:
        result.append(val[level[-1]])
        nxt = []
        for idx in level:
            if left[idx] != -1:
                nxt.append(left[idx])
            if right[idx] != -1:
                nxt.append(right[idx])
        level = nxt
    return result


def main():
    n = 8191
    passes = 40000
    val = [0] * n
    left = [0] * n
    right = [0] * n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        val[i] = (state >> 16) % 1000
        li = 2 * i + 1
        ri = 2 * i + 2
        left[i] = li if li < n else -1
        right[i] = ri if ri < n else -1
    sink = 0
    for _ in range(passes):
        state = (state * 1103515245 + 12345) & 2147483647
        idx = state % n
        val[idx] = (state >> 16) % 1000
        view = right_view(val, left, right, 0)
        for v in view:
            sink += v
    print(sink)


main()
