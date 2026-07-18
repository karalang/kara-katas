"""LeetCode #124 benchmark mirror (build-once + punch). Same workload as the
Kāra / C / Rust / Go mirrors: a forest of T balanced mixed-sign trees, K passes."""

import sys

sys.setrecursionlimit(1 << 20)

TREE_COUNT = 2048
NODE_COUNT = 511
REPS = 60


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def max_gain(node, best):
    if node is None:
        return 0
    lg = max_gain(node.left, best)
    rg = max_gain(node.right, best)
    left_gain = lg if lg > 0 else 0
    right_gain = rg if rg > 0 else 0
    through = node.val + left_gain + right_gain
    if through > best[0]:
        best[0] = through
    branch = left_gain if left_gain > right_gain else right_gain
    return node.val + branch


def max_path_sum(root):
    best = [-1000000000]
    max_gain(root, best)
    return best[0]


def node_value(i, seed):
    return ((i * 37 + seed * 13) % 41) - 20


def build_balanced(lo, hi, seed):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    node = TreeNode(node_value(mid, seed))
    node.left = build_balanced(lo, mid - 1, seed)
    node.right = build_balanced(mid + 1, hi, seed)
    return node


def main():
    forest = [build_balanced(0, NODE_COUNT - 1, t + 1) for t in range(TREE_COUNT)]
    sink = 0
    for _ in range(REPS):
        for root in forest:
            sink += max_path_sum(root)
    print(sink)


if __name__ == "__main__":
    main()
