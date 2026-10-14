# LeetCode #545: Boundary of Binary Tree -- Python mirror of the ★ arm
# (three walks); see boundary_of_binary_tree.kara.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_leaf(n):
    return n.left is None and n.right is None


def leaves(node, out):
    if node is not None:
        if is_leaf(node):
            out.append(node.val)
        else:
            leaves(node.left, out)
            leaves(node.right, out)


def boundary_of_binary_tree(root):
    out = []
    if root is None:
        return out
    out.append(root.val)
    if is_leaf(root):
        return out
    node = root.left
    while node is not None:
        if is_leaf(node):
            break
        out.append(node.val)
        node = node.left if node.left is not None else node.right
    leaves(root.left, out)
    leaves(root.right, out)
    right = []
    node = root.right
    while node is not None:
        if is_leaf(node):
            break
        right.append(node.val)
        node = node.right if node.right is not None else node.left
    out.extend(reversed(right))
    return out


# ---- test harness ----------------------------------------------------------

seed = 545


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


def mix(h, vals):
    for v in vals:
        h = (h * 31 + v + 1001) % 1000000007
    return h


def show(name, values):
    b = boundary_of_binary_tree(from_level(values))
    print(f"{name}: {written(values)} -> [{', '.join(map(str, b))}]")


def summary(name, root):
    b = boundary_of_binary_tree(root)
    print(f"{name}: {len(b)} on the boundary, first {b[0]}, last {b[-1]}, checksum {mix(0, b)}")


def chain(side):
    top = last = TreeNode(0)
    for v in range(1, 10000):
        c = TreeNode(v % 2001 - 1000)
        setattr(last, side, c)
        last = c
    return top


def main():
    show("example 1", [1, None, 2, 3, 4])
    show("example 2", [1, 2, 3, 4, 5, 6, None, None, None, 7, 8, 9, 10])
    show("one node", [7])
    show("only a left child", [1, 2])
    show("only a right child", [1, None, 2])
    show("a left chain", [1, 2, None, 3, None, 4])
    show("a zigzag on the left", [1, 2, 3, None, 4, None, None, 5, 6])
    show("a zigzag on the right", [1, 2, 3, None, None, 4, None, None, 5])
    show("a full tree of three levels", [-1, -2, -3, -4, -5, -6, -7])
    count = 300
    nodes = total = h = 0
    for t in range(count):
        size = 1 + next_random() % 80
        lean = 50 if t % 3 == 0 else 80 if t % 3 == 1 else 95
        b = boundary_of_binary_tree(random_tree(size, lean))
        nodes += size
        total += len(b)
        h = mix(h, b)
    print(f"{count} random trees: {nodes} nodes, {total} on the boundary, checksum {h}")
    summary("10000 nodes at random", random_tree(10000, 50))
    summary("10000 nodes down the left", chain("left"))
    summary("10000 nodes down the right", chain("right"))
    summary("a complete tree of 10000 nodes", from_level([v % 2001 - 1000 for v in range(10000)]))


main()
