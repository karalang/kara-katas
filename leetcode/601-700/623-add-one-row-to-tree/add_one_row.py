# LeetCode #623: Add One Row to Tree -- Python mirror of add_one_row.kara.
#
# The same recursion with the level and the same harness, printing the
# same lines.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def add_one_row(root, val, depth):
    if depth == 1:
        return TreeNode(val, root, None)
    insert(root, val, depth, 1)
    return root


def insert(node, val, depth, level):
    if node is not None:
        if level == depth - 1:
            node.left = TreeNode(val, node.left, None)
            node.right = TreeNode(val, None, node.right)
        else:
            insert(node.left, val, depth, level + 1)
            insert(node.right, val, depth, level + 1)


seed = 623


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(values):
        n = queue[head]
        head += 1
        if values[i] is not None:
            n.left = TreeNode(values[i])
            queue.append(n.left)
        i += 1
        if i < len(values):
            if values[i] is not None:
                n.right = TreeNode(values[i])
                queue.append(n.right)
            i += 1
    return root


def to_level(root):
    parts = []
    queue = [root]
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        if node is None:
            parts.append("null")
        else:
            parts.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
    while parts and parts[-1] == "null":
        parts.pop()
    return "[" + ",".join(parts) + "]"


def random_tree(size, lean):
    if size == 0:
        return None
    root = TreeNode(next_random() % 201 - 100)
    for _ in range(1, size):
        c = TreeNode(next_random() % 201 - 100)
        node = root
        while True:
            if next_random() % 100 < lean:
                if node.left is None:
                    node.left = c
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = c
                    break
                node = node.right
    return root


def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def show(values, val, depth):
    before = to_level(from_level(values))
    print(f"{before}, val = {val}, depth = {depth} -> {to_level(add_one_row(from_level(values), val, depth))}")


def summary(s):
    h = 0
    for c in s:
        h = (h * 31 + ord(c)) % 1000000007
    return f"{len(s)} characters, checksum {h}"


def main():
    show([4, 2, 6, 3, 1, 5], 1, 2)
    show([4, 2, None, 3, 1], 1, 3)
    show([7], 5, 1)
    show([7], 5, 2)
    show([1, 2, 3], -9, 1)
    show([1, 2, 3, 4, None, None, 5], 0, 4)
    show([1, None, 2, None, 3, None, 4], 8, 3)
    show([1, 2, 3, None, 4, 5], 100000, 3)
    total = []
    for _ in range(300):
        leans = [20, 50, 80]
        size = 1 + next_random() % 40
        lean = leans[next_random() % 3]
        tree = random_tree(size, lean)
        depth = 1 + next_random() % (height(tree) + 1)
        val = next_random() % 200001 - 100000
        total.append(to_level(add_one_row(tree, val, depth)))
    print(f"300 random trees: {summary(''.join(total))}")
    big = random_tree(10000, 50)
    print(f"10000 nodes, depth 3: {summary(to_level(add_one_row(big, 1, 3)))}")
    again = random_tree(10000, 50)
    below = height(again) + 1
    print(f"10000 nodes, depth {below}: {summary(to_level(add_one_row(again, -1, below)))}")


main()
