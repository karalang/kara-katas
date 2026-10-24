# Benchmark: LeetCode #979 Distribute Coins in Binary Tree -- the ★ arm,
# excess from the leaves, on random trees of 100 nodes, LeetCode's
# largest. Mirrors distribute_coins.kara, .c, .rs and go-seq/.

import sys

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
    nodes = [TreeNode(0)]
    for _ in range(1, n):
        node = TreeNode(0)
        attach(nodes[0], node)
        nodes.append(node)
    for _ in range(n):
        nodes[next_random() % n].val += 1
    return nodes[0]


def main():
    rounds = 200
    trees = [random_tree(100) for _ in range(2000)]
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(2000):
            m = distribute_coins(trees[(r + i) % 2000])
            total += m
            check = (check * 31 + m + i) % 1000000007
    print(f"{rounds} rounds over 2000 trees of 100 nodes: {total} moves, checksum {check}")


main()
