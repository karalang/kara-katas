# Benchmark for #814: Binary Tree Pruning -- mirror of the ★ arm
# (post-order recursion), with the same workload as prune_tree.kara.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def prune_tree(root):
    if root is None:
        return None
    root.left = prune_tree(root.left)
    root.right = prune_tree(root.right)
    if root.val == 0 and root.left is None and root.right is None:
        return None
    return root


def build(vals, left, right, i):
    if i < 0:
        return None
    l = build(vals, left, right, left[i])
    r = build(vals, left, right, right[i])
    return TreeNode(vals[i], l, r)


def weigh(root, depth):
    if root is None:
        return 0
    return (root.val + 1) * depth + weigh(root.left, depth + 1) + weigh(root.right, depth + 1)


seed = 814


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n, rounds = 64, 200, 300000
    vals, lefts, rights = [], [], []
    for _ in range(count):
        v = [1 if next_random() % 8 == 0 else 0 for _ in range(n)]
        l = [-1] * n
        r = [-1] * n
        for i in range(1, n):
            while True:
                p = next_random() % i
                if next_random() % 2 == 0:
                    if l[p] < 0:
                        l[p] = i
                        break
                elif r[p] < 0:
                    r[p] = i
                    break
        vals.append(v)
        lefts.append(l)
        rights.append(r)
    checksum = 0
    for rnd in range(rounds):
        g = rnd % count
        i = next_random() % n
        vals[g][i] = 1 - vals[g][i]
        root = prune_tree(build(vals[g], lefts[g], rights[g], 0))
        checksum = (checksum * 31 + weigh(root, 1)) % 1000000007
    print(f"{rounds} rounds of {n} nodes: checksum {checksum}")


main()
