# LeetCode #508: Most Frequent Subtree Sum -- post-order with a count
# table. Mirrors find_frequent_tree_sum.kara (the star arm) and its harness.

from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def subtree_sum(node, counts):
    if node is None:
        return 0
    s = node.val + subtree_sum(node.left, counts) + subtree_sum(node.right, counts)
    counts[s] = counts.get(s, 0) + 1
    return s


def find_frequent_tree_sum(root):
    counts = {}
    subtree_sum(root, counts)
    best = 0
    for c in counts.values():
        if c > best:
            best = c
    return [s for s, c in counts.items() if c == best]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(items):
    if items[0] is None:
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


def grow(size, half):
    root = TreeNode(next_random() % (2 * half + 1) - half)
    for _ in range(1, size):
        leaf = TreeNode(next_random() % (2 * half + 1) - half)
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
    sums = sorted(find_frequent_tree_sum(from_level_order(items)))
    print(f"{name}: [{', '.join(str(s) for s in sums)}]")


def main():
    global seed
    show("example 1", [5, 2, -3])
    show("example 2", [5, 2, -5])
    show("one node", [7])
    show("every sum once", [1, 2, 3, 4, 5, 6, 7])
    show("all zero", [0, 0, 0, 0])
    show("a chain", [1, None, -1, None, 1, None, -1])
    show("the extremes", [-100000, 100000, -100000, 100000, None, None, -100000])
    show("sums that cancel", [3, -3, -3, 3, 3, None, 3])
    seed = 508
    count = 300
    total = 0
    modes = 0
    checksum = 0
    for t in range(count):
        half = 2 if t % 3 == 0 else 50 if t % 3 == 1 else 100000
        size = 1 + next_random() % 40
        total += size
        for s in sorted(find_frequent_tree_sum(grow(size, half))):
            modes += 1
            checksum = (checksum * 31 + s + 10000000) % 1000000007
    print(f"{count} random trees: {total} nodes, {modes} most frequent sums, checksum {checksum}")


main()
