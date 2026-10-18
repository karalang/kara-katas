# LeetCode #700: Search in a Binary Search Tree -- recursion.
#
# A mirror of search_in_a_binary_search_tree.kara (the ★ arm) and its
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


def search_bst(root, val):
    if root is None:
        return None
    if val == root.val:
        return root
    if val < root.val:
        return search_bst(root.left, val)
    return search_bst(root.right, val)


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
    print(f"{level_order(tree)} search {val}: {level_order(search_bst(tree, val))}")


def checksum_bytes(total, s):
    for b in s.encode():
        total = (total * 31 + b) % 1000000007
    return total


def main():
    global seed
    show([4, 2, 7, 1, 3], 2)
    show([4, 2, 7, 1, 3], 5)
    show([5], 5)
    show([5], 4)
    for v in (8, 13, 0, 15, 6, 14):
        show([8, 3, 10, 1, 6, 14, 4, 7, 13], v)
    seed = 700
    tree = bst(shuffled(5000))
    print(f"random 5000: {stats(tree)}")
    found = sizes = total = 0
    for k in range(400):
        n = search_bst(tree, k * 4999 % 10000)
        if n is not None:
            found += 1
            s = stats(n)
            total = checksum_bytes(total, s)
            sizes += len(s)
    print(f"  400 searches: {found} found, checksum {total} over {sizes} bytes")
    line = chain(5000)
    print(f"chain 5000 search 5000: {stats(search_bst(line, 5000))}")
    print(f"chain 5000 search 1: {stats(search_bst(line, 1))}")
    print(f"chain 5000 search 5001: {stats(search_bst(line, 5001))}")
    total = hits = 0
    for _ in range(1000):
        n = next_random() % 21
        values = [next_random() % 40 for _ in range(n)]
        val = next_random() % 44 - 2
        s = level_order(search_bst(bst(values), val))
        if s != "[]":
            hits += 1
        total = checksum_bytes(total, s)
    print(f"1000 random trees: {hits} searches found, checksum {total}")


main()
