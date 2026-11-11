# LeetCode #1120: Maximum Average Subtree -- the bench in Python, the ★ arm
# over objects with `__slots__`, the same 16 trees and 200 rounds.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(node, best):
    if node is None:
        return 0, 0
    ls, lc = walk(node.left, best)
    rs, rc = walk(node.right, best)
    s = ls + rs + node.val
    c = lc + rc + 1
    a = s / c
    if a > best[0]:
        best[0] = a
    return s, c


def maximum_average_subtree(root):
    best = [0.0]
    walk(root, best)
    return best[0]


seed = 1120


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_value():
    hi = next_random()
    lo = next_random()
    return (hi * 32768 + lo) % 100001


def random_tree():
    nodes = [TreeNode(random_value())]
    for _ in range(1, 10000):
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
    return nodes


def main():
    trees = [random_tree() for _ in range(16)]
    total = 0.0
    check = 0
    for rnd in range(200):
        for j in range(len(trees)):
            at = (rnd * 7919 + j * 104729) % 10000
            n = trees[j][at]
            n.val = (n.val * 7 + rnd) % 100001
            answer = maximum_average_subtree(trees[j][0])
            total += answer
            check = (check * 31 + int(answer * 1000.0)) % 1000000007
    print(f"200 rounds over 16 trees of 10^4 nodes: answers total {total:.3f}, checksum {check}")


main()
