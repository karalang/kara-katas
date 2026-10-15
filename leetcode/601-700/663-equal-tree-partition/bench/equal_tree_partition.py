# Benchmark for #663: the subtree sums, listed, as the Kara ★ arm.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def check_equal_tree(root):
    sums = []
    total = subtree_sum(root, sums)
    if total % 2 != 0:
        return False
    sums.pop()
    return any(s == total // 2 for s in sums)


def subtree_sum(node, sums):
    if node is None:
        return 0
    s = node.val + subtree_sum(node.left, sums) + subtree_sum(node.right, sums)
    sums.append(s)
    return s


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def grown_tree(count, rng):
    root = TreeNode(rng.next() % 200001 - 100000)
    for _ in range(1, count):
        at = root
        placed = False
        while not placed:
            if rng.next() % 2 == 0:
                if at.left is not None:
                    at = at.left
                else:
                    at.left = TreeNode(rng.next() % 200001 - 100000)
                    placed = True
            else:
                if at.right is not None:
                    at = at.right
                else:
                    at.right = TreeNode(rng.next() % 200001 - 100000)
                    placed = True
    return root


def copy(node):
    if node is None:
        return None
    n = TreeNode(node.val)
    n.left = copy(node.left)
    n.right = copy(node.right)
    return n


def main():
    rng = Rng(663)
    trees = []
    for _ in range(4):
        trees.append(grown_tree(10000, rng))
        root = TreeNode(0)
        root.left = grown_tree(4999, rng)
        root.right = copy(root.left)
        trees.append(root)
    rounds = 4000
    split = 0
    s = 0
    for r in range(rounds):
        ok = check_equal_tree(trees[r % 8])
        if ok:
            split += 1
        s = (s * 31 + r * 2 + (1 if ok else 0)) % 1000000007
    print(f"8 trees of 10000 nodes, {rounds} rounds: {split} split, checksum {s}")


main()
