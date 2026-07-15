#!/usr/bin/env python3
"""LeetCode #108: Convert Sorted Array to Binary Search Tree — recursive middle-pick (mirror
of sorted_to_bst.kara).

Make the middle element (`(lo + hi) // 2`) the root; left half becomes the left subtree, right
half the right subtree. Choosing the middle keeps the halves within one of each other, so the
tree is height-balanced. O(n).
"""


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def build(arr, lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    node = TreeNode(arr[mid])
    node.left = build(arr, lo, mid - 1)
    node.right = build(arr, mid + 1, hi)
    return node


def sorted_to_bst(arr):
    return build(arr, 0, len(arr) - 1)


def ser(node, acc):
    if node is None:
        return (acc * 131 + 1) % 1000000007
    acc = (acc * 131 + (node.val + 2)) % 1000000007
    acc = ser(node.left, acc)
    acc = ser(node.right, acc)
    return acc


def main():
    acc = 0
    for t in range(8):
        length = 8 + t
        arr = [t + 1 + i for i in range(length)]
        root = sorted_to_bst(arr)
        s = ser(root, 0)
        acc = (acc * 1000003 + s) % 1000000007
        print(f"array {t}: len {length} sig {s}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
