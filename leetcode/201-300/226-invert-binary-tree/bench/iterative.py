"""Benchmark workload — iterative BFS invert.

Algorithmic mirror of bench/iterative.kara. See ../README.md § Benchmarks
for the choice of N / K, LCG seed, and BFS-position-weighted sink.
"""

from __future__ import annotations

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
    queue: deque[TreeNode] = deque([root])
    while queue:
        current = queue.popleft()
        current.left, current.right = current.right, current.left
        if current.left is not None:
            queue.append(current.left)
        if current.right is not None:
            queue.append(current.right)
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
    root = build_tree(2000)
    for _ in range(10):
        root = invert(root)
    print(bfs_sink(root))


if __name__ == "__main__":
    main()
