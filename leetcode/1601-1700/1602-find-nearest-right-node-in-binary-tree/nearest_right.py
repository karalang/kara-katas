# LeetCode #1602: Find Nearest Right Node in Binary Tree -- the Python
# mirror of nearest_right.kara (the ★ arm): breadth first, a level at a
# time. Its output is byte-identical to the Kāra arms'.
from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def find_nearest_right_node(root, u):
    queue = deque()
    if root is not None:
        queue.append(root)
    while queue:
        width = len(queue)
        for i in range(width):
            node = queue.popleft()
            if node is u:
                return queue.popleft() if i + 1 < width else None
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
    return None


def from_level_order(items, u):
    root = TreeNode(items[0])
    found = root
    queue = deque([root])
    i = 1
    while i < len(items):
        node = queue.popleft()
        for side in range(2):
            if i < len(items):
                v = items[i]
                if v is not None:
                    child = TreeNode(v)
                    if v == u:
                        found = child
                    if side == 0:
                        node.left = child
                    else:
                        node.right = child
                    queue.append(child)
                i += 1
    return root, found


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def big(self):
        a = self.next()
        return a * 32768 + self.next()


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def random_tree(n, rng):
    values = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = rng.big() % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = [TreeNode(values[0])]
    free = [(nodes[0], True), (nodes[0], False)]
    for v in values[1:]:
        k = rng.big() % len(free)
        free[k], free[-1] = free[-1], free[k]
        parent, left = free.pop()
        child = TreeNode(v)
        if left:
            parent.left = child
        else:
            parent.right = child
        free.append((child, True))
        free.append((child, False))
        nodes.append(child)
    return nodes


def answer(node):
    return node.val if node is not None else 0


def batch(count, most, queries, rng):
    check = nodes = found = 0
    for _ in range(count):
        n = rng.big() % most + 1
        tree = random_tree(n, rng)
        for _ in range(queries):
            u = tree[rng.big() % n]
            a = answer(find_nearest_right_node(tree[0], u))
            if a > 0:
                found += 1
            check = mix(check, a)
        nodes += n
    print(f"{count} trees of up to {most} nodes: {nodes} nodes, {count * queries} queries, {found} found, checksum {check}")


def main():
    examples = [
        ([1, 2, 3, None, 4, 5, 6], 4),
        ([3, None, 4, 2], 2),
        ([1], 1),
        ([1, 2, 3, 4, None, None, 5], 4),
        ([1, 2, 3, 4, 5, 6, 7], 7),
        ([1, 2, None, 3], 3),
    ]
    for items, u in examples:
        root, node = from_level_order(items, u)
        n = find_nearest_right_node(root, node)
        print(n.val if n is not None else "null")
    rng = Rng(1602)
    batch(3000, 8, 5, rng)
    batch(300, 1000, 20, rng)
    batch(3, 100000, 20, rng)


main()
