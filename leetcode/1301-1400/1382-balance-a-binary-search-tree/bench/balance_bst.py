# LeetCode #1382 bench -- Python: the ★ arm: the values read off in
# order, then a new tree built with the middle value at the root and each
# half built the same way beneath it.


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


seed = 1382


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def search_tree(values):
    root = TreeNode(values[0])
    for v in values[1:]:
        at = root
        while True:
            if v < at.val:
                if at.left:
                    at = at.left
                else:
                    at.left = TreeNode(v)
                    break
            else:
                if at.right:
                    at = at.right
                else:
                    at.right = TreeNode(v)
                    break
    return root


def main():
    trees = []
    for _ in range(10):
        step = 1 + next_random() % 99990
        start = next_random() % 99991
        values = [1 + (start + k * step) % 99991 for k in range(10000)]
        for i in range(9999, 0, -1):
            j = next_random() % (i + 1)
            values[i], values[j] = values[j], values[i]
        trees.append(search_tree(values))
    check = 0
    for _ in range(500):
        t = (check + next_random()) % 10
        balanced = balance_bst(trees[t])
        at = balanced
        while at:
            check = (check * 131 + at.val) % 1000000007
            at = at.left if next_random() % 2 == 0 else at.right
        trees[t] = balanced
    print(f"500 rounds over 10 trees of 10000 nodes: checksum {check}")


main()
