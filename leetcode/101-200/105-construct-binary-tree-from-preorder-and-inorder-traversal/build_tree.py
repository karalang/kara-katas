#!/usr/bin/env python3
"""LeetCode #103: Construct Binary Tree from Preorder and Inorder Traversal.

Mirror of build_tree.kara (recursive index-bounds split ★). The first element of a
preorder slice is that subtree's root; its position in the inorder slice splits inorder
into the left/right subtrees and gives the left subtree's size (how much of preorder is the
left child). Recurse on the two halves. Pure index-bounds recursion, no mutable cursor.
"""


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def find_in(inorder, in_lo, in_hi, target):
    i = in_lo
    while i <= in_hi:
        if inorder[i] == target:
            return i
        i += 1
    return -1


def build(preorder, inorder, pre_lo, pre_hi, in_lo, in_hi):
    if pre_lo > pre_hi:
        return None
    root_val = preorder[pre_lo]
    mid = find_in(inorder, in_lo, in_hi, root_val)
    left_size = mid - in_lo
    node = TreeNode(root_val)
    node.left = build(preorder, inorder, pre_lo + 1, pre_lo + left_size, in_lo, mid - 1)
    node.right = build(preorder, inorder, pre_lo + left_size + 1, pre_hi, mid + 1, in_hi)
    return node


def build_tree(preorder, inorder):
    n = len(preorder)
    return build(preorder, inorder, 0, n - 1, 0, n - 1)


def ser(node, acc):
    if node is None:
        return (acc * 131 + 1) % 1000000007
    acc = (acc * 131 + (node.val + 2)) % 1000000007
    acc = ser(node.left, acc)
    acc = ser(node.right, acc)
    return acc


# --- consistent (preorder, inorder) input generation from a reference BST ---

def bst_insert(root, v):
    if root is None:
        return TreeNode(v)
    if v < root.val:
        root.left = bst_insert(root.left, v)
    else:
        root.right = bst_insert(root.right, v)
    return root


def insert_all(nums):
    root = None
    for v in nums:
        root = bst_insert(root, v)
    return root


def preorder_of(node, out):
    if node is None:
        return
    out.append(node.val)
    preorder_of(node.left, out)
    preorder_of(node.right, out)


def inorder_of(node, out):
    if node is None:
        return
    inorder_of(node.left, out)
    out.append(node.val)
    inorder_of(node.right, out)


def main():
    base = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    acc = 0
    for t in range(8):
        nums = [base[(k + t) % len(base)] for k in range(len(base))]
        orig = insert_all(nums)
        pre, ino = [], []
        preorder_of(orig, pre)
        inorder_of(orig, ino)

        rebuilt = build_tree(pre, ino)
        s = ser(rebuilt, 0)
        acc = (acc * 1000003 + s) % 1000000007
        print(f"tree {t}: sig {s}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
