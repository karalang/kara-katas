# LeetCode #1602: Find Nearest Right Node in Binary Tree -- the bench in
# Python, mirroring nearest_right.kara: breadth first, a level at a time.
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


def main():
    rng = Rng(1602)
    trees = []
    picks = []
    for _ in range(10):
        tree = random_tree(100000, rng)
        picks.append([rng.big() % 100000 for _ in range(100)])
        trees.append(tree)
    check = found = 0
    for tree, us in zip(trees, picks):
        for k in us:
            a = answer(find_nearest_right_node(tree[0], tree[k]))
            if a > 0:
                found += 1
            check = mix(check, a)
    print(f"10 trees of 100000 nodes: 1000 queries, {found} found, checksum {check}")


main()
