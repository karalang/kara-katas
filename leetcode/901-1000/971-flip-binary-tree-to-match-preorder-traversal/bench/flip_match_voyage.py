# Benchmark: LeetCode #971 Flip Binary Tree To Match Preorder Traversal
# -- the ★ arm, one walk flipping where the voyage says, on 200 random
# trees of 100 nodes. Mirrors flip_match_voyage.kara, .c, .rs and
# go-seq/.

import sys


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(t, voyage, i, flipped):
    if t is None:
        return True
    if t.val != voyage[i[0]]:
        return False
    i[0] += 1
    if t.left is not None and t.left.val != voyage[i[0]]:
        flipped.append(t.val)
        return walk(t.right, voyage, i, flipped) and walk(t.left, voyage, i, flipped)
    return walk(t.left, voyage, i, flipped) and walk(t.right, voyage, i, flipped)


def flip_match_voyage(root, voyage):
    flipped = []
    if walk(root, voyage, [0], flipped):
        return flipped
    return [-1]


seed = 971


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_permutation(n):
    a = list(range(1, n + 1))
    i = n - 1
    while i > 0:
        j = next_random() % (i + 1)
        a[i], a[j] = a[j], a[i]
        i -= 1
    return a


def random_tree(vals):
    root = TreeNode(vals[0])
    for v in vals[1:]:
        node = TreeNode(v)
        cur = root
        while True:
            if next_random() % 2 == 0:
                if cur.left is not None:
                    cur = cur.left
                else:
                    cur.left = node
                    break
            else:
                if cur.right is not None:
                    cur = cur.right
                else:
                    cur.right = node
                    break
    return root


def random_voyage(t, out):
    if t is not None:
        out.append(t.val)
        if next_random() % 2 == 0:
            random_voyage(t.left, out)
            random_voyage(t.right, out)
        else:
            random_voyage(t.right, out)
            random_voyage(t.left, out)


def main():
    sys.setrecursionlimit(10000)
    rounds, count = 1000, 200
    trees, voyages = [], []
    for c in range(count):
        root = random_tree(random_permutation(100))
        voyage = []
        random_voyage(root, voyage)
        if c % 4 == 3:
            i = next_random() % 100
            j = next_random() % 100
            voyage[i], voyage[j] = voyage[j], voyage[i]
        trees.append(root)
        voyages.append(voyage)
    flips = check = 0
    for r in range(rounds):
        for s in range(count):
            c = (r + s) % count
            for v in flip_match_voyage(trees[c], voyages[c]):
                flips += 1
                check = (check * 31 + v + 2) % 1000000007
    print(f"{rounds} rounds over {count} trees of 100 nodes: {flips} values, checksum {check}")


main()
