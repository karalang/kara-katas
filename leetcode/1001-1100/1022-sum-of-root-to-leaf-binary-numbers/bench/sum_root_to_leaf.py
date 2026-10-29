# LeetCode #1022: Sum of Root To Leaf Binary Numbers -- bench
# Mirrors ./sum_root_to_leaf.kara; see ../README.md § Benchmarks.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def sum_root_to_leaf(root):
    return sum_from(root, 0)


def sum_from(node, above):
    if node is None:
        return 0
    value = above * 2 + node.val
    if node.left is None and node.right is None:
        return value
    return sum_from(node.left, value) + sum_from(node.right, value)


def main():
    count = 200
    rounds = 500
    seed = 1022

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def random_tree(n):
        root = TreeNode(next_random() % 2)
        placed = 1
        while placed < n:
            node = root
            level = 1
            while True:
                go_left = next_random() % 2 == 0
                nxt = node.left if go_left else node.right
                if nxt is not None:
                    node = nxt
                    level += 1
                    if level == 31:
                        break
                else:
                    leaf = TreeNode(next_random() % 2)
                    if go_left:
                        node.left = leaf
                    else:
                        node.right = leaf
                    placed += 1
                    break
        return root

    trees = []
    nodes = 0
    for _ in range(count):
        n = next_random() % 1000 + 1
        nodes += n
        trees.append(random_tree(n))
    total = 0
    check = 0
    for _ in range(rounds):
        for tree in trees:
            answer = sum_root_to_leaf(tree)
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"{count} trees, {nodes} nodes, {rounds} rounds: sum {total}, checksum {check}")


main()
