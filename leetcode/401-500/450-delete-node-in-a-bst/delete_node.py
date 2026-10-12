# LeetCode #450: Delete Node in a BST -- mirror of delete_node.kara
# (recursive, successor's value copied in), with the same harness.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def delete_node(root, key):
    node = root
    if node is None:
        return None
    if key < node.val:
        node.left = delete_node(node.left, key)
        return node
    if key > node.val:
        node.right = delete_node(node.right, key)
        return node
    if node.left is None:
        return node.right
    if node.right is None:
        return node.left
    successor = node.right
    while successor.left is not None:
        successor = successor.left
    node.val = successor.val
    node.right = delete_node(node.right, successor.val)
    return node


# ---- test harness ---------------------------------------------------------


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


def tree_of(values):
    root = None
    for v in values:
        root = insert(root, v)
    return root


def walk(node, out):
    if node is not None:
        walk(node.left, out)
        out.append(node.val)
        walk(node.right, out)


def search_tree(node, low, high):
    if node is None:
        return True
    return (low < node.val < high and search_tree(node.left, low, node.val)
            and search_tree(node.right, node.val, high))


def listed(values):
    return ",".join(str(v) for v in values)


def show(values, key):
    after = delete_node(tree_of(values), key)
    left = []
    walk(after, left)
    valid = "true" if search_tree(after, -(1 << 63), (1 << 63) - 1) else "false"
    print(f"[{listed(values)}] delete {key}: [{listed(left)}], search tree {valid}")


seed = 450


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([5, 3, 6, 2, 4, 7], 3)
    show([5, 3, 6, 2, 4, 7], 0)
    show([], 0)
    show([5, 3, 6, 2, 4, 7], 5)
    show([5, 3, 6, 2, 4, 7], 7)
    show([1], 1)
    show([1, 2, 3, 4, 5, 6], 1)
    show([6, 5, 4, 3, 2, 1], 6)
    show([50, 30, 70, 20, 40, 60, 80, 35, 45, 65], 30)
    count = 300
    found = missed = left_over = 0
    all_search_trees = True
    checksum = 0
    for _ in range(count):
        n = next_random() % 101
        used = set()
        values = []
        while len(values) < n:
            v = next_random() % 200
            if v not in used:
                used.add(v)
                values.append(v)
        if next_random() % 5 == 0:
            values.sort()
        root = tree_of(values)
        size = n
        for _ in range(20):
            key = next_random() % 200
            root = delete_node(root, key)
            left = []
            walk(root, left)
            if len(left) < size:
                found += 1
            else:
                missed += 1
            size = len(left)
            if not search_tree(root, -(1 << 63), (1 << 63) - 1):
                all_search_trees = False
            for v in left:
                checksum = (checksum * 31 + v) % 1000000007
        left_over += size
    flag = "true" if all_search_trees else "false"
    print(f"{count} random trees: {found} keys found, {missed} missed, {left_over} nodes left, search trees {flag}, checksum {checksum}")


main()
