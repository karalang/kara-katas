# LeetCode #701: Insert into a Binary Search Tree -- recursion.
#
# A mirror of insert_into_a_binary_search_tree.kara (the ★ arm) and its
# harness.

import sys

sys.setrecursionlimit(20000)
seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def insert_into_bst(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root


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


def shuffled(n):
    v = list(range(n))
    for i in range(1, n):
        j = next_random() % (i + 1)
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
    count = height = total = 0
    stack = [(root, 1)] if root is not None else []
    while stack:
        n, depth = stack.pop()
        count += 1
        height = max(height, depth)
        total = (total * 31 + n.val) % 1000000007
        if n.right is not None:
            stack.append((n.right, depth + 1))
        if n.left is not None:
            stack.append((n.left, depth + 1))
    if count == 0:
        return "none"
    return f"size {count}, height {height}, checksum {total}"


def show(values, val):
    tree = bst(values)
    before = level_order(tree)
    print(f"{before} insert {val}: {level_order(insert_into_bst(tree, val))}")


def checksum_bytes(total, s):
    for b in s.encode():
        total = (total * 31 + b) % 1000000007
    return total


def main():
    global seed
    show([4, 2, 7, 1, 3], 5)
    show([40, 20, 60, 10, 30, 50, 70], 25)
    show([], 5)
    show([5], 3)
    show([5], 8)
    for v in (0, 15, 2, 5, 9, 12):
        show([8, 3, 10, 1, 6, 14, 4, 7, 13], v)
    seed = 701
    tree = bst([2 * v for v in shuffled(10000)])
    print(f"random 10000: {stats(tree)}")
    for k in range(50):
        tree = insert_into_bst(tree, k * 7919 % 10000 * 2 + 1)
    print(f"  after 50 inserts: {stats(tree)}")
    line = chain(3000)
    line = insert_into_bst(line, 3001)
    print(f"chain 3000 insert 3001: {stats(line)}")
    line = insert_into_bst(line, 0)
    print(f"  then insert 0: {stats(line)}")
    total = sizes = 0
    for _ in range(1000):
        n = next_random() % 21
        values = [next_random() % 100 - 50 for _ in range(n)]
        val = next_random() % 104 - 52
        while val in values:
            val = next_random() % 104 - 52
        s = level_order(insert_into_bst(bst(values), val))
        sizes += len(s)
        total = checksum_bytes(total, s)
    print(f"1000 random trees: checksum {total} over {sizes} bytes")


main()
