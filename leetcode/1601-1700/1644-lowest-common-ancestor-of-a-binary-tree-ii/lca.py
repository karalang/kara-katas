# LeetCode #1644: Lowest Common Ancestor of a Binary Tree II -- the Python
# mirror of the ★ arm: one walk counting how many of p and q each subtree
# holds, the first node to count both the answer.

import sys
from collections import deque

sys.setrecursionlimit(100000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def lowest_common_ancestor(root, p, q):
    found = [None]

    def count_below(node):
        if node is None:
            return 0
        here = 1 if node.val == p.val or node.val == q.val else 0
        count = count_below(node.left) + count_below(node.right) + here
        if count == 2 and found[0] is None:
            found[0] = node
        return count

    count_below(root)
    return found[0]


# ---- the harness: the same as every arm's ---------------------------------


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


seed = 1644


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
    return nodes[0]


def answer(root, p, q):
    node = lowest_common_ancestor(root, TreeNode(p), TreeNode(q))
    return -1 if node is None else node.val


def batch(count, most):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % most + 1
        root = random_tree(n)
        rng = n + n // 4 + 1
        for _ in range(5):
            p = next_random() % rng
            q = next_random() % rng
            if q == p:
                q = (q + 1) % rng
            found = answer(root, p, q)
            total += found + 1
            check = (check * 31 + found + 2) % 1000000007
    print(f"{count} trees of up to {most} nodes: answers sum to {total}, checksum {check}")


example = from_level([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
print(answer(example, 5, 1))
print(answer(example, 5, 4))
print(answer(example, 5, 10))
print(answer(example, 3, 7))
print(answer(from_level([1, 2, None, 3]), 3, 2))
print(answer(example, 11, 12))
batch(3000, 8)
batch(300, 1000)
batch(30, 10000)
