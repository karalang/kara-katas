# Benchmark: LeetCode #993 Cousins in Binary Tree -- the ★ arm, a
# breadth-first search a level at a time, on random trees of 100 nodes,
# LeetCode's largest. Mirrors is_cousins.kara, .rs, .c and go-seq/.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def is_cousins(root, x, y):
    level = [(root, -1)]
    while level:
        px = -1
        py = -1
        nxt = []
        for node, parent in level:
            if node.val == x:
                px = parent
            if node.val == y:
                py = parent
            if node.left is not None:
                nxt.append((node.left, node.val))
            if node.right is not None:
                nxt.append((node.right, node.val))
        if px >= 0 and py >= 0:
            return px != py
        if px >= 0 or py >= 0:
            return False
        level = nxt
    return False


seed = 993


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n):
    vals = list(range(1, n + 1))
    i = n - 1
    while i > 0:
        j = next_random() % (i + 1)
        vals[i], vals[j] = vals[j], vals[i]
        i -= 1
    root = TreeNode(vals[0])
    for k in range(1, n):
        node = TreeNode(vals[k])
        cur = root
        while True:
            if next_random() % 2 == 0:
                if cur.left is not None:
                    cur = cur.left
                else:
                    cur.left = node
                    break
            else:
                if cur.right is not None:
                    cur = cur.right
                else:
                    cur.right = node
                    break
    return root


def main():
    rounds = 500
    trees = [random_tree(100) for _ in range(20)]
    found = 0
    check = 0
    for r in range(rounds):
        for t in range(20):
            d = 1 + (r * 7 + t) % 99
            for x in range(1, 101):
                y = 1 + (x - 1 + d) % 100
                got = is_cousins(trees[(r + t) % 20], x, y)
                if got:
                    found += 1
                check = (check * 31 + (2 if got else 1)) % 1000000007
    print(f"{rounds} rounds over 20 trees of 100 nodes: {found} cousin pairs, checksum {check}")


main()
