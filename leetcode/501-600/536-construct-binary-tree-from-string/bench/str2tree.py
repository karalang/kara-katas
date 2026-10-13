# Benchmark for #536: the star arm (recursive descent); see ../README.md
# section Benchmarks. Mirrors str2tree.kara.
import sys


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def parse(b, i):
    """The tree that starts at byte i[0], leaving i[0] just past it."""
    sign = 1
    if b[i[0]] == 45:
        sign = -1
        i[0] += 1
    val = 0
    while i[0] < len(b) and 48 <= b[i[0]] <= 57:
        val = val * 10 + b[i[0]] - 48
        i[0] += 1
    node = TreeNode(sign * val)
    if i[0] < len(b) and b[i[0]] == 40:
        i[0] += 1
        node.left = parse(b, i)
        i[0] += 1
    if i[0] < len(b) and b[i[0]] == 40:
        i[0] += 1
        node.right = parse(b, i)
        i[0] += 1
    return node


def str2tree(s):
    if not s:
        return None
    return parse(s, [0])


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


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


def render(n, out):
    if n is None:
        return
    out.append(str(n.val))
    if n.left is not None:
        out.append("(")
        render(n.left, out)
        out.append(")")
    if n.right is not None:
        out.append("(")
        render(n.right, out)
        out.append(")")


def walk(n, stats):
    if n is None:
        return
    stats[0] += 1
    stats[1] = (stats[1] * 31 + n.val + 1000) % 1000000007
    walk(n.left, stats)
    walk(n.right, stats)


def main():
    rng = Rng(536)
    strings = []
    for _ in range(20):
        out = []
        render(random_tree(rng, 5500), out)
        strings.append("".join(out).encode())
    rounds = 100
    stats = [0, 0]
    for _ in range(rounds):
        for s in strings:
            walk(str2tree(s), stats)
    print(f"{len(strings)} strings, {rounds} rounds: {stats[0]} nodes, checksum {stats[1]}")


sys.setrecursionlimit(100000)
main()
