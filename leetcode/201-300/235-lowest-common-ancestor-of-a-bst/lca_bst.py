# LeetCode 235 — Lowest Common Ancestor of a BST (oracle mirror).
import sys
sys.setrecursionlimit(10000)

class Node:
    __slots__ = ("val", "left", "right")
    def __init__(self, v): self.val = v; self.left = None; self.right = None

def insert(root, v):
    if root is None: return Node(v)
    if v < root.val: root.left = insert(root.left, v)
    else: root.right = insert(root.right, v)
    return root

def build(vals):
    root = None
    for v in vals: root = insert(root, v)
    return root

def lca(root, p, q):
    cur = root
    while cur is not None:
        if p < cur.val and q < cur.val: cur = cur.left
        elif p > cur.val and q > cur.val: cur = cur.right
        else: return cur.val
    return -1

def report(vals, p, q):
    print(lca(build(vals), p, q))

def main():
    a = [6, 2, 8, 0, 4, 7, 9, 3, 5]
    report(a, 2, 8); report(a, 2, 4); report(a, 3, 5); report(a, 0, 5); report(a, 7, 9)
    b = [5, 4, 3, 2, 1]
    report(b, 1, 2); report(b, 1, 5); report(b, 3, 4)

main()
