# LeetCode #2236: Root Equals Sum of Children -- the benchmark's Python
# mirror of check.kara: 10^6 trees of three nodes built and checked.


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def check_tree(root):
    if root is None or root.left is None or root.right is None:
        return False
    return root.val == root.left.val + root.right.val


def tree(root, left, right):
    node = TreeNode(root)
    node.left = TreeNode(left)
    node.right = TreeNode(right)
    return node


seed = 2236


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    holding = 0
    check = 0
    for _ in range(1000000):
        left = next_random() % 101 - 50
        right = next_random() % 101 - 50
        root = left + right + next_random() % 3 - 1
        holds = check_tree(tree(root, left, right))
        if holds:
            holding += 1
        check = (check * 2 + (1 if holds else 0)) % 1000000007
    print(f"10^6 trees: {holding} hold, checksum {check}")


main()
