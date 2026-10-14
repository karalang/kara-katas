# Benchmark for #606: Python mirror of the ★ arm (write it out); see
# tree2str.kara. The string is built as a list of parts and joined.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def write(node, out):
    out.append(str(node.val))
    if node.left is not None or node.right is not None:
        out.append("(")
        if node.left is not None:
            write(node.left, out)
        out.append(")")
    if node.right is not None:
        out.append("(")
        write(node.right, out)
        out.append(")")


def tree2str(root):
    out = []
    if root is not None:
        write(root, out)
    return "".join(out)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    trees = 20
    rounds = 200
    seed = [606]
    all_nodes = []
    for g in range(trees):
        lean = 50 + 2 * g
        root = TreeNode(next_random(seed) % 2001 - 1000)
        nodes = [root]
        for _ in range(1, 10000):
            c = TreeNode(next_random(seed) % 2001 - 1000)
            node = root
            while True:
                if next_random(seed) % 100 < lean:
                    if node.left is not None:
                        node = node.left
                    else:
                        node.left = c
                        break
                else:
                    if node.right is not None:
                        node = node.right
                    else:
                        node.right = c
                        break
            nodes.append(c)
        all_nodes.append(nodes)
    length = 0
    checksum = 0
    for r in range(rounds):
        for t in range(trees):
            k = (r * 37 + t * 11) % 16
            s = tree2str(all_nodes[t][k])
            length += len(s)
            for i, c in enumerate(s):
                if i % 101 == 0:
                    checksum = (checksum * 31 + ord(c)) % 1000000007
    print(f"{trees} trees, {rounds} times each: {length} characters, checksum {checksum}")


main()
