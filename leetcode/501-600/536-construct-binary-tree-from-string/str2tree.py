# LeetCode #536: Construct Binary Tree from String -- recursive descent.
# Mirrors str2tree.kara and its harness.
import sys
import threading
from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def parse(b, i):
    """The tree that starts at byte i[0], leaving i[0] just past it."""
    sign = 1
    if b[i[0]] == ord("-"):
        sign = -1
        i[0] += 1
    val = 0
    while i[0] < len(b) and ord("0") <= b[i[0]] <= ord("9"):
        val = val * 10 + b[i[0]] - ord("0")
        i[0] += 1
    node = TreeNode(sign * val)
    if i[0] < len(b) and b[i[0]] == ord("("):
        i[0] += 1
        node.left = parse(b, i)
        i[0] += 1
    if i[0] < len(b) and b[i[0]] == ord("("):
        i[0] += 1
        node.right = parse(b, i)
        i[0] += 1
    return node


def str2tree(s):
    if not s:
        return None
    return parse(s.encode(), [0])


# ---- test harness

class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def level_order(root):
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append("null")
        else:
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] == "null":
        out.pop()
    return "[" + ",".join(out) + "]"


def render(node, out):
    if node is None:
        return
    out.append(str(node.val))
    if node.left is not None:
        out.append("(")
        render(node.left, out)
        out.append(")")
    if node.right is not None:
        out.append("(")
        render(node.right, out)
        out.append(")")


def written(root):
    out = []
    render(root, out)
    return "".join(out)


def shape(node, depth, stats):
    if node is None:
        return
    stats[0] += 1
    stats[1] = max(stats[1], depth)
    stats[2] = (stats[2] * 31 + node.val + 1000) % 1000000007
    shape(node.left, depth + 1, stats)
    shape(node.right, depth + 1, stats)


def random_tree(rng, n):
    if n == 0:
        return None
    val = rng.next() % 2001 - 1000
    rest = n - 1
    if rest == 0:
        left = 0
    elif rng.next() % 3 == 0:
        left = rest
    else:
        left = 1 + rng.next() % rest
    l = random_tree(rng, left)
    r = random_tree(rng, rest - left)
    return TreeNode(val, l, r)


def b(x):
    return "true" if x else "false"


def show(s):
    tree = str2tree(s)
    print(f'"{s}" -> {level_order(tree)}, written back {b(written(tree) == s)}')


def main():
    show("4(2(3)(1))(6(5))")
    show("4(2(3)(1))(6(5)(7))")
    show("-4(2(3)(1))(6(5)(7))")
    show("")
    show("7")
    show("-0")
    show("0(-12)(345)")
    show("1(2)")
    show("1(2(3(4(5))))")
    show("-1(-2(-3)(-4))(-5(-6)(-7))")
    rng = Rng(536)
    back = 0
    stats = [0, 0, 0]
    for _ in range(300):
        n = rng.next() % 61
        tree = random_tree(rng, n)
        s = written(tree)
        read = str2tree(s)
        if written(read) == s and level_order(read) == level_order(tree):
            back += 1
        shape(read, 0, stats)
    print(f"300 random trees: {back} read back, {stats[0]} nodes, checksum {stats[2]}")
    tree = random_tree(rng, 5500)
    s = written(tree)
    stats = [0, 0, 0]
    shape(str2tree(s), 0, stats)
    print(f"{len(s)} characters, random: {stats[0]} nodes, height {stats[1]}, checksum {stats[2]}, written back {b(written(str2tree(s)) == s)}")
    chain = []
    for i in range(5000):
        chain.append(str(i % 10))
        if i < 4999:
            chain.append("(")
    chain.append(")" * 4999)
    chain = "".join(chain)
    stats = [0, 0, 0]
    shape(str2tree(chain), 0, stats)
    print(f"{len(chain)} characters, chain: {stats[0]} nodes, height {stats[1]}, checksum {stats[2]}")


sys.setrecursionlimit(100000)
threading.stack_size(512 * 1024 * 1024)
t = threading.Thread(target=main)
t.start()
t.join()
