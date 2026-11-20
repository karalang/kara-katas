# LeetCode #1740: Find Distance in a Binary Tree -- the bench
# (distance.kara in Python): the lowest common ancestor, then depths.

import sys

from collections import deque

sys.setrecursionlimit(100000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def find_distance(root, p, q):
    ancestor = common(root, p, q)
    return depth(ancestor, p) + depth(ancestor, q)


def common(node, p, q):
    if node is None:
        return None
    if node.val == p or node.val == q:
        return node
    left = common(node.left, p, q)
    right = common(node.right, p, q)
    if left is not None and right is not None:
        return node
    return left if left is not None else right


def depth(node, value):
    if node is None:
        return -1
    if node.val == value:
        return 0
    below = max(depth(node.left, value), depth(node.right, value))
    return -1 if below < 0 else below + 1


def from_level(values):
    root = TreeNode(values[0])
    waiting = deque([root])
    i = 1
    while i < len(values):
        parent = waiting.popleft()
        if values[i] is not None:
            child = TreeNode(values[i])
            parent.left = child
            waiting.append(child)
        i += 1
        if i < len(values):
            if values[i] is not None:
                child = TreeNode(values[i])
                parent.right = child
                waiting.append(child)
            i += 1
    return root


seed = 1740


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n):
    values = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = []
    for i in range(n):
        node = TreeNode(values[i])
        if i > 0:
            at = nodes[next_random() % i]
            while True:
                if next_random() % 2 == 0:
                    if at.left is not None:
                        at = at.left
                    else:
                        at.left = node
                        break
                else:
                    if at.right is not None:
                        at = at.right
                    else:
                        at.right = node
                        break
        nodes.append(node)
    return nodes


n, queries, rounds = 10000, 1000, 4
nodes = random_tree(n)
root = nodes[0]
pairs = [(next_random() % n, next_random() % n) for _ in range(queries)]
total = 0
check = 0
for r in range(rounds):
    for p, q in pairs:
        found = find_distance(root, p, q)
        total += found
        check = (check * 31 + found + r) % 1000000007
print(f"{n} nodes, {queries} pairs, {rounds} rounds: distances sum to {total}, checksum {check}")
