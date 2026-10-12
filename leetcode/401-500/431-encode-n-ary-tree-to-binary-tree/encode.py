# LeetCode #431: Encode N-ary Tree to Binary Tree -- mirror of
# encode.kara (left child, right sibling).
import sys

sys.setrecursionlimit(10000)


class Node:
    def __init__(self, val, children=None):
        self.val = val
        self.children = children if children is not None else []


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def encode(root):
    if root is None:
        return None
    return encode_node(root)


def encode_node(node):
    t = TreeNode(node.val)
    prev = None
    for child in node.children:
        c = encode_node(child)
        if prev is None:
            t.left = c
        else:
            prev.right = c
        prev = c
    return t


def decode(root):
    if root is None:
        return None
    return decode_node(root)


def decode_node(t):
    children = []
    child = t.left
    while child is not None:
        children.append(decode_node(child))
        child = child.right
    return Node(t.val, children)


def leaf(val):
    return Node(val)


def tree(val, children):
    return Node(val, children)


def shape(root):
    if root is None:
        return "empty"
    out = []

    def draw(node):
        out.append(f"{node.val}")
        if node.children:
            out.append("(")
            for i, child in enumerate(node.children):
                if i > 0:
                    out.append(" ")
                draw(child)
            out.append(")")

    draw(root)
    return "".join(out)


def bshape(root):
    out = []

    def draw(t):
        if t is None:
            out.append("-")
            return
        out.append(f"{t.val}")
        if t.left is not None or t.right is not None:
            out.append("(")
            draw(t.left)
            out.append(",")
            draw(t.right)
            out.append(")")

    draw(root)
    return "".join(out)


def round_trip(root):
    before = shape(root)
    binary = encode(root)
    back = decode(binary)
    after = shape(back)
    again = encode(back)
    ok = after == before and bshape(again) == bshape(binary)
    return after + ("" if ok else " FAILED")


seed = 431


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build_random(i, vals, kids):
    return Node(vals[i], [build_random(k, vals, kids) for k in kids[i]])


def random_tree(n):
    if n == 0:
        return None
    vals = []
    kids = []
    reach = 1 + step() % n
    for i in range(n):
        vals.append(step() % 10001)
        kids.append([])
        if i > 0:
            back = 1 + step() % min(i, reach)
            kids[i - back].append(i)
    return build_random(0, vals, kids)


def main():
    print(round_trip(tree(1, [tree(3, [leaf(5), leaf(6)]), leaf(2), leaf(4)])))
    print(round_trip(tree(1, [
        leaf(2),
        tree(3, [leaf(6), tree(7, [tree(11, [leaf(14)])])]),
        tree(4, [tree(8, [leaf(12)])]),
        tree(5, [tree(9, [leaf(13)]), leaf(10)]),
    ])))
    print(round_trip(None))
    print(round_trip(leaf(0)))
    print(round_trip(leaf(10000)))
    print(round_trip(tree(1, [tree(2, [tree(3, [tree(4, [leaf(5)])])])])))
    print(round_trip(tree(100, [leaf(v * 7) for v in range(12)])))
    print(round_trip(tree(0, [leaf(0), tree(0, [leaf(0)]), leaf(0)])))
    nodes = 0
    failed = 0
    checksum = 0
    for _ in range(300):
        n = step() % 61
        line = round_trip(random_tree(n))
        nodes += n
        if line.endswith(" FAILED"):
            failed += 1
        for b in line.encode():
            checksum = (checksum * 31 + b) % 1000000007
    print(f"300 random trees, {nodes} nodes: {failed} failed, checksum {checksum}")


main()
