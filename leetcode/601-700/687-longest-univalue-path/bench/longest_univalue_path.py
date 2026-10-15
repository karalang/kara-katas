# LeetCode #687: Longest Univalue Path -- one walk, two arms per node.
# Bench.
#
# 100 random trees of up to 16 levels, values 1 and 2, are built once;
# then 30 rounds answer every tree.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def longest_univalue_path(root):
    best = [0]
    arm(root, best)
    return best[0]


def arm(node, best):
    if node is None:
        return 0
    l = arm(node.left, best)
    r = arm(node.right, best)
    left = 0
    right = 0
    if node.left is not None and node.left.val == node.val:
        left = l + 1
    if node.right is not None and node.right.val == node.val:
        right = r + 1
    if left + right > best[0]:
        best[0] = left + right
    return max(left, right)


seed = 687


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(levels):
    n = TreeNode(1 + next_random() % 2)
    if levels > 1:
        if next_random() % 100 < 88:
            n.left = random_tree(levels - 1)
        if next_random() % 100 < 88:
            n.right = random_tree(levels - 1)
    return n


def main():
    count = 100
    rounds = 30
    trees = [random_tree(16) for _ in range(count)]
    total = 0
    for r in range(rounds):
        for c in range(count):
            k = longest_univalue_path(trees[c])
            total = (total * 31 + k + r) % 1000000007
    print(f"{count * rounds} trees answered, checksum {total}")


main()
