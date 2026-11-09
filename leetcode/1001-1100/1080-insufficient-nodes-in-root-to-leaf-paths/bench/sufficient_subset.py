# Benchmark: LeetCode #1080 Insufficient Nodes in Root to Leaf Paths --
# the ★ arm. Mirrors sufficient_subset.kara, .rs, .c and go-seq/.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def prune(node, need):
    if node is None:
        return None
    if node.left is None and node.right is None:
        return node if node.val >= need else None
    node.left = prune(node.left, need - node.val)
    node.right = prune(node.right, need - node.val)
    return None if node.left is None and node.right is None else node


def sufficient_subset(root, limit):
    return prune(root, limit)


seed = 1080


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_shape(n):
    val, left, right = [], [], []
    for k in range(n):
        val.append(next_random() % 201 - 100)
        left.append(-1)
        right.append(-1)
        if k > 0:
            at = 0
            while True:
                if next_random() % 2 == 0:
                    if left[at] < 0:
                        left[at] = k
                        break
                    at = left[at]
                else:
                    if right[at] < 0:
                        right[at] = k
                        break
                    at = right[at]
    return val, left, right


def build(s, k):
    if k < 0:
        return None
    return TreeNode(s[0][k], build(s, s[1][k]), build(s, s[2][k]))


def count(t):
    return 0 if t is None else 1 + count(t.left) + count(t.right)


def main():
    rounds = 100
    shapes = [random_shape(1000) for _ in range(200)]
    kept = 0
    check = 0
    for r in range(rounds):
        for i in range(200):
            limit = (r * 37 + i * 11) % 401 - 200
            k = count(sufficient_subset(build(shapes[i], 0), limit))
            kept += k
            check = (check * 31 + k + i) % 1000000007
    print(f"{rounds} rounds over 200 trees of 1000 nodes: {kept} nodes kept, checksum {check}")


main()
