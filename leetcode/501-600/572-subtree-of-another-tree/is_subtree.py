# LeetCode #572: Subtree of Another Tree -- Python mirror of the ★ arm
# (recursion); see is_subtree.kara.
import sys

sys.setrecursionlimit(20000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def same_tree(a, b):
    if a is None and b is None:
        return True
    if a is not None and b is not None:
        return a.val == b.val and same_tree(a.left, b.left) and same_tree(a.right, b.right)
    return False


def is_subtree(root, sub_root):
    if same_tree(root, sub_root):
        return True
    if root is None:
        return False
    return is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)


# ---- test harness ---------------------------------------------------------

seed = 572


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def leaf(v):
    return TreeNode(v)


def from_level(values):
    if not values or values[0] is None:
        return None
    root = leaf(values[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(values):
        n = queue[head]
        head += 1
        if values[i] is not None:
            c = leaf(values[i])
            n.left = c
            queue.append(c)
        i += 1
        if i < len(values):
            if values[i] is not None:
                c = leaf(values[i])
                n.right = c
                queue.append(c)
            i += 1
    return root


def random_tree(size, most, lean):
    root = leaf(next_random() % (most + 1))
    for _ in range(1, size):
        c = leaf(next_random() % (most + 1))
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


def copy_tree(node):
    if node is None:
        return None
    return TreeNode(node.val, copy_tree(node.left), copy_tree(node.right))


def all_nodes(node, out):
    if node is not None:
        out.append(node)
        all_nodes(node.left, out)
        all_nodes(node.right, out)


def show(name, root, sub_root):
    got = "true" if is_subtree(from_level(root), from_level(sub_root)) else "false"
    print(f"{name}: {got}")


def main():
    show("example 1", [3, 4, 5, 1, 2], [4, 1, 2])
    show("example 2", [3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2])
    show("the whole tree", [1, 2, 3], [1, 2, 3])
    show("a leaf", [1, 2, 3], [3])
    show("a node with children", [1, 2], [1])
    show("another shape", [1, 2, 3], [1, 3, 2])
    show("larger than root", [1], [1, 1])
    show("12 and 2", [12], [2])
    show("-2 and 2", [-2], [2])
    show("extremes", [-10000, 10000, -10000], [10000])
    found = 0
    checksum = 0
    for t in range(300):
        root = random_tree(1 + next_random() % 60, 2, 50)
        nodes = []
        all_nodes(root, nodes)
        picked = nodes[next_random() % len(nodes)]
        if t % 4 == 3:
            sub_root = random_tree(1 + next_random() % 5, 2, 50)
        else:
            sub_root = copy_tree(picked)
        if t % 4 == 1:
            inside = []
            all_nodes(sub_root, inside)
            n = inside[next_random() % len(inside)]
            n.val = (n.val + 1) % 3
        elif t % 4 == 2:
            inside = []
            all_nodes(sub_root, inside)
            n = inside[next_random() % len(inside)]
            if n.left is None:
                n.left = leaf(0)
            elif n.right is None:
                n.right = leaf(0)
        got = is_subtree(root, sub_root)
        if got:
            found += 1
        checksum = (checksum * 31 + (t + 2 if got else 1)) % 1000000007
    print(f"300 random pairs: {found} found, checksum {checksum}")
    root = random_tree(2000, 10000, 50)
    nodes = []
    all_nodes(root, nodes)
    best = root
    best_size = 0
    for n in nodes:
        inside = []
        all_nodes(n, inside)
        if len(inside) <= 1000 and len(inside) > best_size:
            best_size = len(inside)
            best = n
    got = "true" if is_subtree(root, copy_tree(best)) else "false"
    print(f"2000 nodes, a subtree of {best_size}: {got}")
    chain = leaf(1)
    last = chain
    for _ in range(1, 2000):
        c = leaf(1)
        last.left = c
        last = c
    short = leaf(1)
    end = short
    for _ in range(1, 1000):
        c = leaf(1)
        end.left = c
        end = c
    end.val = 2
    got = "true" if is_subtree(chain, short) else "false"
    print(f"a chain of 2000 ones, a chain of 1000 ending in 2: {got}")
    end.val = 1
    got = "true" if is_subtree(chain, short) else "false"
    print(f"a chain of 2000 ones, a chain of 1000 ones: {got}")


main()
