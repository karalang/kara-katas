# Benchmark: LeetCode #988 Smallest String Starting From Leaf -- the ★
# arm, a walk carrying the path, on random trees of 8500 nodes,
# LeetCode's largest. Mirrors smallest_from_leaf.kara, .rs, .c and
# go-seq/.
import sys

sys.setrecursionlimit(20000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(t, path, best):
    path.append(chr(97 + t.val))
    if t.left is None and t.right is None:
        s = "".join(reversed(path))
        if best[0] is None or s < best[0]:
            best[0] = s
    else:
        if t.left is not None:
            walk(t.left, path, best)
        if t.right is not None:
            walk(t.right, path, best)
    path.pop()


def smallest_from_leaf(root):
    best = [None]
    walk(root, [], best)
    return best[0]


seed = 988


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n):
    root = TreeNode(next_random() % 4)
    for _ in range(1, n):
        node = TreeNode(next_random() % 4)
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
    rounds = 100
    trees = [random_tree(8500) for _ in range(20)]
    letters = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            s = smallest_from_leaf(trees[(r + i) % 20])
            letters += len(s)
            for ch in s:
                check = (check * 31 + ord(ch)) % 1000000007
    print(f"{rounds} rounds over 20 trees of 8500 nodes: {letters} letters, checksum {check}")


main()
