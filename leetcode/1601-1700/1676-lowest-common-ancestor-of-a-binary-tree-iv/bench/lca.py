# LeetCode #1676: Lowest Common Ancestor of a Binary Tree IV -- the bench's
# Python mirror: the ★ arm on one tree of 10000 nodes asked about 500 sets
# of 1 to 50 nodes, all drawn first, each asked 10 times.

import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def lowest_common_ancestor(root, nodes):
    wanted = {n.val for n in nodes}

    def search(node):
        if node is None:
            return None
        if node.val in wanted:
            return node
        left = search(node.left)
        right = search(node.right)
        if left is not None and right is not None:
            return node
        return left if left is not None else right

    return search(root)


seed = 1676


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n):
    values = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = []
    for i in range(n):
        node = TreeNode(values[i])
        if i > 0:
            at = nodes[next_random() % i]
            while True:
                if next_random() % 2 == 0:
                    if at.left is not None:
                        at = at.left
                    else:
                        at.left = node
                        break
                else:
                    if at.right is not None:
                        at = at.right
                    else:
                        at.right = node
                        break
        nodes.append(node)
    return nodes


def main():
    n, queries, rounds = 10000, 500, 10
    nodes = random_tree(n)
    root = nodes[0]
    sets = []
    for _ in range(queries):
        k = next_random() % 50 + 1
        for i in range(k):
            j = i + next_random() % (n - i)
            nodes[i], nodes[j] = nodes[j], nodes[i]
        sets.append(nodes[:k])
    total = 0
    check = 0
    for r in range(rounds):
        for s in sets:
            found = lowest_common_ancestor(root, s).val
            total += found
            check = (check * 31 + found + r) % 1000000007
    print(f"{n} nodes, {queries} sets, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
