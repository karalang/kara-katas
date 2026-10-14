# LeetCode #637: Average of Levels in Binary Tree -- benchmark, Python.
#
# The ★ arm: breadth first with a deque, one level at a time.
from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def average_of_levels(root):
    averages = []
    queue = deque([root] if root else [])
    while queue:
        count = len(queue)
        total = 0
        for _ in range(count):
            node = queue.popleft()
            total += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        averages.append(total / count)
    return averages


seed = 637


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_value():
    high = next_random() % 65536
    low = next_random() % 65536
    return high * 65536 + low - 2147483648


def random_tree(size):
    root = None
    for _ in range(size):
        c = TreeNode(random_value())
        if root is None:
            root = c
            continue
        node = root
        while True:
            if next_random() % 2 == 0:
                if node.left:
                    node = node.left
                else:
                    node.left = c
                    break
            else:
                if node.right:
                    node = node.right
                else:
                    node.right = c
                    break
    return root


def main():
    trees = [random_tree(10000) for _ in range(10)]
    levels = 0
    total = 0.0
    for r in range(4000):
        for a in average_of_levels(trees[r % 10]):
            levels += 1
            total += a
    print(f"10 trees of 10000 nodes, 4000 rounds: {levels} levels, sum of averages {total:.3f}")


main()
