# Benchmark mirror for #617: the same workload and algorithm as
# merge_trees.kara (recursion, a new tree).
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def merge_trees(root1, root2):
    if root1 is not None and root2 is not None:
        return TreeNode(root1.val + root2.val,
                        merge_trees(root1.left, root2.left),
                        merge_trees(root1.right, root2.right))
    return root1 if root1 is not None else root2


seed = 617


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(size, lean):
    root = TreeNode(next_random() % 20001 - 10000)
    for _ in range(1, size):
        c = TreeNode(next_random() % 20001 - 10000)
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
    return root


def walk(node, acc):
    if node is not None:
        acc[0] += 1
        acc[1] = (acc[1] * 31 + node.val + 20000) % 1000000007
        walk(node.left, acc)
        walk(node.right, acc)


def main():
    trees = 20
    rounds = 10000
    every = []
    for _ in range(trees):
        lean = 30 + next_random() % 41
        every.append(random_tree(2000, lean))
    acc = [0, 0]
    for r in range(rounds):
        merged = merge_trees(every[(r * 7) % trees], every[(r * 3 + 1) % trees])
        walk(merged, acc)
    print(f"{trees} trees, {rounds} rounds: {acc[0]} nodes, checksum {acc[1]}")


main()
