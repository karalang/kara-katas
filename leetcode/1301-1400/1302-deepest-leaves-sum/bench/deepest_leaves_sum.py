# LeetCode #1302 bench in Python: the ★ arm (a breadth-first walk a level at
# a time from a `collections.deque`) on the same 50 trees of 10^4 nodes and
# 50 passes.
from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def deepest_leaves_sum(root):
    queue = deque()
    if root is not None:
        queue.append(root)
    total = 0
    while queue:
        total = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            total += node.val
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
    return total


seed = 1302


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(n, level_order):
    root = TreeNode(1 + next_random() % 100)
    nodes = [root]
    if level_order:
        level = deque([root])
        while len(nodes) < n:
            at = level.popleft()
            for side in range(2):
                if len(nodes) < n and next_random() % 4 != 0:
                    node = TreeNode(1 + next_random() % 100)
                    if side == 0:
                        at.left = node
                    else:
                        at.right = node
                    level.append(node)
                    nodes.append(node)
            if not level:
                level.append(at)
    else:
        places = [(root, True), (root, False)]
        while len(nodes) < n:
            k = next_random() % len(places)
            parent, left = places[k]
            places[k] = places[-1]
            places.pop()
            node = TreeNode(1 + next_random() % 100)
            if left:
                parent.left = node
            else:
                parent.right = node
            places.append((node, True))
            places.append((node, False))
            nodes.append(node)
    return nodes


def main():
    n = 10000
    trees = [build(n, t % 2 == 1) for t in range(50)]
    check = 0
    for p in range(50):
        for t in range(50):
            nodes = trees[t]
            nodes[check % n].val = 1 + (check // 7) % 100
            s = deepest_leaves_sum(nodes[0])
            check = (check * 31 + s + p) % 1000000007
    print(f"50 passes over 50 trees of 10^4: checksum {check}")


main()
