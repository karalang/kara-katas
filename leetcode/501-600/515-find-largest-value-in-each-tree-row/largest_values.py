# LeetCode #515: Find Largest Value in Each Tree Row -- level by level.
# Mirrors largest_values.kara (the star arm) and its harness.

from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def largest_values(root):
    largest = []
    queue = deque()
    if root is not None:
        queue.append(root)
    while queue:
        best = -(2**63)
        for _ in range(len(queue)):
            node = queue.popleft()
            best = max(best, node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        largest.append(best)
    return largest


# ---- test harness ---------------------------------------------------------

seed = 515


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(items):
    if not items:
        return None
    root = TreeNode(items[0])
    queue = deque([root])
    i = 1
    while i < len(items):
        node = queue.popleft()
        if items[i] is not None:
            child = TreeNode(items[i])
            node.left = child
            queue.append(child)
        i += 1
        if i < len(items):
            if items[i] is not None:
                child = TreeNode(items[i])
                node.right = child
                queue.append(child)
            i += 1
    return root


def draw(half):
    if half == 0:
        a = next_random()
        b = next_random()
        c = next_random()
        return a * 65536 + b * 2 + c % 2 - 2147483648
    return next_random() % (2 * half + 1) - half


def grow(size, half):
    if size == 0:
        return None
    root = TreeNode(draw(half))
    for _ in range(1, size):
        leaf = TreeNode(draw(half))
        node = root
        while True:
            if next_random() % 2 == 0:
                if node.left is not None:
                    node = node.left
                else:
                    node.left = leaf
                    break
            else:
                if node.right is not None:
                    node = node.right
                else:
                    node.right = leaf
                    break
    return root


def show(name, items):
    row = largest_values(from_level_order(items))
    print(f"{name}: [{', '.join(str(v) for v in row)}]")


def main():
    show("example 1", [1, 3, 2, 5, 3, None, 9])
    show("example 2", [1, 2, 3])
    show("the empty tree", [])
    show("one node", [-7])
    show("all negative", [-1, -5, -3, -9, None, None, -4])
    show("a zigzag", [1, 2, None, None, 3, 4, None, None, 5])
    show("the extremes", [-2147483648, -2147483648, 2147483647, None, -2147483648])
    count = 300
    rows = 0
    checksum = 0
    for t in range(count):
        half = 2 if t % 3 == 0 else 1000 if t % 3 == 1 else 0
        size = next_random() % 61
        row = largest_values(grow(size, half))
        rows += len(row)
        for v in row:
            checksum = (checksum * 31 + v + 2147483648) % 1000000007
    print(f"{count} random trees: {rows} rows, checksum {checksum}")


main()
