# LeetCode #1028: Recover a Tree From Preorder Traversal -- a stack of the path
# Mirrors recover_tree.kara (the ★ arm) and prints the same output.

import sys
from collections import deque

sys.setrecursionlimit(20000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def recover_from_preorder(traversal):
    path = []
    i = 0
    n = len(traversal)
    while i < n:
        depth = 0
        while traversal[i] == "-":
            depth += 1
            i += 1
        value = 0
        while i < n and traversal[i] != "-":
            value = value * 10 + ord(traversal[i]) - 48
            i += 1
        node = TreeNode(value)
        while len(path) > depth:
            path.pop()
        if path:
            parent = path[-1]
            if parent.left is None:
                parent.left = node
            else:
                parent.right = node
        path.append(node)
    return path[0] if path else None


seed = 1028


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_value(top):
    high = next_random()
    return (high * 32768 + next_random()) % top + 1


def random_tree(n, top):
    root = TreeNode(random_value(top))
    placed = 1
    while placed < n:
        leaf = TreeNode(random_value(top))
        node = root
        while True:
            if node.left is None:
                node.left = leaf
                break
            if next_random() % 2 == 0:
                node = node.left
            elif node.right is None:
                node.right = leaf
                break
            else:
                node = node.right
        placed += 1
    return root


def traversal(node, depth, out):
    if node is not None:
        out.append("-" * depth + str(node.val))
        traversal(node.left, depth + 1, out)
        traversal(node.right, depth + 1, out)


def level_order(root):
    items = []
    queue = deque([root])
    while queue:
        entry = queue.popleft()
        if entry is None:
            items.append("null")
        else:
            items.append(str(entry.val))
            queue.append(entry.left)
            queue.append(entry.right)
    while items and items[-1] == "null":
        items.pop()
    return "[" + ",".join(items) + "]"


def main():
    examples = [
        "1-2--3--4-5--6--7",
        "1-2--3---4-5--6---7",
        "1-401--349---90--88",
        "7",
        "10-20",
        "1-2--3---4----5",
        "1000000000-1--1000000000-999999999",
    ]
    for s in examples:
        print(f"{s} -> {level_order(recover_from_preorder(s))}")
    groups = [(2000, 5, 9), (1000, 20, 100), (300, 100, 1000000000), (100, 300, 5), (20, 1000, 1000000000), (2, 1000, 1)]
    for count, n, top in groups:
        exact = 0
        letters = 0
        check = 0
        for _ in range(count):
            tree = random_tree(n, top)
            parts = []
            traversal(tree, 0, parts)
            s = "".join(parts)
            letters += len(s)
            back = level_order(recover_from_preorder(s))
            if back == level_order(tree):
                exact += 1
            for b in back.encode():
                check = (check * 131 + b) % 1000000007
        print(f"{count} trees of {n} nodes (values up to {top}), {letters} letters: {exact} recovered exactly, checksum {check}")


main()
