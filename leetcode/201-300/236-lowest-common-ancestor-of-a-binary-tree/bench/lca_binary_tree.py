"""Benchmark harness for LeetCode #236 — LCA of a Binary Tree.

Mirrors lca_binary_tree.kara algorithm-for-algorithm. Committed as the
correctness oracle; not a measured lane.

sys.setrecursionlimit is raised because the post-order search recurses to the
tree depth (~17 here) but CPython's default limit is low enough to be worth
guarding against for larger N.
"""

import sys

N = 100000
ITERS = 600

sys.setrecursionlimit(100000)


def lca(val, left, right, cur, p, q):
    if cur == -1:
        return -1
    if val[cur] == p or val[cur] == q:
        return cur
    l = lca(val, left, right, left[cur], p, q)
    r = lca(val, left, right, right[cur], p, q)
    if l != -1 and r != -1:
        return cur
    if l != -1:
        return l
    return r


def main():
    val = []
    left = []
    right = []
    for i in range(N):
        lc = 2 * i + 1
        rc = 2 * i + 2
        val.append(i)
        left.append(lc if lc < N else -1)
        right.append(rc if rc < N else -1)

    sink = 0
    y = 2024
    for _ in range(ITERS):
        y = (y * 1103515245 + 12345) % 2147483648
        p = (y // 65536) % N
        y = (y * 1103515245 + 12345) % 2147483648
        q = (y // 65536) % N
        ans = lca(val, left, right, 0, p, q)
        v = -1 if ans == -1 else val[ans]
        sink = (sink + v) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
