# LeetCode #543: Diameter of Binary Tree -- Python mirror of the ★ arm
# (heights, recursively); see diameter_of_binary_tree.kara.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def height(node, best):
    if node is None:
        return 0
    l = height(node.left, best)
    r = height(node.right, best)
    if l + r > best[0]:
        best[0] = l + r
    return 1 + max(l, r)


def diameter_of_binary_tree(root):
    best = [0]
    height(root, best)
    return best[0]


# ---- test harness ----------------------------------------------------------

seed = 543


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
    root = TreeNode(next_random() % 201 - 100)
    for _ in range(1, size):
        c = TreeNode(next_random() % 201 - 100)
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
    d = diameter_of_binary_tree(from_level(values))
    print(f"{name}: {written(values)} -> {d}")


def main():
    show("example 1", [1, 2, 3, 4, 5])
    show("example 2", [1, 2])
    show("one node", [7])
    show("a left chain", [1, 2, None, 3, None, 4])
    show("a zigzag", [1, None, 2, 3, None, None, 4])
    show("the longest path misses the root", [1, 2, 3, 4, 5, None, None, 6, None, None, 7, 8, None, None, 9])
    show("a full tree of three levels", [-1, -2, -3, -4, -5, -6, -7])
    count = 300
    nodes = total = h = 0
    for t in range(count):
        size = 1 + next_random() % 80
        lean = 50 if t % 3 == 0 else 80 if t % 3 == 1 else 95
        d = diameter_of_binary_tree(random_tree(size, lean))
        nodes += size
        total += d
        h = (h * 31 + d) % 1000000007
    print(f"{count} random trees: {nodes} nodes, diameters {total}, checksum {h}")
    print(f"10000 nodes at random: {diameter_of_binary_tree(random_tree(10000, 50))}")
    top = last = TreeNode(0)
    for v in range(1, 10000):
        c = TreeNode(v % 201 - 100)
        last.left = c
        last = c
    print(f"10000 nodes down the left: {diameter_of_binary_tree(top)}")
    root = TreeNode(0)
    l = r = root
    for v in range(1, 10000):
        c = TreeNode(v % 201 - 100)
        if v % 2 == 1:
            l.left = c
            l = c
        else:
            r.right = c
            r = c
    print(f"two chains of 10000 nodes: {diameter_of_binary_tree(root)}")
    values = [v % 201 - 100 for v in range(10000)]
    print(f"a complete tree of 10000 nodes: {diameter_of_binary_tree(from_level(values))}")


main()
