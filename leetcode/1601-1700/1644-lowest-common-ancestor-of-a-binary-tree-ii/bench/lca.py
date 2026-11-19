# LeetCode #1644: Lowest Common Ancestor of a Binary Tree II -- the bench's
# Python mirror: the ★ arm on 60 random trees of 10000 nodes, each asked
# about 50 pairs of values, one in five of them not in the tree, all drawn
# first.

import sys

sys.setrecursionlimit(100000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def lowest_common_ancestor(root, p, q):
    found = [None]

    def count_below(node):
        if node is None:
            return 0
        here = 1 if node.val == p.val or node.val == q.val else 0
        count = count_below(node.left) + count_below(node.right) + here
        if count == 2 and found[0] is None:
            found[0] = node
        return count

    count_below(root)
    return found[0]


# ---- the harness ----------------------------------------------------------


seed = 1644


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
    return nodes[0]


trees = []
for _ in range(60):
    root = random_tree(10000)
    pairs = []
    for _ in range(50):
        p = next_random() % 12500
        q = next_random() % 12500
        if q == p:
            q = (q + 1) % 12500
        pairs.append((p, q))
    trees.append((root, pairs))
check = 0
total = 0
for root, pairs in trees:
    for p, q in pairs:
        node = lowest_common_ancestor(root, TreeNode(p), TreeNode(q))
        found = -1 if node is None else node.val
        total += found + 1
        check = (check * 31 + found + 2) % 1000000007
print(f"60 trees of 10000 nodes, 50 pairs each: answers sum to {total}, checksum {check}")
