# LeetCode #968: Binary Tree Cameras -- greedy from the leaves.
#
# Mirrors min_camera_cover.kara: walk the tree bottom up, each subtree
# reporting its root's state: 0 not yet covered, 1 holds a camera, 2
# covered without one. A node with an uncovered child takes a camera; a
# node with a camera below is covered; otherwise it waits for its parent,
# and an uncovered root takes one itself.

import sys
from collections import deque

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def min_camera_cover(root):
    cameras = 0

    def watch(t):
        nonlocal cameras
        if t is None:
            return 2
        l = watch(t.left)
        r = watch(t.right)
        if l == 0 or r == 0:
            cameras += 1
            return 1
        if l == 1 or r == 1:
            return 2
        return 0

    if watch(root) == 0:
        cameras += 1
    return cameras


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while i < len(vals):
        node = queue.popleft()
        if vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals):
            if vals[i] is not None:
                node.right = TreeNode(vals[i])
                queue.append(node.right)
            i += 1
    return root


def attach(root, node):
    cur = root
    while True:
        if next_random() % 2 == 0:
            if cur.left is not None:
                cur = cur.left
            else:
                cur.left = node
                return
        else:
            if cur.right is not None:
                cur = cur.right
            else:
                cur.right = node
                return


def random_tree(n):
    root = TreeNode(0)
    for _ in range(1, n):
        attach(root, TreeNode(0))
    return root


def complete_tree(n):
    nodes = [TreeNode(0) for _ in range(n)]
    for i in range(1, n):
        if i % 2 == 1:
            nodes[(i - 1) // 2].left = nodes[i]
        else:
            nodes[(i - 1) // 2].right = nodes[i]
    return nodes[0]


def path(n):
    t = TreeNode(0)
    for _ in range(1, n):
        t = TreeNode(0, t)
    return t


def size(t):
    if t is None:
        return 0
    return 1 + size(t.left) + size(t.right)


def main():
    global seed
    N = None
    cases = [
        [0, 0, N, 0, 0],
        [0, 0, N, 0, N, 0, N, N, 0],
        [0],
        [0, 0],
        [0, 0, 0],
        [0, 0, N, 0, N, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, N, 0, N, 0, N, 0],
        [0, 0, 0, 0, N, N, 0, 0, N, N, 0],
        [0, N, 0, N, 0, N, 0, N, 0],
    ]
    for i, c in enumerate(cases):
        print(f"case {i + 1}: {min_camera_cover(from_level_order(c))}")
    seed = 968
    nodes = 0
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 12
        t = random_tree(n)
        nodes += size(t)
        c = min_camera_cover(t)
        total += c
        check = (check * 31 + c + 1) % 1000000007
    print(f"300 random trees of {nodes} nodes: {total} cameras, checksum {check}")
    print(f"a random tree of 1000 nodes: {min_camera_cover(random_tree(1000))} cameras")
    print(f"the complete tree of 1000 nodes: {min_camera_cover(complete_tree(1000))} cameras")
    print(f"a path of 1000 nodes: {min_camera_cover(path(1000))} cameras")


main()
