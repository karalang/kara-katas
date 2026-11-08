# LeetCode #1522: Diameter of N-Ary Tree -- bench: the ★ arm over 1000
# random trees of 1 to 2000 nodes, built once and answered 20 times.
import sys

sys.setrecursionlimit(100000)


class Node:
    __slots__ = ("val", "children")

    def __init__(self, val, children):
        self.val = val
        self.children = children


def height(node, best):
    first = second = 0
    for child in node.children:
        h = height(child, best) + 1
        if h > first:
            second, first = first, h
        elif h > second:
            second = h
    best[0] = max(best[0], first + second)
    return first


def diameter(root):
    best = [0]
    height(root, best)
    return best[0]


def build(vals, kids):
    n = len(vals)
    made = [None] * n
    for i in range(n - 1, -1, -1):
        made[i] = Node(vals[i], [made[c] for c in kids[i]])
    return made[0]


seed = 1522


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    count = 1000
    trees = []
    for _ in range(count):
        n = next_random() % 2000 + 1
        window = next_random() % 64 + 1
        vals = []
        kids = [[] for _ in range(n)]
        for i in range(n):
            vals.append(next_random() % 1000)
            if i > 0:
                kids[i - 1 - next_random() % min(i, window)].append(i)
        trees.append(build(vals, kids))
    check = 0
    total = 0
    for _ in range(20):
        for tree in trees:
            d = diameter(tree)
            total += d
            check = mix(check, d)
    print(f"20 passes over 1000 trees of up to 2000 nodes: diameters sum to {total}, checksum {check}")


main()
