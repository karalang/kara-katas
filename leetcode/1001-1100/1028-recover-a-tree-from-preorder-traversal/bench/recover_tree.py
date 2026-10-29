# LeetCode #1028: Recover a Tree From Preorder Traversal -- bench
# Mirrors ./recover_tree.kara; see ../README.md § Benchmarks.

import sys

sys.setrecursionlimit(10000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def recover_from_preorder(traversal):
    data = traversal.encode()
    path = []
    i = 0
    while i < len(data):
        depth = 0
        while data[i] == 45:
            depth += 1
            i += 1
        value = 0
        while i < len(data) and data[i] != 45:
            value = value * 10 + (data[i] - 48)
            i += 1
        node = TreeNode(value)
        while len(path) > depth:
            path.pop()
        if path:
            parent = path[-1]
            if parent.left is None:
                parent.left = node
            else:
                parent.right = node
        path.append(node)
    return path[0] if path else None


# a fold of the tree's values and shape
def digest(node):
    if node is None:
        return 1
    return (node.val + 3 * digest(node.left) + 7 * digest(node.right)) % 1000000007


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_value(seed, top):
    a = next_random(seed)
    b = next_random(seed)
    return (a * 32768 + b) % top + 1


def write(at, depth, vals, left, right, out):
    out.append("-" * depth)
    out.append(str(vals[at]))
    if left[at] >= 0:
        write(left[at], depth + 1, vals, left, right, out)
    if right[at] >= 0:
        write(right[at], depth + 1, vals, left, right, out)


def make_traversal(seed, n):
    vals, left, right = [], [], []
    for k in range(n):
        v = random_value(seed, 1000000000)
        vals.append(v)
        left.append(-1)
        right.append(-1)
        at = 0
        while k > 0:
            if v < vals[at]:
                if left[at] < 0:
                    left[at] = k
                    break
                at = left[at]
            else:
                if right[at] < 0:
                    right[at] = k
                    break
                at = right[at]
    out = []
    write(0, 0, vals, left, right, out)
    return "".join(out)


def main():
    count, rounds = 200, 50
    seed = [1028]
    traversals = []
    letters = 0
    for _ in range(count):
        s = make_traversal(seed, 1000)
        letters += len(s)
        traversals.append(s)
    check = 0
    for _ in range(rounds):
        for s in traversals:
            check = (check * 131 + digest(recover_from_preorder(s))) % 1000000007
    print(f"{count} traversals of 1000 nodes, {letters} letters, {rounds} rounds: checksum {check}")


main()
