# LeetCode #449: Serialize and Deserialize BST -- mirror of codec.kara
# (preorder, rebuilt with bounds).


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def write_preorder(node, out):
    if node is not None:
        out.append(str(node.val))
        write_preorder(node.left, out)
        write_preorder(node.right, out)


def serialize(root):
    out = []
    write_preorder(root, out)
    return ",".join(out)


def deserialize(data):
    values = [int(token) for token in data.split(",")] if data else []
    at = 0

    def build(low, high):
        nonlocal at
        if at == len(values) or values[at] < low or values[at] > high:
            return None
        v = values[at]
        at += 1
        left = build(low, v - 1)
        right = build(v + 1, high)
        return TreeNode(v, left, right)

    return build(-(2**63), 2**63 - 1)


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


def same(a, b):
    if a is None or b is None:
        return a is None and b is None
    return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)


def height(node):
    return 0 if node is None else 1 + max(height(node.left), height(node.right))


def visit(node, out):
    if node is not None:
        out.append(node.val)
        visit(node.left, out)
        visit(node.right, out)


def round_trip(root):
    text = serialize(root)
    back = deserialize(text)
    return same(root, back), serialize(back) == text


def show(values):
    root = None
    for v in values:
        root = insert(root, v)
    order = []
    visit(root, order)
    tree_back, text_back = round_trip(root)
    listed = ",".join(str(v) for v in order)
    print(f"[{listed}]: {len(order)} nodes, height {height(root)}, tree back {str(tree_back).lower()}, text back {str(text_back).lower()}")


seed = 449


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


show([2, 1, 3])
show([])
show([0])
show([10000, 0])
show([1, 2, 3, 4, 5, 6])
show([6, 5, 4, 3, 2, 1])
show([50, 30, 70, 20, 40, 60, 80, 35, 45, 65])
count = 300
nodes = 0
heights = 0
round_trips = 0
checksum = 0
for _ in range(count):
    n = next_random() % 201
    used = set()
    values = []
    while len(values) < n:
        v = next_random() % 10001
        if v not in used:
            used.add(v)
            values.append(v)
    if next_random() % 5 == 0:
        values.sort()
    root = None
    for v in values:
        root = insert(root, v)
    tree_back, text_back = round_trip(root)
    if tree_back and text_back:
        round_trips += 1
    order = []
    visit(root, order)
    nodes += len(order)
    heights += height(root)
    for v in order:
        checksum = (checksum * 31 + v) % 1000000007
print(f"{count} random trees: {nodes} nodes, heights {heights}, {round_trips} round trips, checksum {checksum}")
