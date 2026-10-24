# Benchmark: LeetCode #968 Binary Tree Cameras -- the ★ arm, greedy from
# the leaves, on random trees of 1000 nodes, LeetCode's largest. Mirrors
# min_camera_cover.kara, .c, .rs and go-seq/.

import sys

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


seed = 968


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    rounds = 200
    trees = [random_tree(1000) for _ in range(200)]
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(200):
            c = min_camera_cover(trees[(r + i) % 200])
            total += c
            check = (check * 31 + c + i) % 1000000007
    print(f"{rounds} rounds over 200 trees of 1000 nodes: {total} cameras, checksum {check}")


main()
