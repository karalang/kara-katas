# LeetCode #2236: Root Equals Sum of Children -- the mirror of
# check.kara: the root's value against the sum of its two children's.


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
    return TreeNode(root, TreeNode(left), TreeNode(right))


def show(root, left, right):
    print(f"[{root}, {left}, {right}] -> {'true' if check_tree(tree(root, left, right)) else 'false'}")


seed = 2236


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show(10, 4, 6)
    show(5, 3, 1)
    show(0, 0, 0)
    show(-100, -50, -50)
    show(0, -100, 100)
    show(100, 100, 1)
    show(10, 6, 4)
    trees = 0
    holding = 0
    for left in range(-100, 101):
        for right in range(-100, 101):
            for root in range(left + right - 1, left + right + 2):
                if -100 <= root <= 100:
                    trees += 1
                    if check_tree(tree(root, left, right)):
                        holding += 1
    print(f"{trees} trees near the sum: {holding} hold")
    check = 0
    for _ in range(3000):
        root = next_random() % 201 - 100
        left = next_random() % 201 - 100
        right = next_random() % 201 - 100
        check = (check * 2 + (1 if check_tree(tree(root, left, right)) else 0)) % 1000000007
    print(f"3000 random trees: checksum {check}")


main()
