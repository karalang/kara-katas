# Benchmark for #428: mirror of codec.kara (preorder with child counts).
import sys

sys.setrecursionlimit(100000)


class Node:
    __slots__ = ("val", "children")

    def __init__(self, val, children):
        self.val = val
        self.children = children


def write(node, out):
    out.append(f"{node.val} {len(node.children)}")
    for child in node.children:
        write(child, out)


def serialize(root):
    out = []
    if root is not None:
        write(root, out)
    return " ".join(out)


def read(words, at):
    val = int(words[at[0]])
    count = int(words[at[0] + 1])
    at[0] += 2
    return Node(val, [read(words, at) for _ in range(count)])


def deserialize(data):
    if len(data) == 0:
        return None
    return read(data.split(" "), [0])


seed = 428


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build_random(i, vals, kids):
    return Node(vals[i], [build_random(k, vals, kids) for k in kids[i]])


def total(node):
    s = node.val
    for child in node.children:
        s += total(child)
    return s


def main():
    n = 10000
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    chars = 0
    checksum = 0
    for _ in range(rounds):
        reach = 1 + step() % 1000
        vals = []
        kids = []
        for i in range(n):
            vals.append(step() % 10001)
            kids.append([])
            if i > 0:
                back = 1 + step() % min(i, reach)
                kids[i - back].append(i)
        tree = build_random(0, vals, kids)
        text = serialize(tree)
        back = deserialize(text)
        chars += len(text)
        checksum = (checksum * 31 + len(text) + total(back)) % 1000000007
    print(f"{rounds} rounds of {n} nodes: {chars} characters, checksum {checksum}")


main()
