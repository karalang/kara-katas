# LeetCode #2331: Evaluate Boolean Binary Tree -- the Python mirror of
# the ★ arm: a leaf is its own truth, and an OR or an AND node its two
# subtrees evaluated recursively and joined.


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def evaluate_tree(root):
    if root is None:
        return False
    if root.val == 0:
        return False
    if root.val == 1:
        return True
    if root.val == 2:
        return evaluate_tree(root.left) or evaluate_tree(root.right)
    return evaluate_tree(root.left) and evaluate_tree(root.right)


def leaf(value):
    return TreeNode(value)


def join(op, left, right):
    return TreeNode(op, left, right)


seed = 2331


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(depth):
    if depth == 0 or next_random() % 3 == 0:
        return leaf(next_random() % 2)
    op = next_random() % 2 + 2
    left = random_tree(depth - 1)
    right = random_tree(depth - 1)
    return join(op, left, right)


def show(value):
    print("true" if value else "false")


def main():
    show(evaluate_tree(join(2, leaf(1), join(3, leaf(0), leaf(1)))))
    show(evaluate_tree(leaf(0)))
    show(evaluate_tree(leaf(1)))
    show(evaluate_tree(join(3, leaf(0), leaf(1))))
    show(evaluate_tree(join(2, leaf(0), leaf(0))))
    chain = leaf(0)
    for _ in range(500):
        chain = join(3, chain, leaf(1))
    show(evaluate_tree(chain))
    check = 0
    truths = 0
    for _ in range(3000):
        depth = next_random() % 9
        value = evaluate_tree(random_tree(depth))
        check = (check * 3 + (1 if value else 2)) % 1000000007
        if value:
            truths += 1
    print(f"3000 trees: checksum {check}, {truths} true")


main()
