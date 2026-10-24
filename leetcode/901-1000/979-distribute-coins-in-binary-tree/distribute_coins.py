# LeetCode #979: Distribute Coins in Binary Tree -- mirror of the ★ arm
# (distribute_coins.kara), excess from the leaves.
import sys
from collections import deque

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def distribute_coins(root):
    moves = 0

    def excess(t):
        nonlocal moves
        if t is None:
            return 0
        l = excess(t.left)
        r = excess(t.right)
        moves += abs(l) + abs(r)
        return t.val + l + r - 1

    excess(root)
    return moves


seed = 979


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
            if cur.left is None:
                cur.left = node
                return
            cur = cur.left
        else:
            if cur.right is None:
                cur.right = node
                return
            cur = cur.right


def random_tree(n):
    nodes = [TreeNode(0)]
    for _ in range(1, n):
        node = TreeNode(0)
        attach(nodes[0], node)
        nodes.append(node)
    for _ in range(n):
        nodes[next_random() % n].val += 1
    return nodes[0]


def complete_tree(n):
    nodes = [TreeNode(0) for _ in range(n)]
    for i in range(1, n):
        if i % 2 == 1:
            nodes[(i - 1) // 2].left = nodes[i]
        else:
            nodes[(i - 1) // 2].right = nodes[i]
    nodes[0].val = n
    return nodes[0]


def path(n):
    t = TreeNode(n)
    for _ in range(1, n):
        t = TreeNode(0, t)
    return t


def main():
    cases = [
        [3, 0, 0],
        [0, 3, 0],
        [1],
        [1, 0, 2],
        [0, 0, 3],
        [1, 0, 0, None, 3],
        [0, 0, None, 0, None, 4],
        [4, 0, None, 0, None, 0],
        [7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7],
    ]
    for i, vals in enumerate(cases):
        print(f"case {i + 1}: {distribute_coins(from_level_order(vals))}")
    for count, most in [(300, 12), (3000, 100)]:
        nodes = total = check = 0
        for _ in range(count):
            n = 1 + next_random() % most
            m = distribute_coins(random_tree(n))
            nodes += n
            total += m
            check = (check * 31 + m + 1) % 1000000007
        print(f"{count} random trees of {nodes} nodes: {total} moves, checksum {check}")
    print(f"a random tree of 100 nodes: {distribute_coins(random_tree(100))} moves")
    print(f"the complete tree of 100 nodes, every coin on the root: {distribute_coins(complete_tree(100))} moves")
    print(f"a path of 100 nodes, every coin at the far end: {distribute_coins(path(100))} moves")


main()
