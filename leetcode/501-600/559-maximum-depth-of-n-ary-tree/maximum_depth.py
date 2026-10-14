# LeetCode #559: Maximum Depth of N-ary Tree -- Python mirror of the ★
# arm (recursion); see maximum_depth.kara. A node is (val, children).
import sys

sys.setrecursionlimit(10000)


def depth(node):
    deepest = 0
    for child in node[1]:
        deepest = max(deepest, depth(child))
    return deepest + 1


def max_depth(root):
    return 0 if root is None else depth(root)


# ---- test harness ----------------------------------------------------------


def leaf(val):
    return (val, [])


def tree(val, children):
    return (val, children)


class Seed:
    def __init__(self, v):
        self.v = v

    def step(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def build_random(i, vals, kids):
    return (vals[i], [build_random(k, vals, kids) for k in kids[i]])


def random_tree(n, seed):
    if n == 0:
        return None
    vals = []
    kids = []
    reach = 1 + seed.step() % n
    for i in range(n):
        vals.append(seed.step() % 10001)
        kids.append([])
        if i > 0:
            back = 1 + seed.step() % min(i, reach)
            kids[i - back].append(i)
    return build_random(0, vals, kids)


def show(name, root):
    print(f"{name}: {max_depth(root)}")


def main():
    show("[1,null,3,2,4,null,5,6]", tree(1, [tree(3, [leaf(5), leaf(6)]), leaf(2), leaf(4)]))
    show("example 2", tree(1, [
        leaf(2),
        tree(3, [leaf(6), tree(7, [tree(11, [leaf(14)])])]),
        tree(4, [tree(8, [leaf(12)])]),
        tree(5, [tree(9, [leaf(13)]), leaf(10)]),
    ]))
    show("empty", None)
    show("one node", leaf(7))
    path = leaf(999)
    for v in range(999):
        path = tree(998 - v, [path])
    show("a path of 1000", path)
    show("a root with 9999 leaves", tree(0, [leaf(v) for v in range(9999)]))
    show("deepest last", tree(0, [leaf(1), tree(2, [leaf(4)]), tree(3, [tree(5, [leaf(6)])])]))
    seed = Seed(559)
    nodes = 0
    total = 0
    checksum = 0
    for _ in range(300):
        n = seed.step() % 61
        d = max_depth(random_tree(n, seed))
        nodes += n
        total += d
        checksum = (checksum * 31 + d) % 1000000007
    print(f"300 random trees, {nodes} nodes: depths sum to {total}, checksum {checksum}")


main()
