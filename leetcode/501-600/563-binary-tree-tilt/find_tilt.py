# LeetCode #563: Binary Tree Tilt -- Python mirror of the ★ arm (subtree
# sums, recursively); see find_tilt.kara.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def subtree_sum(node, total):
    if node is None:
        return 0
    l = subtree_sum(node.left, total)
    r = subtree_sum(node.right, total)
    total[0] += abs(l - r)
    return node.val + l + r


def find_tilt(root):
    total = [0]
    subtree_sum(root, total)
    return total[0]


# ---- test harness ---------------------------------------------------------

seed = 563


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
    print(f"{name}: {written(values)} -> {find_tilt(from_level(values))}")


def main():
    show("example 1", [1, 2, 3])
    show("example 2", [4, 2, 9, 3, 5, None, 7])
    show("example 3", [21, 7, 14, 1, 1, 2, 2, 3, 3])
    show("no nodes", [])
    show("one node", [7])
    show("a left chain", [1, 2, None, 3, None, 4])
    show("negative values", [-1, -2, -3, -4, -5, -6, -7])
    show("the problem's extremes", [1000, -1000, 1000, None, -1000, 1000])
    count = 300
    nodes = 0
    total = 0
    h = 0
    for t in range(count):
        size = 1 + next_random() % 80
        lean = 50 if t % 3 == 0 else 80 if t % 3 == 1 else 95
        tilt = find_tilt(random_tree(size, lean))
        nodes += size
        total += tilt
        h = (h * 31 + tilt) % 1000000007
    print(f"{count} random trees: {nodes} nodes, tilts {total}, checksum {h}")
    print(f"10000 nodes at random: {find_tilt(random_tree(10000, 50))}")
    top = TreeNode(0)
    last = top
    for v in range(1, 10000):
        c = TreeNode(v % 2001 - 1000)
        last.left = c
        last = c
    print(f"10000 nodes down the left: {find_tilt(top)}")
    root = TreeNode(0)
    l = root
    r = root
    for v in range(1, 10000):
        c = TreeNode(v % 2001 - 1000)
        if v % 2 == 1:
            l.left = c
            l = c
        else:
            r.right = c
            r = c
    print(f"two chains of 10000 nodes: {find_tilt(root)}")
    print(f"a complete tree of 10000 nodes: {find_tilt(from_level([v % 2001 - 1000 for v in range(10000)]))}")


main()
