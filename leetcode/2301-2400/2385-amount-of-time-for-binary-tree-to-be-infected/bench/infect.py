# LeetCode #2385: Amount of Time for Binary Tree to Be Infected -- the
# bench, the ★ arm in Python: one post-order walk returning each
# subtree's height and the start's distance below it. The nodes are
# objects with `__slots__`.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(node, start, best):
    if node is None:
        return 0, -1
    lh, ld = walk(node.left, start, best)
    rh, rd = walk(node.right, start, best)
    height = 1 + max(lh, rh)
    if node.val == start:
        best[0] = max(best[0], max(lh, rh))
        return height, 0
    if ld >= 0:
        best[0] = max(best[0], ld + 1 + rh)
        return height, ld + 1
    if rd >= 0:
        best[0] = max(best[0], rd + 1 + lh)
        return height, rd + 1
    return height, -1


def amount_of_time(root, start):
    best = [0]
    walk(root, start, best)
    return best[0]


seed = 2385


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n):
    values = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = [TreeNode(v) for v in values]
    for k in range(1, n):
        high = next_random()
        at = nodes[(high * 32768 + next_random()) % k]
        while True:
            if next_random() % 2 == 0:
                if at.left is not None:
                    at = at.left
                else:
                    at.left = nodes[k]
                    break
            else:
                if at.right is not None:
                    at = at.right
                else:
                    at.right = nodes[k]
                    break
    return nodes[0]


def main():
    # 200 random trees of 1000 nodes, each asked from 400 starts, start s
    # of tree t being 1 + (37 s + t) % 1000
    check = 0
    for t in range(200):
        root = random_tree(1000)
        for s in range(400):
            check = (check * 31 + amount_of_time(root, 1 + (37 * s + t) % 1000)) % 1000000007
    print(f"200 trees of 1000, 400 starts each: checksum {check}")


main()
