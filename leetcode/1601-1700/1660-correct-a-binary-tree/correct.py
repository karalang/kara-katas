# LeetCode #1660: Correct a Binary Tree -- Python mirror of correct.kara.
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


def from_level_order(items):
    root = TreeNode(items[0])
    queue = deque([root])
    i = 1
    while i < len(items):
        node = queue.popleft()
        for side in range(2):
            if i < len(items):
                v = items[i]
                if v is not None:
                    child = TreeNode(v)
                    if side == 0:
                        node.left = child
                    else:
                        node.right = child
                    queue.append(child)
                i += 1
    return root


def find(root, val):
    stack = [root]
    while stack:
        node = stack.pop()
        if node.val == val:
            return node
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)
    raise ValueError("no such node")


def written(root):
    items = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            items.append("null")
        else:
            items.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
    while items and items[-1] == "null":
        items.pop()
    return "[" + ",".join(items) + "]"


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


def batch(count, most):
    check = 0
    kept = 0
    for _ in range(count):
        while True:
            n = big() % (most - 2) + 3
            root = random_tree(n)
            if break_tree(root) is not None:
                break
        c, check = fold(correct_binary_tree(root), check)
        kept += c
    print(f"{count} trees of up to {most} nodes: {kept} nodes kept, checksum {check}")


def main():
    global seed
    examples = [
        ([1, 2, 3], 2, 3),
        ([8, 3, 1, 7, None, 9, 4, 2, None, None, None, 5, 6], 7, 4),
        ([1, 2, 3, 4, None, None, 5], 4, 5),
        ([1, 2, 3, 4, None, 5, 6], 2, 3),
        ([1, 2, 3, 4, 5, 6, 7], 4, 7),
    ]
    for items, frm, to in examples:
        root = from_level_order(items)
        find(root, frm).right = find(root, to)
        print(written(correct_binary_tree(root)))
    seed = 1660
    batch(3000, 8)
    batch(300, 1000)
    batch(30, 100000)


main()
