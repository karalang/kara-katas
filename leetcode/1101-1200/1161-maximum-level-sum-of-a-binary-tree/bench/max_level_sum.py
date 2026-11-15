# LeetCode #1161: Maximum Level Sum of a Binary Tree -- the bench in
# Python, the ★ arm over objects with `__slots__`, the same 16 trees and
# 200 rounds.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val, self.left, self.right = val, None, None


def max_level_sum(root):
    level = [root] if root else []
    best = best_sum = depth = 0
    while level:
        depth += 1
        total = 0
        nxt = []
        for node in level:
            total += node.val
            if node.left:
                nxt.append(node.left)
            if node.right:
                nxt.append(node.right)
        if best == 0 or total > best_sum:
            best, best_sum = depth, total
        level = nxt
    return best


seed = 1161


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_value():
    a = next_random()
    b = next_random()
    return (a * 32768 + b) % 200001 - 100000


def grow(nodes):
    c = TreeNode(random_value())
    while True:
        at = nodes[next_random() % len(nodes)]
        if next_random() % 2 == 0:
            if at.left is None:
                at.left = c
                break
        elif at.right is None:
            at.right = c
            break
    nodes.append(c)


def main():
    trees = []
    for _ in range(16):
        nodes = [TreeNode(random_value())]
        for _ in range(1, 10000):
            grow(nodes)
        trees.append(nodes)
    total = check = 0
    for _ in range(200):
        for nodes in trees:
            grow(nodes)
            level = max_level_sum(nodes[0])
            total += level
            check = (check * 31 + level) % 1000000007
    print(f"200 rounds over 16 trees of 10^4 nodes: levels total {total}, checksum {check}")


main()
