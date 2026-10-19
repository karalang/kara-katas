# LeetCode 776 — Split BST: Python mirror of the ★ arm (recursive), with
# the same harness.
from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def split_bst(root, target):
    if root is None:
        return None, None
    if root.val <= target:
        small, large = split_bst(root.right, target)
        root.right = small
        return root, large
    small, large = split_bst(root.left, target)
    root.left = large
    return small, root


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def insert(root, v):
    fresh = TreeNode(v)
    if root is None:
        return fresh
    node = root
    while True:
        if v < node.val:
            if node.left is None:
                node.left = fresh
                break
            node = node.left
        else:
            if node.right is None:
                node.right = fresh
                break
            node = node.right
    return root


def tree_of(values):
    root = None
    for v in values:
        root = insert(root, v)
    return root


def level_order(root):
    items = []
    queue = deque([root])
    while queue:
        slot = queue.popleft()
        if slot is None:
            items.append("null")
        else:
            items.append(str(slot.val))
            queue.append(slot.left)
            queue.append(slot.right)
    while items and items[-1] == "null":
        items.pop()
    return "[" + ",".join(items) + "]"


def show(values, target):
    before = level_order(tree_of(values))
    small, large = split_bst(tree_of(values), target)
    print(f"{before}, target = {target} -> {level_order(small)} {level_order(large)}")


def main():
    show([4, 2, 6, 1, 3, 5, 7], 2)
    show([1], 1)
    show([1], 0)
    show([5, 3, 8, 1, 4, 7, 9, 2, 6], 4)
    show([5, 3, 8, 1, 4, 7, 9, 2, 6], 6)
    show([5, 3, 8, 1, 4, 7, 9, 2, 6], 0)
    show([5, 3, 8, 1, 4, 7, 9, 2, 6], 9)
    show([1, 2, 3, 4, 5, 6, 7, 8], 4)
    show([8, 7, 6, 5, 4, 3, 2, 1], 4)
    show([10, 1, 20, 2, 19, 3, 18, 4, 17], 10)
    seed = [776]
    check = 0
    small_nodes = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 50
        used = set()
        values = []
        while len(values) < n:
            v = next_random(seed) % 1001
            if v not in used:
                used.add(v)
                values.append(v)
        target = next_random(seed) % 1001
        small, large = split_bst(tree_of(values), target)
        text = f"{level_order(small)}|{level_order(large)}"
        for b in text.encode():
            check = (check * 31 + b) % 1000000007
        small_nodes += sum(1 for v in values if v <= target)
    print(f"300 random trees: {small_nodes} nodes in the small trees, checksum {check}")


main()
