# LeetCode 783 — Minimum Distance Between BST Nodes: the bench, in Python.
# Mirrors min_diff_in_bst.kara: ancestor bounds over the same 64 trees.
import sys

sys.setrecursionlimit(10000)

I64_MAX = 2**63 - 1


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def closest(n, low, high):
    if n is None:
        return I64_MAX
    best = I64_MAX
    if low != -1:
        best = min(best, n.val - low)
    if high != -1:
        best = min(best, high - n.val)
    best = min(best, closest(n.left, low, n.val))
    return min(best, closest(n.right, n.val, high))


def min_diff_in_bst(root):
    return closest(root, -1, -1)


seed = 783


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def insert(root, v):
    if root is None:
        return TreeNode(v)
    at = root
    while True:
        if v < at.val:
            if at.left is not None:
                at = at.left
            else:
                at.left = TreeNode(v)
                break
        else:
            if at.right is not None:
                at = at.right
            else:
                at.right = TreeNode(v)
                break
    return root


def middle_first(ordered, lo, hi, out):
    if lo > hi:
        return
    mid = (lo + hi) // 2
    out.append(ordered[mid])
    middle_first(ordered, lo, mid - 1, out)
    middle_first(ordered, mid + 1, hi, out)


def main():
    trees = []
    for t in range(64):
        taken = set()
        values = []
        while len(values) < 100:
            hi = next_random()
            v = (hi * 32768 + next_random()) % 100001
            if v not in taken:
                taken.add(v)
                values.append(v)
        if t % 4 >= 2:
            values.sort()
        if t % 4 == 2:
            order = []
            middle_first(values, 0, 99, order)
            values = order
        root = None
        for v in values:
            root = insert(root, v)
        trees.append(root)
    rounds = 2000000
    total = 0
    check = 0
    for r in range(rounds):
        answer = min_diff_in_bst(trees[r % 64])
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{rounds} rounds of 100-value trees: gaps sum to {total}, checksum {check}")


main()
