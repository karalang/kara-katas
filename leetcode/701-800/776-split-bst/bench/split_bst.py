# Benchmark for #776: Split BST -- mirror of the ★ arm (recursive), with
# the same workload as split_bst.kara.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


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


def weigh(root, depth):
    if root is None:
        return 0
    return root.val * depth + weigh(root.left, depth + 1) + weigh(root.right, depth + 1)


def main():
    count = 64
    seed = 776

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    orders = []
    targets = []
    for _ in range(count):
        used = set()
        values = []
        while len(values) < 50:
            v = next_random() % 1001
            if v not in used:
                used.add(v)
                values.append(v)
        orders.append(values)
        targets.append(next_random() % 1001)
    checksum = 0
    for rnd in range(200000):
        g = rnd % count
        root = None
        for v in orders[g]:
            root = insert(root, v)
        small, large = split_bst(root, targets[g])
        checksum = (checksum * 31 + weigh(small, 1) + 3 * weigh(large, 1)) % 1000000007
    print(f"200000 rounds of 50 values: checksum {checksum}")


main()
