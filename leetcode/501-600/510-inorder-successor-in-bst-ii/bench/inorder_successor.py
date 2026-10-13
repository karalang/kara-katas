# Benchmark for #510: Python mirror of the ★ arm (down the right subtree,
# or up to the first larger ancestor); see inorder_successor.kara.


class Node:
    __slots__ = ("val", "left", "right", "parent")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None


def inorder_successor(node):
    if node.right is not None:
        cur = node.right
        while cur.left is not None:
            cur = cur.left
        return cur
    up = node.parent
    while up is not None:
        if up.val > node.val:
            return up
        up = up.parent
    return None


# ---- benchmark --------------------------------------------------------------

seed = 510


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(values):
    root = Node(values[0])
    nodes = [root]
    for v in values[1:]:
        leaf = Node(v)
        node = root
        while True:
            if v < node.val:
                if node.left is not None:
                    node = node.left
                else:
                    leaf.parent = node
                    node.left = leaf
                    break
            else:
                if node.right is not None:
                    node = node.right
                else:
                    leaf.parent = node
                    node.right = leaf
                    break
        nodes.append(leaf)
    return nodes


def main():
    # 100 random search trees of 10,000 different values, the j-th value
    # j * 20 plus less than 20, shuffled, built once. Then the successor
    # of every node, 50 times over.
    trees = 100
    size = 10000
    all_trees = []
    for _ in range(trees):
        values = [j * 20 + next_random() % 20 - 100000 for j in range(size)]
        for i in range(1, size):
            k = next_random() % (i + 1)
            values[i], values[k] = values[k], values[i]
        all_trees.append(build(values))
    nulls = 0
    checksum = 0
    for _ in range(50):
        for t in range(trees):
            for node in all_trees[t]:
                s = inorder_successor(node)
                if s is not None:
                    checksum = (checksum + s.val + 100000) % 1000000007
                else:
                    nulls += 1
    print(f"{trees} trees of {size} nodes, 50 times each: {nulls} without a successor, checksum {checksum}")


main()
