# Benchmark for #501: Python mirror of the ★ arm (in-order with a
# running count); see find_mode.kara.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Walk:
    def __init__(self):
        self.prev = 0
        self.run = 0
        self.best = 0
        self.modes = []


def visit(node, walk):
    if node is None:
        return
    visit(node.left, walk)
    if walk.run > 0 and node.val == walk.prev:
        walk.run += 1
    else:
        walk.prev = node.val
        walk.run = 1
    if walk.run > walk.best:
        walk.best = walk.run
        walk.modes.clear()
        walk.modes.append(node.val)
    elif walk.run == walk.best:
        walk.modes.append(node.val)
    visit(node.right, walk)


def find_mode(root):
    walk = Walk()
    visit(root, walk)
    return walk.modes


seed = 501


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(values):
    root = TreeNode(values[0])
    for v in values[1:]:
        node = root
        while True:
            if v < node.val or (v == node.val and next_random() % 2 == 0):
                if node.left is not None:
                    node = node.left
                else:
                    node.left = TreeNode(v)
                    break
            else:
                if node.right is not None:
                    node = node.right
                else:
                    node.right = TreeNode(v)
                    break
    return root


def main():
    # 100 random search trees of 10,000 values, drawn from 1 to 10
    # values, 1,000 values, or the whole range -100,000 to 100,000 in
    # turn, built once. Then the modes of each tree are found 30 times.
    trees = 100
    all_trees = []
    for t in range(trees):
        if t % 3 == 0:
            rng = 1 + next_random() % 10
        elif t % 3 == 1:
            rng = 1000
        else:
            rng = 200001
        values = []
        for _ in range(10000):
            v = next_random() * 7 % rng
            values.append(v - 100000 if rng == 200001 else v)
        all_trees.append(build(values))
    modes = 0
    checksum = 0
    for _ in range(30):
        for t in range(trees):
            for m in find_mode(all_trees[t]):
                modes += 1
                checksum = (checksum * 31 + m + 100000) % 1000000007
    print(f"{trees} trees of 10000 values, 30 times each: {modes} modes, checksum {checksum}")


main()
