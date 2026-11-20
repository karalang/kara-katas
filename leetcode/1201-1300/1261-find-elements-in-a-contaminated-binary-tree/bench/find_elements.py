# LeetCode #1261 bench, in Python: the ★ arm (the tree recovered from the
# root down, every value kept in a hash set) on 20 random contaminated trees
# of 10000 nodes, at most 20 levels deep, built once; 120 rounds, each tree
# recovered again and asked 10000 targets, half of them nodes' places;
# the targets found counted and folded into a checksum.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def recover(node, value, values):
    if node:
        node.val = value
        values.add(value)
        recover(node.left, 2 * value + 1, values)
        recover(node.right, 2 * value + 2, values)


class FindElements:
    def __init__(self, root):
        self.values = set()
        recover(root, 0, self.values)

    def find(self, target):
        return target in self.values


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def build(present, at):
    if at not in present:
        return None
    return TreeNode(-1, build(present, 2 * at + 1), build(present, 2 * at + 2))


def random_places(n, rng):
    places = [0]
    present = {0}
    while len(places) < n:
        p = places[rng.next() % len(places)]
        child = 2 * p + 1 + rng.next() % 2
        if child < 2097151 and child not in present:
            present.add(child)
            places.append(child)
    return present


def main():
    rng = Rng(1261)
    trees = []
    targets = []
    for _ in range(20):
        present = random_places(10000, rng)
        places = sorted(present)
        deepest = places[-1]
        trees.append(build(present, 0))
        targets.append([places[rng.next() % 10000] if q % 2 == 0 else rng.next() * 64 % (deepest + 1) for q in range(10000)])
    found = 0
    check = 0
    for _ in range(120):
        for t in range(20):
            tree = FindElements(trees[t])
            for target in targets[t]:
                if tree.find(target):
                    found += 1
                    check = (check * 131 + target) % 1000000007
    print(f"120 rounds of 20 trees of 10000 nodes: {found} found, checksum {check}")


main()
