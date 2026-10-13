# LeetCode #510: Inorder Successor in BST II -- down the right subtree,
# or up to the first larger ancestor. Mirrors inorder_successor.kara (the
# star arm) and its harness.


class Node:
    __slots__ = ("val", "left", "right", "parent")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None


def inorder_successor(node):
    if node.right is not None:
        cur = node.right
        while cur.left is not None:
            cur = cur.left
        return cur
    up = node.parent
    while up is not None:
        if up.val > node.val:
            return up
        up = up.parent
    return None


# ---- test harness ---------------------------------------------------------

seed = 510


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(values):
    root = Node(values[0])
    for v in values[1:]:
        leaf = Node(v)
        node = root
        while True:
            if v < node.val:
                if node.left is not None:
                    node = node.left
                else:
                    leaf.parent = node
                    node.left = leaf
                    break
            else:
                if node.right is not None:
                    node = node.right
                else:
                    leaf.parent = node
                    node.right = leaf
                    break
    return root


def find(root, v):
    node = root
    while node.val != v:
        node = node.left if v < node.val else node.right
    return node


def answer(node):
    return "null" if node is None else str(node.val)


def show(name, values, target):
    root = build(values)
    print(f"{name}: [{', '.join(str(v) for v in values)}], node {target} -> {answer(inorder_successor(find(root, target)))}")


def main():
    show("example 1", [2, 1, 3], 1)
    show("example 2", [5, 3, 6, 2, 4, 1], 6)
    show("down the right subtree", [5, 3, 6, 2, 4, 1], 3)
    show("up two levels", [5, 3, 6, 2, 4, 1], 4)
    show("the smallest", [5, 3, 6, 2, 4, 1], 1)
    show("one node", [7], 7)
    show("a chain to the right", [1, 2, 3, 4], 2)
    show("a chain to the left", [4, 3, 2, 1], 1)
    show("the extremes", [-100000, 100000, 0], 0)
    count = 300
    nodes = 0
    nulls = 0
    checksum = 0
    for t in range(count):
        spread = 1 if t % 3 == 0 else 7 if t % 3 == 1 else 5000
        size = 1 + next_random() % 40
        values = []
        for j in range(size):
            values.append(j * spread + next_random() % spread - 100000)
        for i in range(1, size):
            k = next_random() % (i + 1)
            values[i], values[k] = values[k], values[i]
        root = build(values)
        for v in values:
            nodes += 1
            s = inorder_successor(find(root, v))
            if s is not None:
                checksum = (checksum * 31 + s.val + 100000) % 1000000007
            else:
                nulls += 1
    print(f"{count} random trees: {nodes} nodes, {nulls} without a successor, checksum {checksum}")


main()
