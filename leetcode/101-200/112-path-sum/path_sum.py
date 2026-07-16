#!/usr/bin/env python3
"""LeetCode #112: Path Sum — recursive DFS with a running remainder (mirror of path_sum.kara).

Is there a root-to-leaf path summing to target? Subtract each node's value from the remaining
target; the answer is yes exactly when some leaf is reached with remainder zero. The leaf check
is essential — only a leaf can complete a path.
"""


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def insert(root, v):
    if root is None:
        return TreeNode(v)
    if v < root.val:
        root.left = insert(root.left, v)
    else:
        root.right = insert(root.right, v)
    return root


def has_path_sum(node, target):
    if node is None:
        return False
    rem = target - node.val
    if node.left is None and node.right is None:
        return rem == 0
    return has_path_sum(node.left, rem) or has_path_sum(node.right, rem)


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


def main():
    acc = 0
    for t in range(8):
        n = 7 + t
        root = build_balanced(t * 20, t * 20 + n - 1)
        target = leftmost_path_sum(root) if t % 2 == 0 else 1000000000
        hit = has_path_sum(root, target)
        acc = (acc * 131 + (1 if hit else 0) + 1) % 1000000007
        print(f"tree {t}: target {target} has_path={'true' if hit else 'false'}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
