#!/usr/bin/env python3
"""LeetCode #106: Construct Binary Tree from Inorder and Postorder Traversal.

Mirror of build_tree.kara (recursive index-bounds split ★). Postorder ends with the root;
its position in the inorder slice splits inorder into the left/right subtrees and gives the
left subtree's size (how postorder divides into [left][right][root]). Recurse on the halves.
Pure index-bounds recursion, no mutable cursor.
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


def build(postorder, inorder, post_lo, post_hi, in_lo, in_hi):
    if post_lo > post_hi:
        return None
    root_val = postorder[post_hi]
    mid = find_in(inorder, in_lo, in_hi, root_val)
    left_size = mid - in_lo
    node = TreeNode(root_val)
    node.left = build(postorder, inorder, post_lo, post_lo + left_size - 1, in_lo, mid - 1)
    node.right = build(postorder, inorder, post_lo + left_size, post_hi - 1, mid + 1, in_hi)
    return node


def build_tree(postorder, inorder):
    n = len(postorder)
    return build(postorder, inorder, 0, n - 1, 0, n - 1)


def ser(node, acc):
    if node is None:
        return (acc * 131 + 1) % 1000000007
    acc = (acc * 131 + (node.val + 2)) % 1000000007
    acc = ser(node.left, acc)
    acc = ser(node.right, acc)
    return acc


# --- consistent (inorder, postorder) input generation from a reference BST ---

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


def inorder_of(node, out):
    if node is None:
        return
    inorder_of(node.left, out)
    out.append(node.val)
    inorder_of(node.right, out)


def postorder_of(node, out):
    if node is None:
        return
    postorder_of(node.left, out)
    postorder_of(node.right, out)
    out.append(node.val)


def main():
    base = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    acc = 0
    for t in range(8):
        nums = [base[(k + t) % len(base)] for k in range(len(base))]
        orig = insert_all(nums)
        ino, post = [], []
        inorder_of(orig, ino)
        postorder_of(orig, post)

        rebuilt = build_tree(post, ino)
        s = ser(rebuilt, 0)
        acc = (acc * 1000003 + s) % 1000000007
        print(f"tree {t}: sig {s}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
