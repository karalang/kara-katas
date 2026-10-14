# Benchmark for #572: Python mirror of the ★ arm (recursion); see
# is_subtree.kara.
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


# ---- benchmark --------------------------------------------------------------

seed = 572


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(size):
    root = TreeNode(next_random() % 2)
    for _ in range(1, size):
        c = TreeNode(next_random() % 2)
        node = root
        while True:
            if next_random() % 2 == 0:
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


def main():
    count = 20
    rounds = 1000
    pairs = []
    for g in range(count):
        root = random_tree(2000)
        nodes = []
        all_nodes(root, nodes)
        while True:
            picked = nodes[next_random() % len(nodes)]
            inside = []
            all_nodes(picked, inside)
            if len(inside) >= 20:
                break
        sub = copy_tree(picked)
        if g % 2 == 1:
            inside = []
            all_nodes(sub, inside)
            n = inside[next_random() % len(inside)]
            n.val = 1 - n.val
        pairs.append((root, sub))
    found = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            root, sub = pairs[(rnd * 7 + g) % count]
            got = is_subtree(root, sub)
            if got:
                found += 1
            checksum = (checksum * 31 + (g + 2 if got else 1)) % 1000000007
    print(f"{count} pairs, {rounds} rounds: {found} found, checksum {checksum}")


main()
