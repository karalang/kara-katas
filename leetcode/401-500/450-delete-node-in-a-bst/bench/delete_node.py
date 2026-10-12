# Benchmark for #450: mirror of delete_node.kara (recursive, successor's
# value copied in) on one random search tree of 1,000,000 values, built
# once, then 1,000,000 deletes of random keys.
import sys


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def delete_node(root, key):
    node = root
    if node is None:
        return None
    if key < node.val:
        node.left = delete_node(node.left, key)
        return node
    if key > node.val:
        node.right = delete_node(node.right, key)
        return node
    if node.left is None:
        return node.right
    if node.right is None:
        return node.left
    successor = node.right
    while successor.left is not None:
        successor = successor.left
    node.val = successor.val
    node.right = delete_node(node.right, successor.val)
    return node


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


def walk(node, out):
    if node is not None:
        walk(node.left, out)
        out.append(node.val)
        walk(node.right, out)


seed = 450


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    sys.setrecursionlimit(10000)
    n = 1000000
    deletes = 1000000
    # A shuffle of the even numbers below 2n.
    values = [i * 2 for i in range(n)]
    for i in range(n):
        r = next_random() * 32768
        r += next_random()
        j = i + r % (n - i)
        values[i], values[j] = values[j], values[i]
    root = None
    for v in values:
        root = insert(root, v)
    for _ in range(deletes):
        key = next_random() * 32768
        key = (key + next_random()) % (2 * n)
        root = delete_node(root, key)
    left = []
    walk(root, left)
    checksum = 0
    for v in left:
        checksum = (checksum * 31 + v) % 1000000007
    print(f"{deletes} deletes from {n} values: {len(left)} nodes left, checksum {checksum}")


main()
