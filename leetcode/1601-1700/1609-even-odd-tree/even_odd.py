# LeetCode #1609: Even Odd Tree -- the Python mirror of even_odd.kara:
# breadth first, a level at a time, each value checked for its parity and
# against the one before it on the level.
from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def is_even_odd_tree(root):
    queue = deque()
    if root is not None:
        queue.append(root)
    even = True
    while queue:
        prev = None
        for _ in range(len(queue)):
            node = queue.popleft()
            v = node.val
            if even:
                ok = v % 2 == 1 and (prev is None or v > prev)
            else:
                ok = v % 2 == 0 and (prev is None or v < prev)
            if not ok:
                return False
            prev = v
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        even = not even
    return True


def from_level_order(items):
    root = TreeNode(items[0])
    queue = deque([root])
    i = 1
    while i < len(items):
        node = queue.popleft()
        for side in range(2):
            if i < len(items):
                if items[i] is not None:
                    child = TreeNode(items[i])
                    if side == 0:
                        node.left = child
                    else:
                        node.right = child
                    queue.append(child)
                i += 1
    return root


seed = 1609


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw():
    a = next_random()
    return a * 32768 + next_random()


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def random_tree(n):
    nodes = [TreeNode(0)]
    free = [(nodes[0], True), (nodes[0], False)]
    for _ in range(1, n):
        k = draw() % len(free)
        # swap_remove
        free[k], free[-1] = free[-1], free[k]
        parent, left = free.pop()
        child = TreeNode(0)
        if left:
            parent.left = child
        else:
            parent.right = child
        free.append((child, True))
        free.append((child, False))
        nodes.append(child)
    level = [nodes[0]]
    depth = 0
    while level:
        if depth % 2 == 0:
            v = 1 + 2 * (next_random() % 5)
        else:
            v = 1000000 - 2 * (next_random() % 5)
        below = []
        for node in level:
            node.val = v
            step = 2 * (next_random() % 2 + 1)
            v = v + step if depth % 2 == 0 else v - step
            if node.left is not None:
                below.append(node.left)
            if node.right is not None:
                below.append(node.right)
        level = below
        depth += 1
    return nodes


def spoil(nodes):
    n = len(nodes)
    kind = next_random() % 4
    if kind == 0:
        a = nodes[draw() % n]
        a.val = a.val - 1 if a.val > 1 else a.val + 1
    elif kind == 1:
        a = nodes[draw() % n]
        b = nodes[draw() % n]
        a.val, b.val = b.val, a.val


def batch(count, most):
    check = nodes = even_odd = 0
    for _ in range(count):
        n = draw() % most + 1
        tree = random_tree(n)
        spoil(tree)
        yes = is_even_odd_tree(tree[0])
        if yes:
            even_odd += 1
        check = mix(check, 1 if yes else 0)
        nodes += n
    print(f"{count} trees of up to {most} nodes: {nodes} nodes, {even_odd} even-odd, checksum {check}")


examples = [
    [1, 10, 4, 3, None, 7, 9, 12, 8, 6, None, None, 2],
    [5, 4, 2, 3, 3, 7],
    [5, 9, 1, 3, 5, 7],
    [1],
    [2],
    [1, 10, 10],
    [1, 4, 10],
]
for items in examples:
    print("true" if is_even_odd_tree(from_level_order(items)) else "false")
batch(3000, 8)
batch(300, 1000)
batch(10, 100000)
