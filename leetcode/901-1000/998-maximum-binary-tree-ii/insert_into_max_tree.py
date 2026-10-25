# LeetCode #998: Maximum Binary Tree II -- mirror of the ★ arm
# (insert_into_max_tree.kara), down the right spine by recursion.
from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def insert_into_max_tree(root, val):
    if root is None:
        return TreeNode(val)
    if val > root.val:
        return TreeNode(val, root, None)
    root.right = insert_into_max_tree(root.right, val)
    return root


seed = 998


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def construct(a):
    def go(lo, hi):
        if lo >= hi:
            return None
        m = lo
        for i in range(lo + 1, hi):
            if a[i] > a[m]:
                m = i
        return TreeNode(a[m], go(lo, m), go(m + 1, hi))
    return go(0, len(a))


def level_order(root):
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def text(vals):
    return "[" + ",".join("null" if v is None else str(v) for v in vals) + "]"


def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def fold(check, vals):
    for v in vals:
        check = (check * 31 + (0 if v is None else v) + 1) % 1000000007
    return check


def random_case(n):
    pool = list(range(1, 101))
    for i in range(n + 1):
        j = i + next_random() % (100 - i)
        pool[i], pool[j] = pool[j], pool[i]
    return pool[:n], pool[n]


def main():
    cases = [
        ([1, 4, 2, 3], 5),
        ([2, 1, 5, 4], 3),
        ([2, 1, 5, 3], 4),
        ([1], 2),
        ([2], 1),
        ([1, 2, 3], 4),
        ([2, 3, 4], 1),
        ([4, 3, 1], 2),
        ([7, 1, 6, 2, 5, 3], 4),
        ([5, 4, 3, 2], 1),
    ]
    for a, val in cases:
        root = construct(a)
        before = text(level_order(root))
        after = text(level_order(insert_into_max_tree(root, val)))
        print(f"root = {before}, val = {val} -> {after}")
    big = [
        ("99 values rising from 1", list(range(1, 100)), 100),
        ("99 values rising from 2", list(range(2, 101)), 1),
        ("99 values falling from 100", list(range(100, 1, -1)), 1),
        ("99 values falling from 99", list(range(99, 0, -1)), 100),
        ("99 values falling from 100 but 50", [v for v in range(100, 0, -1) if v != 50], 50),
    ]
    for name, a, val in big:
        got = insert_into_max_tree(construct(a), val)
        vals = level_order(got)
        print(f"{name}, val = {val}: height {height(got)}, root {got.val}, checksum {fold(0, vals)}")
    for count, most in [(300, 5), (3000, 30), (300, 99)]:
        nodes = 0
        heights = 0
        check = 0
        for _ in range(count):
            n = 1 + next_random() % most
            a, val = random_case(n)
            got = insert_into_max_tree(construct(a), val)
            nodes += n + 1
            heights += height(got)
            check = fold(check, level_order(got))
        print(f"{count} random trees of {nodes} nodes: heights {heights}, checksum {check}")


main()
