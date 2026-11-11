# LeetCode #1123: Lowest Common Ancestor of Deepest Leaves -- the bench, the
# same workload as lca_deepest_leaves.kara: the one-walk solution over 16
# trees of 10^4 nodes, built once, each round hanging one more node on every
# tree and solving it again.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(node):
    if node is None:
        return 0, None
    ld, la = walk(node.left)
    rd, ra = walk(node.right)
    if ld == rd:
        return ld + 1, node
    if ld > rd:
        return ld + 1, la
    return rd + 1, ra


def lca_deepest_leaves(root):
    return walk(root)[1]


seed = 1123


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_value():
    a = next_random()
    b = next_random()
    return (a * 32768 + b) % 100001


def grow(nodes):
    c = TreeNode(random_value())
    while True:
        at = nodes[next_random() % len(nodes)]
        if next_random() % 2 == 0:
            if at.left is None:
                at.left = c
                break
        elif at.right is None:
            at.right = c
            break
    nodes.append(c)


def main():
    trees = []
    for _ in range(16):
        nodes = [TreeNode(random_value())]
        for _ in range(1, 10000):
            grow(nodes)
        trees.append(nodes)
    total = 0
    check = 0
    for _ in range(200):
        for nodes in trees:
            grow(nodes)
            answer = lca_deepest_leaves(nodes[0])
            total += answer.val
            check = (check * 31 + answer.val) % 1000000007
    print(f"200 rounds over 16 trees of 10^4 nodes: answers total {total}, checksum {check}")


main()
