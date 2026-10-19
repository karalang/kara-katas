# LeetCode 783 — Minimum Distance Between BST Nodes, ancestor bounds.
# Mirrors min_diff_in_bst.kara (the ★ arm) and its harness.
import sys

sys.setrecursionlimit(10000)

I64_MAX = 2**63 - 1


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def closest(node, low, high):
    if node is None:
        return I64_MAX
    best = I64_MAX
    if low != -1:
        best = min(best, node.val - low)
    if high != -1:
        best = min(best, high - node.val)
    best = min(best, closest(node.left, low, node.val))
    return min(best, closest(node.right, node.val, high))


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


def build(values):
    root = None
    for v in values:
        root = insert(root, v)
    return root


def random_values(n, top):
    taken = set()
    out = []
    while len(out) < n:
        hi = next_random()
        v = (hi * 32768 + next_random()) % (top + 1)
        if v not in taken:
            taken.add(v)
            out.append(v)
    return out


def show(values):
    answer = min_diff_in_bst(build(values))
    print(f"insert [{', '.join(map(str, values))}] -> {answer}")


def main():
    show([4, 2, 6, 1, 3])
    show([1, 0, 48, 12, 49])
    show([0, 100000])
    show([10, 5, 15, 9, 11])
    show([90, 69, 49, 89, 52])
    show([1, 2, 3, 4, 5, 7])
    show([50, 40, 30, 20, 10, 11])
    chain = [i * 1000 + (1 if i == 63 else 0) for i in range(100)]
    print(f"an ascending chain of 100 -> {min_diff_in_bst(build(chain))}")
    answer = min_diff_in_bst(build(random_values(100, 100000)))
    print(f"100 random values -> {answer}")
    total = 0
    check = 0
    for _ in range(300):
        n = 2 + next_random() % 99
        top = n - 1 + next_random() % 2000
        answer = min_diff_in_bst(build(random_values(n, top)))
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"300 random trees: gaps sum to {total}, checksum {check}")


main()
