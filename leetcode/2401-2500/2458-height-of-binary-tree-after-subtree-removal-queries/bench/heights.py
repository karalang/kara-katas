# LeetCode #2458: Height of Binary Tree After Subtree Removal Queries --
# the bench, the ★ arm in Python: every subtree's height, then a walk
# down carrying the height the tree keeps without each node. The nodes
# are objects with `__slots__`.

import sys

sys.setrecursionlimit(10000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def height(node, heights):
    if node is None:
        return -1
    h = 1 + max(height(node.left, heights), height(node.right, heights))
    heights[node.val] = h
    return h


def of(node, heights):
    return -1 if node is None else heights[node.val]


def walk(node, depth, rest, heights, answers):
    if node is not None:
        answers[node.val] = rest
        walk(node.left, depth + 1, max(rest, depth + 1 + of(node.right, heights)), heights, answers)
        walk(node.right, depth + 1, max(rest, depth + 1 + of(node.left, heights)), heights, answers)


def tree_queries(root, queries):
    heights = {}
    height(root, heights)
    answers = {}
    walk(root, 0, 0, heights, answers)
    return [answers[q] for q in queries]


seed = 2458


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n):
    values = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = [TreeNode(v) for v in values]
    for k in range(1, n):
        high = next_random()
        at = nodes[(high * 32768 + next_random()) % k]
        while True:
            if next_random() % 2 == 0:
                if at.left is not None:
                    at = at.left
                else:
                    at.left = nodes[k]
                    break
            else:
                if at.right is not None:
                    at = at.right
                else:
                    at.right = nodes[k]
                    break
    return nodes[0]


def main():
    # 20 random trees of 10^4 nodes built once; then 60 passes, each
    # asking every tree about every value but the root's, pass p starting
    # its queries p * 101 values along
    n = 10000
    trees = [random_tree(n) for _ in range(20)]
    check = 0
    for p in range(60):
        for root in trees:
            r = root.val
            queries = [v for v in (1 + (i + p * 101) % n for i in range(n)) if v != r]
            for a in tree_queries(root, queries):
                check = (check * 31 + a + p) % 1000000007
    print(f"60 passes over 20 trees of 10^4: checksum {check}")


main()
