# LeetCode #538: Convert BST to Greater Tree -- Python mirror of the ★
# arm (reverse in order, recursively); see convert_bst.kara.
import sys

sys.setrecursionlimit(30000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def visit(node, total):
    if node is not None:
        visit(node.right, total)
        total[0] += node.val
        node.val = total[0]
        visit(node.left, total)


def convert_bst(root):
    visit(root, [0])
    return root


# ---- test harness ---------------------------------------------------------

seed = 538


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    for v in values[1:]:
        node = root
        while True:
            if v < node.val:
                if node.left is None:
                    node.left = TreeNode(v)
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = TreeNode(v)
                    break
                node = node.right
    return root


def level_order(root):
    out = []
    queue = [root]
    head = 0
    while head < len(queue):
        n = queue[head]
        if n is not None:
            out.append(n.val)
            queue.append(n.left)
            queue.append(n.right)
        else:
            out.append(None)
        head += 1
    while out and out[-1] is None:
        out.pop()
    return out


def written(root):
    return "[" + ",".join("null" if v is None else str(v) for v in level_order(root)) + "]"


def mix(h, root):
    for v in level_order(root):
        x = 7 if v is None else v + 1000000000
        h = (h * 31 + x) % 1000000007
    return h


def show(name, values):
    root = build(values)
    before = written(root)
    print(f"{name}: {before} -> {written(convert_bst(root))}")


def main():
    show("example 1", [4, 1, 6, 0, 2, 5, 7, 3, 8])
    show("example 2", [0, 1])
    show("one node", [5])
    show("no nodes", [])
    show("negative values", [-3, -5, -1, -4, -2])
    show("both ends of the range", [0, -10000, 10000, -1, 1])
    show("falling chain", [5, 4, 3, 2, 1])
    show("rising chain", [1, 2, 3, 4, 5])
    pool = list(range(-10000, 10001))
    count = 300
    total = 0
    h = 0
    for _ in range(count):
        size = next_random() % 81
        values = []
        for i in range(size):
            j = i + (next_random() * 32768 + next_random()) % (20001 - i)
            pool[i], pool[j] = pool[j], pool[i]
            values.append(pool[i])
        total += size
        h = mix(h, convert_bst(build(values)))
    print(f"{count} random trees: {total} values, checksum {h}")
    values = list(range(-5000, 5000))
    for i in range(9999, 0, -1):
        j = (next_random() * 32768 + next_random()) % (i + 1)
        values[i], values[j] = values[j], values[i]
    root = convert_bst(build(values))
    print(f"10000 values in a random order: root {root.val}, checksum {mix(0, root)}")
    top = TreeNode(1)
    last = top
    for v in range(2, 10001):
        nxt = TreeNode(v)
        last.right = nxt
        last = nxt
    root = convert_bst(top)
    print(f"a chain of 10000: top {top.val}, bottom {last.val}, checksum {mix(0, root)}")


main()
