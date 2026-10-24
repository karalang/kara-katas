# Benchmark: LeetCode #987 Vertical Order Traversal of a Binary Tree --
# the ★ arm, every node's place sorted, on random trees of 1000 nodes,
# LeetCode's largest. Mirrors vertical_traversal.kara, .rs, .c and
# go-seq/.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(t, row, col, out):
    if t is not None:
        out.append((col, row, t.val))
        walk(t.left, row + 1, col - 1, out)
        walk(t.right, row + 1, col + 1, out)


def vertical_traversal(root):
    places = []
    walk(root, 0, 0, places)
    places.sort()
    out = []
    last = 0
    for col, _, val in places:
        if not out or col != last:
            out.append([])
            last = col
        out[-1].append(val)
    return out


seed = 987


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n):
    root = TreeNode(next_random() % 1001)
    for _ in range(1, n):
        node = TreeNode(next_random() % 1001)
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
    trees = [random_tree(1000) for _ in range(20)]
    columns = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            cols = vertical_traversal(trees[(r + i) % 20])
            columns += len(cols)
            mid = cols[len(cols) // 2]
            check = (check * 31 + len(mid) + mid[0]) % 1000000007
    print(f"{rounds} rounds over 20 trees of 1000 nodes: {columns} columns, checksum {check}")


main()
