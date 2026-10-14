# LeetCode #606: Construct String from Binary Tree -- Python mirror of the
# ★ arm (write it out); see tree2str.kara. The string is built as a list
# of parts and joined at the end.
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


# ---- test harness ---------------------------------------------------------

seed = 606


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(values):
        n = queue[head]
        head += 1
        if values[i] is not None:
            c = TreeNode(values[i])
            n.left = c
            queue.append(c)
        i += 1
        if i < len(values):
            if values[i] is not None:
                c = TreeNode(values[i])
                n.right = c
                queue.append(c)
            i += 1
    return root


def random_tree(size, lean):
    root = TreeNode(next_random() % 2001 - 1000)
    for _ in range(1, size):
        c = TreeNode(next_random() % 2001 - 1000)
        node = root
        while True:
            if next_random() % 100 < lean:
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
    return root


def written(values):
    return "[" + ",".join("null" if v is None else str(v) for v in values) + "]"


def show(name, values):
    print(f"{name}: {written(values)} -> {tree2str(from_level(values))}")


def summary(s):
    h = 0
    for c in s:
        h = (h * 31 + ord(c)) % 1000000007
    return f"{len(s)} characters, checksum {h}"


def main():
    show("example 1", [1, 2, 3, 4])
    show("example 2", [1, 2, 3, None, 4])
    show("one node", [7])
    show("a left child only", [1, 2])
    show("a right child only", [1, None, 2])
    show("a right chain", [1, None, 2, None, 3])
    show("a left chain", [1, 2, None, 3, None, 4])
    show("negative values", [-1, -2, -3, None, -5, -6])
    show("the problem's extremes", [1000, -1000, 0, None, -1000, 1000])
    count = 300
    nodes = 0
    length = 0
    h = 0
    for t in range(count):
        size = 1 + next_random() % 80
        lean = 50 if t % 3 == 0 else 80 if t % 3 == 1 else 95
        s = tree2str(random_tree(size, lean))
        nodes += size
        length += len(s)
        for c in s:
            h = (h * 31 + ord(c)) % 1000000007
    print(f"{count} random trees: {nodes} nodes, {length} characters, checksum {h}")
    print(f"10000 nodes at random: {summary(tree2str(random_tree(10000, 50)))}")
    top = TreeNode(0)
    last = top
    for v in range(1, 10000):
        c = TreeNode(v % 2001 - 1000)
        last.left = c
        last = c
    print(f"10000 nodes down the left: {summary(tree2str(top))}")
    start = TreeNode(0)
    end = start
    for v in range(1, 10000):
        c = TreeNode(v % 2001 - 1000)
        end.right = c
        end = c
    print(f"10000 nodes down the right: {summary(tree2str(start))}")
    print(f"a complete tree of 10000 nodes: {summary(tree2str(from_level([v % 2001 - 1000 for v in range(10000)])))}")


main()
