# LeetCode #1022: Sum of Root To Leaf Binary Numbers -- recursion
# Mirrors sum_root_to_leaf.kara (the ★ arm) and prints the same output.
from collections import deque


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


seed = 1022


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(values):
    if not values or values[0] < 0:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    k = 1
    while k < len(values):
        node = queue.popleft()
        if values[k] >= 0:
            node.left = TreeNode(values[k])
            queue.append(node.left)
        k += 1
        if k < len(values) and values[k] >= 0:
            node.right = TreeNode(values[k])
            queue.append(node.right)
        k += 1
    return root


def random_tree(n, depth, ones):
    root = TreeNode(1 if next_random() % 8 < ones else 0)
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
                if level == depth:
                    break
            else:
                leaf = TreeNode(1 if next_random() % 8 < ones else 0)
                if go_left:
                    node.left = leaf
                else:
                    node.right = leaf
                placed += 1
                break
    return root


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    examples = [
        [1, 0, 1, 0, 1, 0, 1],
        [0],
        [1],
        [1, 1],
        [1, -1, 0],
        [0, 1, -1, 1, 0],
        [1, 0, 0, -1, 1, 1, -1, 0, -1, -1, 1],
    ]
    for values in examples:
        print(f"{show(values)} -> {sum_root_to_leaf(from_level_order(values))}")
    groups = [(3000, 7, 4), (1000, 30, 4), (300, 200, 1), (300, 200, 7), (50, 1000, 4), (50, 1000, 8)]
    for count, n, ones in groups:
        total = 0
        most = 0
        check = 0
        for _ in range(count):
            answer = sum_root_to_leaf(random_tree(n, 31, ones))
            total += answer
            most = max(most, answer)
            check = (check * 31 + answer) % 1000000007
        print(f"{count} random trees of {n} nodes ({ones}/8 ones): sum {total}, most {most}, checksum {check}")
    path = [1]
    for _ in range(1, 31):
        path += [-1, 1]
    full = [1] * 1023
    print(f"a path of 31 ones: {sum_root_to_leaf(from_level_order(path))}; 10 full levels of ones: {sum_root_to_leaf(from_level_order(full))}")


main()
