# LeetCode #1676: Lowest Common Ancestor of a Binary Tree IV -- the Python
# mirror of the ★ arm: #236's search widened to a set of nodes.

import sys
from collections import deque

sys.setrecursionlimit(100000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def lowest_common_ancestor(root, nodes):
    wanted = {n.val for n in nodes}

    def search(node):
        if node is None:
            return None
        if node.val in wanted:
            return node
        left = search(node.left)
        right = search(node.right)
        if left is not None and right is not None:
            return node
        return left if left is not None else right

    return search(root)


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


seed = 1676


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


def answer(root, nodes):
    return lowest_common_ancestor(root, nodes).val


def at_values(root, values):
    found = []
    for v in values:
        stack = [root]
        while stack:
            node = stack.pop()
            if node.val == v:
                found.append(node)
                break
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)
    return found


def batch(count, most):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % most + 1
        nodes = random_tree(n)
        root = nodes[0]
        for _ in range(5):
            k = next_random() % min(n, 20) + 1
            for i in range(k):
                j = i + next_random() % (n - i)
                nodes[i], nodes[j] = nodes[j], nodes[i]
            found = answer(root, nodes[:k])
            total += found
            check = (check * 31 + found + k) % 1000000007
    print(f"{count} trees of up to {most} nodes: answers sum to {total}, checksum {check}")


example = from_level([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
print(answer(example, at_values(example, [4, 7])))
print(answer(example, at_values(example, [1])))
print(answer(example, at_values(example, [7, 6, 2, 4])))
print(answer(example, at_values(example, [0, 1, 2, 3, 4, 5, 6, 7, 8])))
print(answer(example, at_values(example, [6, 4])))
single = from_level([1])
print(answer(single, at_values(single, [1])))
batch(3000, 8)
batch(300, 1000)
batch(30, 10000)
