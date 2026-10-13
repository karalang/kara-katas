# Benchmark for #538: Python mirror of the ★ arm (reverse in order,
# recursively); see convert_bst.kara.
import sys

sys.setrecursionlimit(30000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def visit(node, total):
    if node is not None:
        visit(node.right, total)
        total[0] += node.val
        node.val = total[0]
        visit(node.left, total)


def convert_bst(root):
    visit(root, [0])
    return root


seed = 538


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# A search tree of distinct values, inserted in the order given; every
# node is also listed in `nodes`, in the same order.
def build(values, nodes):
    root = TreeNode(values[0])
    nodes.append(root)
    for v in values[1:]:
        node = root
        while True:
            if v < node.val:
                if node.left is None:
                    node.left = TreeNode(v)
                    nodes.append(node.left)
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = TreeNode(v)
                    nodes.append(node.right)
                    break
                node = node.right
    return root


def main():
    # 100 random search trees of 10,000 distinct values (the problem's
    # most) from -10,000 to 10,000, built once. Then 50 times over, each
    # tree has its values put back and is converted.
    trees = 100
    pool = list(range(-10000, 10001))
    roots, lists, originals = [], [], []
    for _ in range(trees):
        for i in range(10000):
            high = next_random()
            j = i + (high * 32768 + next_random()) % (20001 - i)
            pool[i], pool[j] = pool[j], pool[i]
        values = pool[:10000]
        nodes = []
        roots.append(build(values, nodes))
        lists.append(nodes)
        originals.append(values)
    total = 0
    checksum = 0
    for _ in range(50):
        for t in range(trees):
            for node, v in zip(lists[t], originals[t]):
                node.val = v
            top = convert_bst(roots[t]).val
            total += top
            checksum = (checksum * 31 + top + 1000000000) % 1000000007
    print(f"{trees} trees of 10000 values, 50 times each: total {total}, checksum {checksum}")


main()
