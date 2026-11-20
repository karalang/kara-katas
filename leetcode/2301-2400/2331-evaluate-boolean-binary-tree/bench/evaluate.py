# LeetCode #2331: Evaluate Boolean Binary Tree -- the bench, the ★ arm
# in Python. A leaf is its own truth, and an OR or an AND node its two
# subtrees evaluated recursively and joined by `or` or `and`, which stop
# at the first child that settles it. O(n).

import sys


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def evaluate_tree(root):
    if root is None:
        return False
    if root.val == 0:
        return False
    if root.val == 1:
        return True
    if root.val == 2:
        return evaluate_tree(root.left) or evaluate_tree(root.right)
    return evaluate_tree(root.left) and evaluate_tree(root.right)


def main():
    seed = 2331

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def random_tree(depth):
        if depth == 0 or next_random() % 8 == 0:
            return TreeNode(next_random() % 2)
        op = next_random() % 2 + 2
        left = random_tree(depth - 1)
        right = random_tree(depth - 1)
        return TreeNode(op, left, right)

    trees = [random_tree(14) for _ in range(200)]
    check = 0
    for p in range(500):
        for k in range(200):
            truth = 1 if evaluate_tree(trees[k]) else 2
            check = (check * 3 + truth + p) % 1000000007
    print(f"500 passes over 200 trees of depth up to 14: checksum {check}")


sys.setrecursionlimit(10000)
main()
