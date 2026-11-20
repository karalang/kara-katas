# LeetCode #1214 bench, in Python: the ★ arm (each tree's values read in
# order, then two pointers, one climbing the first list and one coming
# down the second) on 16 pairs of balanced search trees of 5000 nodes
# each, built once; then 10 rounds over the pairs, four targets each,
# every answer folded into a checksum.

import sys

sys.setrecursionlimit(10000)

seed = 1214


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big():
    hi = next_random()
    lo = next_random()
    return (hi * 32768 + lo) % 2000000001 - 1000000000


def in_order(node, out):
    if node is not None:
        in_order(node.left, out)
        out.append(node.val)
        in_order(node.right, out)


def two_sum_bsts(root1, root2, target):
    a, b = [], []
    in_order(root1, a)
    in_order(root2, b)
    i, j = 0, len(b) - 1
    while i < len(a) and j >= 0:
        s = a[i] + b[j]
        if s == target:
            return True
        if s < target:
            i += 1
        else:
            j -= 1
    return False


def balanced(sorted_values, low, high):
    if low >= high:
        return None
    mid = (low + high) // 2
    return TreeNode(sorted_values[mid], balanced(sorted_values, low, mid), balanced(sorted_values, mid + 1, high))


def distinct_values(n):
    seen = set()
    while len(seen) < n:
        seen.add(big())
    return sorted(seen)


def main():
    pairs = []
    for _ in range(16):
        a = distinct_values(5000)
        b = distinct_values(5000)
        i = next_random() % 5000
        j = next_random() % 5000
        t3 = big()
        t4 = big()
        pairs.append((balanced(a, 0, 5000), balanced(b, 0, 5000), [a[i] + b[j], a[j] + b[i], t3, t4]))
    check = 0
    for rnd in range(10):
        for t1, t2, targets in pairs:
            for t in targets:
                answer = 2 if two_sum_bsts(t1, t2, t) else 1
                check = (check * 131 + answer + rnd) % 1000000007
    print(f"10 rounds over 16 pairs of 5000-node trees: checksum {check}")


main()
