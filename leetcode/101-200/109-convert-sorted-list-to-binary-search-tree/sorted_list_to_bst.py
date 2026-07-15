#!/usr/bin/env python3
"""LeetCode #109: Convert Sorted Linked List to Binary Search Tree — walk to array, then
middle-pick (mirror of sorted_list_to_bst.kara).

Walk the sorted list once into a Python list, then build a height-balanced BST by the
middle-pick divide-and-conquer (the middle is the root, halves are the subtrees).
"""


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def build_from_arr(arr, lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    node = TreeNode(arr[mid])
    node.left = build_from_arr(arr, lo, mid - 1)
    node.right = build_from_arr(arr, mid + 1, hi)
    return node


def sorted_list_to_bst(head):
    arr = []
    cur = head
    while cur is not None:
        arr.append(cur.val)
        cur = cur.next
    return build_from_arr(arr, 0, len(arr) - 1)


def ser(node, acc):
    if node is None:
        return (acc * 131 + 1) % 1000000007
    acc = (acc * 131 + (node.val + 2)) % 1000000007
    acc = ser(node.left, acc)
    acc = ser(node.right, acc)
    return acc


def build_list(len_, off):
    head = None
    for i in range(len_ - 1, -1, -1):
        head = ListNode(off + 1 + i, head)
    return head


def main():
    acc = 0
    for t in range(8):
        length = 8 + t
        head = build_list(length, t)
        root = sorted_list_to_bst(head)
        s = ser(root, 0)
        acc = (acc * 1000003 + s) % 1000000007
        print(f"list {t}: len {length} sig {s}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
