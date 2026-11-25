# LeetCode #1372 bench -- Python: one walk up from the leaves, each node
# reporting the longest zigzag starting at it going left and going right,
# each one more than its child's the other way.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lengths(node, best):
    left = right = 0
    if node.left is not None:
        left = 1 + lengths(node.left, best)[1]
    if node.right is not None:
        right = 1 + lengths(node.right, best)[0]
    best[0] = max(best[0], left, right)
    return left, right


def longest_zig_zag(root):
    best = [0]
    if root is not None:
        lengths(root, best)
    return best[0]


seed = 1372


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 trees of 5 * 10^4 nodes, the constraints' most, each node hung
    # on a random empty child place, built once; then 300 rounds, each
    # hanging one more leaf on one tree, on a place drawn from the
    # checksum so far, and finding that tree's longest zigzag
    roots = []
    places = []
    for _ in range(20):
        root = TreeNode(1)
        free = [(root, True), (root, False)]
        for _ in range(1, 50000):
            k = next_random() % len(free)
            parent, left = free[k]
            free[k] = free[-1]
            free.pop()
            node = TreeNode(1)
            if left:
                parent.left = node
            else:
                parent.right = node
            free.append((node, True))
            free.append((node, False))
        roots.append(root)
        places.append(free)
    check = 0
    for r in range(300):
        t = check % 20
        free = places[t]
        k = (check // 20) % len(free)
        parent, left = free[k]
        free[k] = free[-1]
        free.pop()
        node = TreeNode(1)
        if left:
            parent.left = node
        else:
            parent.right = node
        free.append((node, True))
        free.append((node, False))
        got = longest_zig_zag(roots[t])
        check = (check * 31 + got + r) % 1000000007
    print(f"300 rounds over 20 trees of 50000 nodes: checksum {check}")


main()
