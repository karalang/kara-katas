# LeetCode #637: Average of Levels in Binary Tree -- Python mirror of the
# ★ arm.
#
# Breadth first with a deque, one level at a time.
from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def average_of_levels(root):
    averages = []
    queue = deque([root] if root else [])
    while queue:
        count = len(queue)
        total = 0
        for _ in range(count):
            node = queue.popleft()
            total += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        averages.append(total / count)
    return averages


seed = 637


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(values):
        n = queue[head]
        head += 1
        if values[i] is not None:
            n.left = TreeNode(values[i])
            queue.append(n.left)
        i += 1
        if i < len(values):
            if values[i] is not None:
                n.right = TreeNode(values[i])
                queue.append(n.right)
            i += 1
    return root


def random_value():
    high = next_random() % 65536
    low = next_random() % 65536
    return high * 65536 + low - 2147483648


def random_tree(size, lean, wide):
    root = None
    for _ in range(size):
        c = TreeNode(random_value() if wide else next_random() % 201 - 100)
        if root is None:
            root = c
            continue
        node = root
        while True:
            if next_random() % 100 < lean:
                if node.left:
                    node = node.left
                else:
                    node.left = c
                    break
            else:
                if node.right:
                    node = node.right
                else:
                    node.right = c
                    break
    return root


def show(values):
    averages = average_of_levels(from_level(values))
    text = "[" + ", ".join(f"{a:.5f}" for a in averages) + "]"
    print(f"{len(values)} values -> {text}")


show([3, 9, 20, None, None, 15, 7])
show([3, 9, 20, 15, 7])
show([-7])
show([1, 2, None, 3, None, 4])
show([0, -1, 0, -3, 1])
show([5, 2147483647, -2147483648, 1, None, None, 2])
show([-2147483648, 2147483647, 2147483647])
show([])
levels = 0
total = 0.0
for _ in range(300):
    leans = [20, 50, 80]
    size = 1 + next_random() % 40
    lean = leans[next_random() % 3]
    for a in average_of_levels(random_tree(size, lean, False)):
        levels += 1
        total += a
print(f"300 random trees: {levels} levels, sum of averages {total:.4f}")
averages = average_of_levels(random_tree(10000, 50, True))
s = 0.0
low = averages[0]
for a in averages:
    s += a
    if a < low:
        low = a
print(f"10000 nodes: {len(averages)} levels, sum of averages {s:.3f}, lowest {low:.3f}")
