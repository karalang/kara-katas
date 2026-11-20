# LeetCode #1666: Change the Root of a Binary Tree -- the Python mirror of
# the ★ arm (up from the leaf).
from collections import deque


class Node:
    __slots__ = ("val", "left", "right", "parent")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None


def flip_binary_tree(root, leaf):
    cur = leaf
    below = None
    while True:
        above = cur.parent
        cur.parent = below
        if above is None:
            break
        p = above
        if p.left is cur:
            p.left = None
        else:
            p.right = None
        if cur.left is not None:
            cur.right = cur.left
        cur.left = p
        below = cur
        cur = p
    return leaf


# ---- the harness: the same in every arm --------------------------------


def from_level_order(items):
    root = Node(items[0])
    nodes = [root]
    queue = deque([root])
    i = 1
    while i < len(items):
        node = queue.popleft()
        for side in range(2):
            if i < len(items):
                v = items[i]
                if v is not None:
                    child = Node(v)
                    child.parent = node
                    if side == 0:
                        node.left = child
                    else:
                        node.right = child
                    queue.append(child)
                    nodes.append(child)
                i += 1
    return nodes


def written(root):
    items = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            items.append("null")
        else:
            items.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
    while items and items[-1] == "null":
        items.pop()
    return "[" + ",".join(items) + "]"


def level_order(root):
    if root.parent is not None:
        return None
    values = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        values.append(node.val)
        for c in (node.left, node.right):
            if c is not None:
                if c.parent is not node:
                    return None
                queue.append(c)
    return values


def find(nodes, val):
    for n in nodes:
        if n.val == val:
            return n
    raise ValueError("no such node")


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n):
    values = list(range(n))
    for i in range(n - 1, 0, -1):
        j = (next_random() * 32768 + next_random()) % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = []
    for i in range(n):
        node = Node(values[i])
        if i > 0:
            at = nodes[(next_random() * 32768 + next_random()) % i]
            while True:
                if next_random() % 2 == 0:
                    if at.left is not None:
                        at = at.left
                    else:
                        node.parent = at
                        at.left = node
                        break
                else:
                    if at.right is not None:
                        at = at.right
                    else:
                        node.parent = at
                        at.right = node
                        break
        nodes.append(node)
    return nodes


def batch(count, most):
    check = 0
    broken = 0
    for _ in range(count):
        n = next_random() % (most - 1) + 2
        nodes = random_tree(n)
        leaves = [v for v in nodes[1:] if v.left is None and v.right is None]
        pick = leaves[(next_random() * 32768 + next_random()) % len(leaves)]
        root = flip_binary_tree(nodes[0], pick)
        values = level_order(root)
        if values is None:
            broken += 1
        else:
            for v in values:
                check = (check * 31 + v + 1) % 1000000007
    print(f"{count} trees of up to {most} nodes: {broken} with broken parent links, checksum {check}")


items = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
tree = from_level_order(items)
print(written(flip_binary_tree(tree[0], find(tree, 7))))
tree = from_level_order(items)
print(written(flip_binary_tree(tree[0], find(tree, 0))))
tree = from_level_order([1, 2])
print(written(flip_binary_tree(tree[0], tree[1])))
tree = from_level_order([1, 2, 3, 4, 5])
print(written(flip_binary_tree(tree[0], find(tree, 4))))
seed = 1666
batch(3000, 8)
batch(300, 1000)
batch(30, 100000)
