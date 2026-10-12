# Benchmark for #431: mirror of encode.kara (left child, right sibling).
import sys

sys.setrecursionlimit(100000)


class Node:
    __slots__ = ("val", "children")

    def __init__(self, val, children):
        self.val = val
        self.children = children


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


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


def decode_node(t):
    children = []
    child = t.left
    while child is not None:
        children.append(decode_node(child))
        child = child.right
    return Node(t.val, children)


seed = 431


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build_random(i, vals, kids):
    return Node(vals[i], [build_random(k, vals, kids) for k in kids[i]])


def main():
    n = 10000
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    count = 0
    checksum = 0
    for _ in range(rounds):
        reach = 10 + step() % 1000
        vals = []
        kids = []
        for i in range(n):
            vals.append(step() % 10001)
            kids.append([])
            if i > 0:
                back = 1 + step() % min(i, reach)
                kids[i - back].append(i)
        back = decode_node(encode_node(build_random(0, vals, kids)))
        stack = [back]
        while stack:
            node = stack.pop()
            count += 1
            checksum = (checksum * 31 + node.val) % 1000000007
            stack.extend(reversed(node.children))
    print(f"{rounds} rounds of {n} nodes: {count} decoded, checksum {checksum}")


main()
