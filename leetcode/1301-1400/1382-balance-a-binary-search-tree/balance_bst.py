# LeetCode #1382: Balance a Binary Search Tree -- Python mirror of the ★
# arm: the values read off in order, then a new tree built with the
# middle value at the root and each half built the same way beneath it.

import sys
from collections import deque

sys.setrecursionlimit(100000)

seed = 1382


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def values_in_order(node, values):
    if node:
        values_in_order(node.left, values)
        values.append(node.val)
        values_in_order(node.right, values)


def build(values, lo, hi):
    if lo >= hi:
        return None
    mid = (lo + hi) // 2
    return TreeNode(values[mid], build(values, lo, mid), build(values, mid + 1, hi))


def balance_bst(root):
    values = []
    values_in_order(root, values)
    return build(values, 0, len(values))


def from_level(values):
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while i < len(values):
        if not queue:
            break
        node = queue.popleft()
        if values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


def search_tree(values):
    root = TreeNode(values[0])
    for v in values[1:]:
        at = root
        while True:
            nxt = at.left if v < at.val else at.right
            if nxt:
                at = nxt
            else:
                if v < at.val:
                    at.left = TreeNode(v)
                else:
                    at.right = TreeNode(v)
                break
    return root


def chain(values):
    root = TreeNode(values[0])
    at = root
    for v in values[1:]:
        nxt = TreeNode(v)
        if v < at.val:
            at.left = nxt
        else:
            at.right = nxt
        at = nxt
    return root


def in_order(node, out):
    values_in_order(node, out)


def balanced_height(node):
    if not node:
        return 0
    lh = balanced_height(node.left)
    rh = balanced_height(node.right)
    if lh < 0 or rh < 0 or abs(lh - rh) > 1:
        return -1
    return 1 + max(lh, rh)


def verdict(root):
    before = []
    in_order(root, before)
    balanced = balance_bst(root)
    after = []
    in_order(balanced, after)
    if after != before:
        return -1
    return balanced_height(balanced)


def main():
    examples = [
        [1, None, 2, None, 3, None, 4],
        [2, 1, 3],
        [5],
        [7, 6, None, 5, None, 4, None, 3, None, 2, None, 1],
        [1, None, 6, 2, None, None, 5, 3, None, None, 4],
        [4, 2, 6, 1, 3, 5, 7],
    ]
    print(" ".join(str(verdict(from_level(e))) for e in examples))
    up = TreeNode(1)
    top = up
    for v in range(2, 10001):
        top.right = TreeNode(v)
        top = top.right
    down = TreeNode(10000)
    top = down
    for v in range(9999, 0, -1):
        top.left = TreeNode(v)
        top = top.left
    print(f"chains of 10000 nodes: heights {verdict(up)} {verdict(down)}")
    balanced = 0
    heights = 0
    check = 0
    for c in range(2000):
        n = 1 + next_random() % 300
        step = 1 + next_random() % 99990
        start = next_random() % 99991
        values = [1 + (start + k * step) % 99991 for k in range(n)]
        kind = c % 4
        if kind == 0:
            for i in range(n - 1, 0, -1):
                j = next_random() % (i + 1)
                values[i], values[j] = values[j], values[i]
        elif kind == 1:
            values.sort()
        elif kind == 2:
            values.sort()
            values.reverse()
        else:
            values.sort()
            values = [values[k // 2] if k % 2 == 0 else values[n - 1 - k // 2] for k in range(n)]
        root = search_tree(values) if kind == 0 else chain(values)
        h = verdict(root)
        if h >= 0:
            balanced += 1
            heights += h
        check = (check * 131 + h + 1) % 1000000007
    print(f"2000 random trees: {balanced} balanced, heights {heights} in all, checksum {check}")


main()
