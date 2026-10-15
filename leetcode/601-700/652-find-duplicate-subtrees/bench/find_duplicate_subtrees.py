# Benchmark for #652: a number for every shape, as the Kara ★ arm.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def find_duplicate_subtrees(root):
    ids = {}
    counts = []
    found = []

    def number(node):
        if node is None:
            return 0
        key = (node.val, number(node.left), number(node.right))
        i = ids.get(key)
        if i is None:
            counts.append(0)
            ids[key] = len(counts)
            i = len(counts)
        counts[i - 1] += 1
        if counts[i - 1] == 2:
            found.append(node)
        return i

    number(root)
    return found


seed = 652


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(size, spread):
    root = TreeNode(next_random() % spread)
    for _ in range(1, size):
        c = TreeNode(next_random() % spread)
        node = root
        while True:
            if next_random() % 2 == 0:
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


def main():
    inputs = 4
    rounds = 40
    spreads = [2, 3, 5, 401]
    trees = [random_tree(100000, spreads[i]) for i in range(inputs)]
    kinds = 0
    checksum = 0
    for r in range(rounds):
        found = find_duplicate_subtrees(trees[r % inputs])
        kinds += len(found)
        for n in found:
            checksum = (checksum * 31 + n.val + 1) % 1000000007
    print(f"{inputs} trees, {rounds} rounds: {kinds} kinds, checksum {checksum}")


main()
