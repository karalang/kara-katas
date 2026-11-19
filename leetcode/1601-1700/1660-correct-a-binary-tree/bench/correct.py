# LeetCode #1660: Correct a Binary Tree -- the bench's Python mirror: the
# ★ arm on 40 random trees of 100000 nodes, each broken once, all built
# first.
#
# A preorder walk, right before left, keeping the values met in a set;
# the first node whose right child is already in the set is the bad one.

import sys
from collections import deque

sys.setrecursionlimit(1 << 20)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def correct(node, seen):
    if node is None:
        return None
    if node.right is not None and node.right.val in seen:
        return None
    seen.add(node.val)
    node.right = correct(node.right, seen)
    node.left = correct(node.left, seen)
    return node


def correct_binary_tree(root):
    return correct(root, set())


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def big():
    a = next_random()
    return a * 32768 + next_random()


def random_tree(n):
    values = list(range(n))
    for i in range(n - 1, 0, -1):
        j = big() % (i + 1)
        values[i], values[j] = values[j], values[i]
    root = TreeNode(values[0])
    free = [(root, True), (root, False)]
    for i in range(1, n):
        k = big() % len(free)
        free[k], free[-1] = free[-1], free[k]
        parent, left = free.pop()
        child = TreeNode(values[i])
        if left:
            parent.left = child
        else:
            parent.right = child
        free.append((child, True))
        free.append((child, False))
    return root


def break_tree(root):
    pairs = 0
    level = [root]
    levels = []
    while level:
        below = []
        for i, node in enumerate(level):
            if node.right is None:
                pairs += len(level) - 1 - i
            if node.left is not None:
                below.append(node.left)
            if node.right is not None:
                below.append(node.right)
        levels.append(level)
        level = below
    if pairs == 0:
        return None
    k = big() % pairs
    for level in levels:
        for i, node in enumerate(level):
            if node.right is None:
                after = len(level) - 1 - i
                if k < after:
                    to = level[i + 1 + k]
                    node.right = to
                    return (node.val, to.val)
                k -= after
    return None


def fold(root, check):
    count = 0
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            check = mix(check, 0)
        else:
            count += 1
            check = mix(check, node.val + 1)
            queue.append(node.left)
            queue.append(node.right)
    return count, check


def main():
    global seed
    seed = 1660
    roots = []
    while len(roots) < 40:
        root = random_tree(100000)
        if break_tree(root) is not None:
            roots.append(root)
    check = 0
    kept = 0
    for root in roots:
        c, check = fold(correct_binary_tree(root), check)
        kept += c
    print(f"40 trees of 100000 nodes: {kept} nodes kept, checksum {check}")


main()
