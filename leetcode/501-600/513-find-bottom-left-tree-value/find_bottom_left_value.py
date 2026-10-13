# LeetCode #513: Find Bottom Left Tree Value -- level by level. Mirrors
# find_bottom_left_value.kara (the star arm) and its harness.

from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def find_bottom_left_value(root):
    queue = deque([root])
    leftmost = root.val
    while queue:
        leftmost = queue[0].val
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
    return leftmost


# ---- test harness ---------------------------------------------------------

seed = 513


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(items):
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
    print(f"{name}: {find_bottom_left_value(from_level_order(items))}")


def main():
    show("example 1", [2, 1, 3])
    show("example 2", [1, 2, 3, 4, None, 5, 6, None, None, 7])
    show("one node", [-7])
    show("only a right child", [1, None, 2])
    show("the bottom row on the right", [1, 2, 3, None, None, 4, 5])
    show("a zigzag", [1, 2, None, None, 3, 4, None, None, 5])
    show("the extremes", [2147483647, -2147483648, 2147483647, None, -2147483648])
    count = 300
    total = 0
    checksum = 0
    for t in range(count):
        half = 2 if t % 3 == 0 else 1000 if t % 3 == 1 else 0
        size = 1 + next_random() % 60
        total += size
        v = find_bottom_left_value(grow(size, half))
        checksum = (checksum * 31 + v + 2147483648) % 1000000007
    print(f"{count} random trees: {total} nodes, checksum {checksum}")


main()
