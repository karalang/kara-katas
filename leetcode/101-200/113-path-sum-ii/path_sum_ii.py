#!/usr/bin/env python3
"""LeetCode #113: Path Sum II — backtracking DFS (mirror of path_sum_ii.kara).

Collect every root-to-leaf path whose values sum to target. Push each node's value onto a running
path descending, snapshot the path when a leaf exhausts the remainder, and pop on the way back up.
"""


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def dfs(node, target, path, out):
    if node is None:
        return
    path.append(node.val)
    rem = target - node.val
    if node.left is None and node.right is None:
        if rem == 0:
            out.append(list(path))
    else:
        dfs(node.left, rem, path, out)
        dfs(node.right, rem, path, out)
    path.pop()


def path_sum(root, target):
    out = []
    dfs(root, target, [], out)
    return out


def build_perfect(depth, val):
    if depth <= 0:
        return None
    node = TreeNode(val)
    node.left = build_perfect(depth - 1, val)
    node.right = build_perfect(depth - 1, val)
    return node


def build_balanced(lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    node = TreeNode(mid)
    node.left = build_balanced(lo, mid - 1)
    node.right = build_balanced(mid + 1, hi)
    return node


def leftmost_path_sum(node):
    if node is None:
        return 0
    if node.left is not None:
        return node.val + leftmost_path_sum(node.left)
    return node.val + leftmost_path_sum(node.right)


def hash_paths(paths):
    h = 1
    for p in paths:
        h = (h * 1000003 + 7) % 1000000007
        for v in p:
            h = (h * 131 + v + 1000) % 1000000007
    return h


def main():
    acc = 0
    for t in range(8):
        if t % 2 == 0:
            depth = 3 + (t % 3)
            val = 2 + t
            root = build_perfect(depth, val)
            paths = path_sum(root, depth * val)
        else:
            n = 7 + t
            root = build_balanced(t * 20, t * 20 + n - 1)
            paths = path_sum(root, leftmost_path_sum(root))
        cnt = len(paths)
        h = hash_paths(paths)
        acc = (acc * 131 + cnt + h) % 1000000007
        print(f"tree {t}: paths={cnt} hash={h}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
