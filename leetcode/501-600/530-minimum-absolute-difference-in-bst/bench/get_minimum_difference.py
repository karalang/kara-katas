# Benchmark for #530: Python mirror of the ★ arm (in-order,
# recursively); see get_minimum_difference.kara.
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
        self.prev = None
        self.best = 2**63 - 1


def visit(node, walk):
    if node is None:
        return
    visit(node.left, walk)
    if walk.prev is not None:
        walk.best = min(walk.best, node.val - walk.prev)
    walk.prev = node.val
    visit(node.right, walk)


def get_minimum_difference(root):
    walk = Walk()
    visit(root, walk)
    return walk.best


seed = 530


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
    # 100 random search trees of 10,000 different values, drawn from 0
    # to 10,000, 0 to 20,000, ... up to 0 to 100,000 in turn, built once.
    # Then the answer for each tree is found 50 times.
    trees = 100
    all_trees = []
    for t in range(trees):
        rng = 10000 * (1 + t % 10) + 1
        pool = list(range(rng))
        for i in range(10000):
            high = next_random()
            j = i + (high * 32768 + next_random()) % (rng - i)
            pool[i], pool[j] = pool[j], pool[i]
        all_trees.append(build(pool[:10000]))
    total = 0
    checksum = 0
    for _ in range(50):
        for t in range(trees):
            answer = get_minimum_difference(all_trees[t])
            total += answer
            checksum = (checksum * 31 + answer) % 1000000007
    print(f"{trees} trees of 10000 values, 50 times each: total {total}, checksum {checksum}")


main()
