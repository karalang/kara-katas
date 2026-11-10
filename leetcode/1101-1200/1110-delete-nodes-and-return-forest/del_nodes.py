# LeetCode #1110: Delete Nodes And Return Forest -- the Python mirror of
# the ★ arm: one walk from the root, each call told whether its node's
# parent is gone. Prints the same lines as every Kāra arm.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def prune(node, parent_gone, gone, roots):
    if node is None:
        return None
    deleted = node.val in gone
    if parent_gone and not deleted:
        roots.append(node)
    node.left = prune(node.left, deleted, gone, roots)
    node.right = prune(node.right, deleted, gone, roots)
    return None if deleted else node


def del_nodes(root, to_delete):
    gone = set(to_delete)
    roots = []
    prune(root, True, gone, roots)
    return roots


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def parse(text):
    inner = text[1:-1]
    if inner == "":
        return None
    items = [None if s == "null" else int(s) for s in inner.split(",")]
    root = TreeNode(items[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(items):
        node = queue[head]
        head += 1
        if items[i] is not None:
            child = TreeNode(items[i])
            node.left = child
            queue.append(child)
        i += 1
        if i < len(items):
            if items[i] is not None:
                child = TreeNode(items[i])
                node.right = child
                queue.append(child)
            i += 1
    return root


def written(root):
    out = []
    queue = [root]
    head = 0
    while head < len(queue):
        n = queue[head]
        if n is not None:
            out.append(str(n.val))
            queue.append(n.left)
            queue.append(n.right)
        else:
            out.append("null")
        head += 1
    while out and out[-1] == "null":
        out.pop()
    return "[" + ",".join(out) + "]"


def forest(roots):
    trees = sorted(((r.val, written(r)) for r in roots), key=lambda t: t[0])
    return "[" + ",".join(t[1] for t in trees) + "]"


def random_tree(size):
    pool = list(range(1, 1001))
    for i in range(size):
        j = i + next_random() % (1000 - i)
        pool[i], pool[j] = pool[j], pool[i]
    root = TreeNode(pool[0])
    nodes = [root]
    for i in range(1, size):
        while True:
            at = nodes[next_random() % len(nodes)]
            if next_random() % 2 == 0:
                if at.left is None:
                    c = TreeNode(pool[i])
                    at.left = c
                    nodes.append(c)
                    break
            elif at.right is None:
                c = TreeNode(pool[i])
                at.right = c
                nodes.append(c)
                break
    return written(root), pool[:size]


def fold(h, text):
    for b in text.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    global seed
    cases = [
        ("[1,2,3,4,5,6,7]", [3, 5]),
        ("[1,2,4,null,3]", [3]),
        ("[1,2,3]", [1]),
        ("[1,2,3]", []),
        ("[1,2,3]", [1, 2, 3]),
        ("[7]", [7]),
        ("[7]", [8]),
        ("[1,null,2,null,3,null,4]", [2, 4]),
        ("[5,3,8,1,4,7,9]", [3, 8]),
        ("[10,20,30,40,null,null,50]", [20, 50, 999]),
    ]
    for text, to_delete in cases:
        print(f"{text} without {to_delete} -> {forest(del_nodes(parse(text), list(to_delete)))}")
    seed = 1110
    trees = 0
    check = 0
    for _ in range(2000):
        size = next_random() % 40 + 1
        text, values = random_tree(size)
        to_delete = [v for v in values if next_random() % 3 == 0]
        roots = del_nodes(parse(text), to_delete)
        trees += len(roots)
        check = fold(check, forest(roots))
    print(f"2000 random trees: {trees} trees left, checksum {check}")
    text, values = random_tree(1000)
    to_delete = [v for v in values if v % 2 == 0]
    roots = del_nodes(parse(text), to_delete)
    print(f"1000 nodes, the even values deleted: {len(roots)} trees, checksum {fold(0, forest(roots))}")
    chain = ["1" if v == 1 else f"null,{v}" for v in range(1, 1001)]
    text = "[" + ",".join(chain) + "]"
    to_delete = [v for v in range(1, 1001) if v % 3 == 0]
    roots = del_nodes(parse(text), to_delete)
    print(f"a chain of 1000, every third deleted: {len(roots)} trees, checksum {fold(0, forest(roots))}")


main()
