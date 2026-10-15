# LeetCode #669: Trim a Binary Search Tree -- recursion, in place.
# Mirrors the ★ arm (trim_a_binary_search_tree.kara) and its test harness.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def trim_bst(root, low, high):
    if root is None:
        return None
    if root.val < low:
        return trim_bst(root.right, low, high)
    if root.val > high:
        return trim_bst(root.left, low, high)
    root.left = trim_bst(root.left, low, high)
    root.right = trim_bst(root.right, low, high)
    return root


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def bst(values):
    if not values:
        return None
    root = TreeNode(values[0])
    for v in values[1:]:
        at = root
        while True:
            if v < at.val:
                if at.left is None:
                    at.left = TreeNode(v)
                    break
                at = at.left
            elif v > at.val:
                if at.right is None:
                    at.right = TreeNode(v)
                    break
                at = at.right
            else:
                break
    return root


def chain(n):
    root = TreeNode(1)
    at = root
    for v in range(2, n + 1):
        at.right = TreeNode(v)
        at = at.right
    return root


def shuffled(n, rng):
    v = list(range(n))
    for i in range(1, n):
        j = rng.next() % (i + 1)
        v[i], v[j] = v[j], v[i]
    return v


def level_order(root):
    parts = []
    queue = [root]
    head = 0
    while head < len(queue):
        at = queue[head]
        head += 1
        if at is None:
            parts.append("null")
        else:
            parts.append(str(at.val))
            queue.append(at.left)
            queue.append(at.right)
    while parts and parts[-1] == "null":
        parts.pop()
    return "[" + ",".join(parts) + "]"


def stats(root):
    count = height = s = 0
    stack = [(root, 1)] if root is not None else []
    while stack:
        n, depth = stack.pop()
        count += 1
        height = max(height, depth)
        s = (s * 31 + n.val) % 1000000007
        if n.right is not None:
            stack.append((n.right, depth + 1))
        if n.left is not None:
            stack.append((n.left, depth + 1))
    return f"size {count}, height {height}, checksum {s}"


def show(values, low, high):
    before = level_order(bst(values))
    print(f"{before} in [{low}, {high}]: {level_order(trim_bst(bst(values), low, high))}")


def main():
    show([1, 0, 2], 1, 2)
    show([3, 0, 4, 2, 1], 1, 3)
    show([5], 5, 5)
    show([5], 6, 9)
    seven = [4, 2, 6, 1, 3, 5, 7]
    for low, high in [(0, 10), (8, 10), (3, 3), (5, 7), (1, 3)]:
        show(seven, low, high)
    show([8, 3, 10, 1, 6, 14, 4, 7, 13], 2, 13)
    rng = Rng(669)
    order = shuffled(10000, rng)
    print(f"random 10000: {stats(bst(order))}")
    for low, high in [(0, 9999), (2500, 7499), (5000, 5000), (-5, -1), (9000, 20000)]:
        print(f"  in [{low}, {high}]: {stats(trim_bst(bst(order), low, high))}")
    print(f"chain 10000 in [100, 9900]: {stats(trim_bst(chain(10000), 100, 9900))}")
    print(f"chain 10000 in [5000, 5000]: {stats(trim_bst(chain(10000), 5000, 5000))}")
    s = 0
    kept = 0
    for _ in range(1000):
        n = rng.next() % 21
        values = [rng.next() % 40 for _ in range(n)]
        low = rng.next() % 44 - 2
        high = low + rng.next() % 20
        t = level_order(trim_bst(bst(values), low, high))
        for b in t.encode():
            s = (s * 31 + b) % 1000000007
        if t != "[]":
            kept += 1
    print(f"1000 random trees: {kept} not empty, checksum {s}")


main()
