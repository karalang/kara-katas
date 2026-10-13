# Benchmark for #513: Python mirror of the ★ arm (level by level); see
# find_bottom_left_value.kara. The queue is a fresh deque for every call.
from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


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


# ---- benchmark --------------------------------------------------------------

seed = 513


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(values, lo, hi):
    if lo >= hi:
        return None
    mid = lo + next_random() % (hi - lo)
    left = build(values, lo, mid)
    right = build(values, mid + 1, hi)
    return TreeNode(values[mid], left, right)


def main():
    # 100 random trees of 10,000 nodes, the values from the whole range
    # -2^31 to 2^31 - 1, built once. Then each is solved 50 times.
    trees = 100
    all_trees = []
    for _ in range(trees):
        values = []
        for _ in range(10000):
            a = next_random()
            b = next_random()
            c = next_random()
            values.append(a * 65536 + b * 2 + c % 2 - 2147483648)
        all_trees.append(build(values, 0, 10000))
    checksum = 0
    for _ in range(50):
        for t in range(trees):
            checksum = (checksum * 31 + find_bottom_left_value(all_trees[t]) + 2147483648) % 1000000007
    print(f"{trees} trees of 10000 nodes, 50 times each: checksum {checksum}")


main()
