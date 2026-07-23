"""LeetCode 230 — Kth Smallest Element in a BST (Python mirror / oracle).

Index-pool BST built by insertion; iterative in-order walk stops at the k-th
node (in-order of a BST is ascending). Mirrors the Kara version.
"""


class Node:
    def __init__(self, val):
        self.val = val
        self.left = -1
        self.right = -1


def insert(nodes, root, v):
    if root == -1:
        idx = len(nodes)
        nodes.append(Node(v))
        return idx
    if v < nodes[root].val:
        nodes[root].left = insert(nodes, nodes[root].left, v)
    else:
        nodes[root].right = insert(nodes, nodes[root].right, v)
    return root


def build(vals):
    nodes = []
    root = -1
    for v in vals:
        root = insert(nodes, root, v)
    return nodes


def kth_smallest(nodes, root, k):
    stack = []
    cur = root
    count = 0
    while cur != -1 or stack:
        while cur != -1:
            stack.append(cur)
            cur = nodes[cur].left
        node = stack.pop()
        count += 1
        if count == k:
            return nodes[node].val
        cur = nodes[node].right
    return -1


def report(vals, k):
    nodes = build(vals)
    root = 0 if nodes else -1
    print(kth_smallest(nodes, root, k))


def main():
    a = [3, 1, 4, 2]
    report(a, 1)
    report(a, 3)
    b = [5, 3, 6, 2, 4, 1]
    report(b, 3)
    report(b, 6)
    report([1], 1)
    report([2, 1], 2)
    report([10, 5, 15, 3, 7, 18], 4)
    report([8, 3, 10, 1, 6, 14, 4], 5)


main()
