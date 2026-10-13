# Benchmark for #508: Python mirror of the ★ arm (post-order with a count
# table); see find_frequent_tree_sum.kara. The count table is a fresh
# dict for every call.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def subtree_sum(node, counts):
    if node is None:
        return 0
    s = node.val + subtree_sum(node.left, counts) + subtree_sum(node.right, counts)
    counts[s] = counts.get(s, 0) + 1
    return s


def find_frequent_tree_sum(root):
    counts = {}
    subtree_sum(root, counts)
    best = 0
    for c in counts.values():
        if c > best:
            best = c
    return [s for s, c in counts.items() if c == best]


# ---- benchmark --------------------------------------------------------------

seed = 508


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(values, lo, hi):
    if lo >= hi:
        return None
    mid = lo + next_random() % (hi - lo)
    left = build(values, lo, mid)
    right = build(values, mid + 1, hi)
    return TreeNode(values[mid], left, right)


def main():
    # 100 random trees of 10,000 nodes, the values from -2 to 2, from -50
    # to 50, or from the whole range -100,000 to 100,000 in turn, built
    # once. Then each is solved 30 times.
    trees = 100
    all_trees = []
    for t in range(trees):
        half = 2 if t % 3 == 0 else 50 if t % 3 == 1 else 100000
        values = [next_random() % (2 * half + 1) - half for _ in range(10000)]
        all_trees.append(build(values, 0, 10000))
    found = 0
    total = 0
    for _ in range(30):
        for t in range(trees):
            for s in find_frequent_tree_sum(all_trees[t]):
                found += 1
                total += s
    print(f"{trees} trees of 10000 nodes, 30 times each: {found} most frequent sums, adding up to {total}")


main()
