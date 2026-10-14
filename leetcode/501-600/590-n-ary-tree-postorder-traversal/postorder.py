# LeetCode #590: N-ary Tree Postorder Traversal -- Python mirror of the
# ★ arm (recursion); see postorder.kara.
import sys

sys.setrecursionlimit(10000)


class Node:
    __slots__ = ("val", "children")

    def __init__(self, val, children):
        self.val = val
        self.children = children


def walk(node, out):
    for child in node.children:
        walk(child, out)
    out.append(node.val)


def postorder(root):
    out = []
    if root is not None:
        walk(root, out)
    return out


# ---- test harness ---------------------------------------------------------

def leaf(val):
    return Node(val, [])


def tree(val, children):
    return Node(val, children)


seed = 0


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


def checksum_of(vals):
    checksum = 0
    for v in vals:
        checksum = (checksum * 31 + v) % 1000000007
    return checksum


def show(name, root):
    print(f"{name}: {postorder(root)}")


def show_long(name, root):
    got = postorder(root)
    print(f"{name}: {len(got)} values, first {got[0:5]}, checksum {checksum_of(got)}")


def main():
    global seed
    show("[1,null,3,2,4,null,5,6]", tree(1, [tree(3, [leaf(5), leaf(6)]), leaf(2), leaf(4)]))
    show("example 2", tree(1, [
        leaf(2),
        tree(3, [leaf(6), tree(7, [tree(11, [leaf(14)])])]),
        tree(4, [tree(8, [leaf(12)])]),
        tree(5, [tree(9, [leaf(13)]), leaf(10)]),
    ]))
    show("empty", None)
    show("one node", leaf(7))
    show("repeated values", tree(4, [leaf(4), tree(4, [leaf(0), leaf(4)]), leaf(0)]))
    show("last child deepest", tree(0, [leaf(1), tree(2, [leaf(3)]), tree(4, [tree(5, [leaf(6)])])]))
    path = leaf(999)
    for v in range(999):
        path = tree(998 - v, [path])
    show_long("a path of 1000", path)
    wide = [leaf(9999 - v) for v in range(9999)]
    show_long("a root with 9999 leaves", tree(10000, wide))
    seed = 590
    nodes = 0
    checksum = 0
    for _ in range(300):
        n = step() % 61
        got = postorder(random_tree(n))
        nodes += len(got)
        checksum = (checksum * 1000003 + checksum_of(got)) % 1000000007
    print(f"300 random trees: {nodes} values, checksum {checksum}")


main()
