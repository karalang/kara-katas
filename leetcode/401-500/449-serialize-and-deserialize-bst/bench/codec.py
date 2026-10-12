# Benchmark for #449: mirror of codec.kara (preorder, rebuilt with
# bounds) on 10 random search trees of 50,000 values, built once, then
# serialized and deserialized 20 times over.
import sys


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def write_preorder(node, out):
    if node is not None:
        out.append(str(node.val))
        write_preorder(node.left, out)
        write_preorder(node.right, out)


def serialize(root):
    out = []
    write_preorder(root, out)
    return ",".join(out)


# Builds the subtree of values from low to high, both inclusive, taking
# them from values[at[0]] onward.
def build(values, at, low, high):
    if at[0] == len(values) or values[at[0]] < low or values[at[0]] > high:
        return None
    v = values[at[0]]
    at[0] += 1
    left = build(values, at, low, v - 1)
    right = build(values, at, v + 1, high)
    return TreeNode(v, left, right)


def deserialize(data):
    values = [int(token) for token in data.split(",")] if data else []
    return build(values, [0], -(1 << 63), (1 << 63) - 1)


def insert(root, v):
    fresh = TreeNode(v)
    if root is None:
        return fresh
    node = root
    while True:
        if v < node.val:
            if node.left is None:
                node.left = fresh
                break
            node = node.left
        else:
            if node.right is None:
                node.right = fresh
                break
            node = node.right
    return root


seed = 449


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    sys.setrecursionlimit(10000)
    trees = 10
    n = 50000
    rounds = 20
    roots = []
    for t in range(trees):
        # A shuffle of 0 to n - 1, spread out and shifted per tree.
        values = [i * 3 + t for i in range(n)]
        for i in range(n):
            r = next_random() * 32768
            r += next_random()
            j = i + r % (n - i)
            values[i], values[j] = values[j], values[i]
        root = None
        for v in values:
            root = insert(root, v)
        roots.append(root)
    characters = 0
    checksum = 0
    for _ in range(rounds):
        for root in roots:
            text = serialize(root)
            back = deserialize(text)
            top = back.val if back is not None else -1
            characters += len(text)
            checksum = (checksum * 31 + len(text) + top) % 1000000007
    print(f"{rounds} rounds on {trees} trees of {n}: {characters} characters, checksum {checksum}")


main()
