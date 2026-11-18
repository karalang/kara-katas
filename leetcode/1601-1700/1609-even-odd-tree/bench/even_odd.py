# LeetCode #1609: Even Odd Tree -- the bench in Python, mirroring
# even_odd.kara: breadth first, a level at a time over a deque, each value
# checked for its parity and against the one before it on the level.
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


def main():
    seed = 1609

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def big():
        a = next_random()
        return a * 32768 + next_random()

    def random_tree(n):
        nodes = [TreeNode(0)]
        free = [(nodes[0], True), (nodes[0], False)]
        for _ in range(1, n):
            k = big() % len(free)
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
            v = 1 + 2 * (next_random() % 5) if depth % 2 == 0 else 1000000 - 2 * (next_random() % 5)
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

    trees, picks = [], []
    for _ in range(20):
        trees.append(random_tree(100000))
        picks.append([(big() % 100000, big() % 100000) for _ in range(20)])
    check = checks = even_odd = 0
    for tree, pairs in zip(trees, picks):
        for a, b in [(0, 0)] + pairs:
            tree[a].val, tree[b].val = tree[b].val, tree[a].val
            yes = is_even_odd_tree(tree[0])
            tree[a].val, tree[b].val = tree[b].val, tree[a].val
            if yes:
                even_odd += 1
            check = (check * 31 + (1 if yes else 0) + 1) % 1000000007
            checks += 1
    print(f"20 trees of 100000 nodes: {checks} checks, {even_odd} even-odd, checksum {check}")


main()
