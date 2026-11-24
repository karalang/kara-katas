# LeetCode #1339 bench in Python: the ★ arm (one recursive walk for the
# total, a second for every subtree's sum, keeping the best product, taken
# modulo 10^9 + 7 at the end) on the same 10 trees of 5 * 10^4 nodes and
# 20 passes. A tree hung at random places is a few dozen levels deep, well
# inside Python's recursion limit.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def total(node):
    if node is None:
        return 0
    return node.val + total(node.left) + total(node.right)


def max_product(root):
    all_ = total(root)
    best = 0

    def best_cut(node):
        nonlocal best
        if node is None:
            return 0
        s = node.val + best_cut(node.left) + best_cut(node.right)
        p = s * (all_ - s)
        if p > best:
            best = p
        return s

    best_cut(root)
    return best % 1000000007


seed = 1339


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(n):
    root = TreeNode(1 + next_random() % 10000)
    nodes = [root]
    places = [(root, True), (root, False)]
    while len(nodes) < n:
        k = next_random() % len(places)
        places[k], places[-1] = places[-1], places[k]
        parent, left = places.pop()
        node = TreeNode(1 + next_random() % 10000)
        if left:
            parent.left = node
        else:
            parent.right = node
        places.append((node, True))
        places.append((node, False))
        nodes.append(node)
    return nodes


def main():
    n = 50000
    trees = [build(n) for _ in range(10)]
    check = 0
    for pass_ in range(20):
        for t in range(10):
            nodes = trees[t]
            nodes[check % n].val = 1 + (check // 7) % 10000
            answer = max_product(nodes[0])
            check = (check * 31 + answer + pass_) % 1000000007
    print(f"20 passes over 10 trees of 5 * 10^4: checksum {check}")


main()
