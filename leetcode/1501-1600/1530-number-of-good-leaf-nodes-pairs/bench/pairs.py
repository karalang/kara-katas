# LeetCode #1530: Number of Good Leaf Nodes Pairs -- bench: the ★ arm
# over 1000 random trees of 1 to 1024 nodes, built once and answered 10
# times, each with its own distance from 1 to 10.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def leaves_below(node, distance, pairs):
    counts = [0] * distance
    if node is not None:
        if node.left is None and node.right is None:
            counts[0] = 1
        else:
            l = leaves_below(node.left, distance, pairs)
            r = leaves_below(node.right, distance, pairs)
            for i in range(distance):
                for j in range(distance - i - 1):
                    pairs[0] += l[i] * r[j]
            for i in range(distance - 1):
                counts[i + 1] = l[i] + r[i]
    return counts


def count_pairs(root, distance):
    pairs = [0]
    leaves_below(root, distance, pairs)
    return pairs[0]


def make(at, vals, left, right):
    if at < 0:
        return None
    return TreeNode(vals[at], make(left[at], vals, left, right), make(right[at], vals, left, right))


seed = 1530


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def random_tree(most):
    n = next_random() % most + 1
    vals, left, right = [], [], []
    for i in range(n):
        vals.append(next_random() % 100 + 1)
        left.append(-1)
        right.append(-1)
        if i > 0:
            at = next_random() % i
            while True:
                if next_random() % 2 == 0:
                    if left[at] < 0:
                        left[at] = i
                        break
                    at = left[at]
                else:
                    if right[at] < 0:
                        right[at] = i
                        break
                    at = right[at]
    return make(0, vals, left, right)


def main():
    trees = []
    for _ in range(1000):
        root = random_tree(1024)
        trees.append((root, next_random() % 10 + 1))
    check = 0
    for _ in range(10):
        for root, distance in trees:
            check = mix(check, count_pairs(root, distance))
    print(f"10 passes over 1000 trees of up to 1024 nodes: checksum {check}")


main()
