"""LeetCode #124: Binary Tree Maximum Path Sum — Python mirror of max_path_sum.kara.

Same algorithm (post-order, clamp child gains at 0, thread a running max) and the
same deterministic tree construction, so the printed sink matches byte-for-byte.
"""


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_gain(node, best):
    # `best` is a one-element list used as a mutable i64 accumulator (mirrors the
    # Kāra `mut ref i64`).
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


def leaf(v):
    return TreeNode(v)


def main():
    sink = 0

    e1 = TreeNode(1, leaf(2), leaf(3))
    sink += max_path_sum(e1)  # 6

    e2_right = TreeNode(20, leaf(15), leaf(7))
    e2 = TreeNode(-10, leaf(9), e2_right)
    sink += max_path_sum(e2)  # 42

    sink += max_path_sum(leaf(-3))  # -3

    neg = TreeNode(-5, leaf(-8), leaf(-2))
    sink += max_path_sum(neg)  # -2

    t = 0
    while t < 8:
        n = 9 + t * 3
        root = build_balanced(0, n - 1, t + 1)
        sink += max_path_sum(root)
        t += 1

    print(sink)


if __name__ == "__main__":
    main()
