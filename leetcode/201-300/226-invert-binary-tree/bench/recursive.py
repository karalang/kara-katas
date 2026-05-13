"""Benchmark workload — recursive DFS invert.

Algorithmic mirror of bench/recursive.kara. See ../README.md § Benchmarks
for the choice of N / K, LCG seed, and BFS-position-weighted sink.
"""

from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def invert(root: TreeNode | None) -> TreeNode | None:
    if root is None:
        return None
    new_left = invert(root.right)
    new_right = invert(root.left)
    root.left = new_left
    root.right = new_right
    return root


def build_tree(n: int) -> TreeNode | None:
    if n <= 0:
        return None
    nodes = [TreeNode(i) for i in range(n)]
    state = 12345
    for i in range(1, n):
        cur = nodes[0]
        while True:
            state = (state * 1103515245 + 12345) & 2147483647
            bit = state & 1
            if bit == 0:
                if cur.left is None:
                    cur.left = nodes[i]
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = nodes[i]
                    break
                cur = cur.right
    return nodes[0]


def bfs_sink(root: TreeNode | None) -> int:
    if root is None:
        return 0
    queue: deque[TreeNode] = deque([root])
    pos = 0
    total = 0
    while queue:
        cur = queue.popleft()
        pos += 1
        total += cur.val * pos
        if cur.left is not None:
            queue.append(cur.left)
        if cur.right is not None:
            queue.append(cur.right)
    return total


def main() -> None:
    # Random walks under the LCG can produce paths deeper than CPython's
    # default 1000-frame limit; bump it so recursion mirrors the iterative
    # build/sink without changing observable output.
    sys.setrecursionlimit(50000)
    root = build_tree(2000)
    for _ in range(10):
        root = invert(root)
    print(bfs_sink(root))


if __name__ == "__main__":
    main()
