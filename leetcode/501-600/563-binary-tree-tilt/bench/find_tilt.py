# Benchmark for #563: Python mirror of the ★ arm (subtree sums,
# recursively); see find_tilt.kara.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def subtree_sum(node, total):
    if node is None:
        return 0
    l = subtree_sum(node.left, total)
    r = subtree_sum(node.right, total)
    total[0] += abs(l - r)
    return node.val + l + r


def find_tilt(root):
    total = [0]
    subtree_sum(root, total)
    return total[0]


seed = 563


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 random trees of 10,000 nodes (the problem's most), each new
    # node walking down from the root and going left with chance 50 to
    # 88 in 100, built once, the nodes kept in the order they were
    # added. Then 1,000 times over every tree the subtree at one of its
    # first 16 nodes, picked by the round and the tree, is answered.
    trees = 20
    all_trees = []
    for g in range(trees):
        lean = 50 + 2 * g
        root = TreeNode(next_random() % 2001 - 1000)
        nodes = [root]
        for _ in range(1, 10000):
            c = TreeNode(next_random() % 2001 - 1000)
            node = root
            while True:
                if next_random() % 100 < lean:
                    if node.left is not None:
                        node = node.left
                    else:
                        node.left = c
                        break
                else:
                    if node.right is not None:
                        node = node.right
                    else:
                        node.right = c
                        break
            nodes.append(c)
        all_trees.append(nodes)
    total = 0
    checksum = 0
    for r in range(1000):
        for t in range(trees):
            d = find_tilt(all_trees[t][(r * 37 + t * 11) % 16])
            total += d
            checksum = (checksum * 31 + d) % 1000000007
    print(f"{trees} trees, 1000 times each: tilts {total}, checksum {checksum}")


main()
