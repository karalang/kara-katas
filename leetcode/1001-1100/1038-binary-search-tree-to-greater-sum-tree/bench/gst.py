# LeetCode #1038: Binary Search Tree to Greater Sum Tree -- bench
# Mirrors ../gst.kara; see ../README.md § Benchmarks.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def add_greater(node, above):
    if node is None:
        return above
    total = add_greater(node.right, above) + node.val
    node.val = total
    return add_greater(node.left, total)


def bst_to_gst(root):
    add_greater(root, 0)
    return root


seed = 1038


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(keys):
    root = TreeNode(keys[0])
    nodes = [root]
    for v in keys[1:]:
        fresh = TreeNode(v)
        nodes.append(fresh)
        node = root
        while True:
            if v < node.val:
                if node.left is not None:
                    node = node.left
                else:
                    node.left = fresh
                    break
            else:
                if node.right is not None:
                    node = node.right
                else:
                    node.right = fresh
                    break
    return root, nodes


def main():
    trees, rounds = 10000, 50
    pool = list(range(101))
    roots, lists, originals = [], [], []
    for _ in range(trees):
        for i in range(100):
            j = i + next_random() % (101 - i)
            pool[i], pool[j] = pool[j], pool[i]
        keys = pool[:100]
        root, nodes = build(keys)
        roots.append(root)
        lists.append(nodes)
        originals.append(keys)
    total = 0
    check = 0
    for _ in range(rounds):
        for t in range(trees):
            for n, k in zip(lists[t], originals[t]):
                n.val = k
            top = bst_to_gst(roots[t]).val
            total += top
            check = (check * 31 + top + 1000) % 1000000007
    print(f"{trees} trees of 100 keys, {rounds} rounds: total {total}, checksum {check}")


main()
