# LeetCode #653: Two Sum IV - Input is a BST -- in order, then two ends.
# Mirrors the ★ arm (two_sum_bst.kara) and its test harness.


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def find_target(root, k):
    values = []

    def in_order(node):
        if node is not None:
            in_order(node.left)
            values.append(node.val)
            in_order(node.right)

    in_order(root)
    if len(values) < 2:
        return False
    low, high = 0, len(values) - 1
    while low < high:
        s = values[low] + values[high]
        if s == k:
            return True
        elif s < k:
            low += 1
        else:
            high -= 1
    return False


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def bst(values):
    root = None
    for v in values:
        c = TreeNode(v)
        if root is None:
            root = c
            continue
        node = root
        while True:
            if v < node.val:
                if node.left is not None:
                    node = node.left
                else:
                    node.left = c
                    break
            else:
                if node.right is not None:
                    node = node.right
                else:
                    node.right = c
                    break
    return root


def distinct(count, low, high, rng):
    seen = set()
    values = []
    while len(values) < count:
        v = low + rng.next() % (high - low + 1)
        if v not in seen:
            seen.add(v)
            values.append(v)
    return values


def show(values, k):
    found = find_target(bst(values), k)
    print(f"{len(values)} values, k = {k} -> {'true' if found else 'false'}")


def main():
    show([5, 3, 6, 2, 4, 7], 9)
    show([5, 3, 6, 2, 4, 7], 28)
    show([1], 2)
    show([2, 1, 3], 4)
    show([2, 1, 3], 6)
    show([0, -10000, 10000], 0)
    show([0, -10000, 10000], -20000)
    show([0, -10000, 10000], 10000)
    show(list(range(1, 11)), 19)
    show(list(range(1, 11)), 20)
    rng = Rng(653)
    asked = yes = checksum = 0
    for _ in range(200):
        size = 1 + rng.next() % 60
        root = bst(distinct(size, -100, 100, rng))
        for _ in range(20):
            k = rng.next() % 401 - 200
            found = find_target(root, k)
            asked += 1
            yes += found
            checksum = (checksum * 2 + (1 if found else 0)) % 1000000007
    print(f"200 random trees: {yes} of {asked} found, checksum {checksum}")
    root = bst(distinct(10000, -10000, 10000, rng))
    yes = checksum = 0
    for _ in range(40):
        k = rng.next() % 60001 - 30000
        found = find_target(root, k)
        yes += found
        checksum = (checksum * 2 + (1 if found else 0)) % 1000000007
    print(f"10000 values: {yes} of 40 found, checksum {checksum}")


main()
