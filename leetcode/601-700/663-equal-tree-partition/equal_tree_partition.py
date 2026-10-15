# LeetCode #663: Equal Tree Partition -- the subtree sums, listed.
# Mirrors the ★ arm (equal_tree_partition.kara) and its test harness.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def check_equal_tree(root):
    sums = []
    total = subtree_sum(root, sums)
    if total % 2 != 0:
        return False
    sums.pop()
    return any(s == total // 2 for s in sums)


def subtree_sum(node, sums):
    if node is None:
        return 0
    s = node.val + subtree_sum(node.left, sums) + subtree_sum(node.right, sums)
    sums.append(s)
    return s


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


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


def random_tree(levels, chance, spread, rng):
    if levels == 0:
        return None
    n = TreeNode(rng.next() % (2 * spread + 1) - spread)
    if rng.next() % 100 < chance:
        n.left = random_tree(levels - 1, chance, spread, rng)
    if rng.next() % 100 < chance:
        n.right = random_tree(levels - 1, chance, spread, rng)
    return n


def grown_tree(count, rng):
    root = TreeNode(rng.next() % 200001 - 100000)
    for _ in range(1, count):
        at = root
        placed = False
        while not placed:
            if rng.next() % 2 == 0:
                if at.left is not None:
                    at = at.left
                else:
                    at.left = TreeNode(rng.next() % 200001 - 100000)
                    placed = True
            else:
                if at.right is not None:
                    at = at.right
                else:
                    at.right = TreeNode(rng.next() % 200001 - 100000)
                    placed = True
    return root


def chain(count, last):
    top = TreeNode(1)
    bottom = top
    for i in range(1, count):
        c = TreeNode(1)
        if i % 3 == 0:
            bottom.left = c
        else:
            bottom.right = c
        bottom = c
    bottom.val = last
    return top


def copy(node):
    if node is None:
        return None
    n = TreeNode(node.val)
    n.left = copy(node.left)
    n.right = copy(node.right)
    return n


def word(b):
    return "true" if b else "false"


def show(label, root):
    print(f"{label}: {word(check_equal_tree(root))}")


def main():
    show("[5,10,10,null,null,2,3]", from_level([5, 10, 10, None, None, 2, 3]))
    show("[1,2,10,null,null,2,20]", from_level([1, 2, 10, None, None, 2, 20]))
    show("[0]", from_level([0]))
    show("[0,0]", from_level([0, 0]))
    show("[0,-1,1]", from_level([0, -1, 1]))
    show("[1,-1]", from_level([1, -1]))
    show("[1,1]", from_level([1, 1]))
    show("chain of 10000 ones", chain(10000, 1))
    show("the same, its last node 2", chain(10000, 2))
    rng = Rng(663)
    yes = 0
    s = 0
    for i in range(300):
        levels = 1 + rng.next() % 10
        chance = 40 + rng.next() % 61
        if check_equal_tree(random_tree(levels, chance, 3, rng)):
            yes += 1
            s = (s * 31 + i) % 1000000007
    print(f"300 random trees: {yes} split, checksum {s}")
    show("10000 nodes grown at random", grown_tree(10000, rng))
    half = grown_tree(4999, rng)
    root = TreeNode(0)
    root.left = copy(half)
    root.right = copy(half)
    show("0 over two copies of 4999", root)
    root = TreeNode(0)
    root.left = copy(half)
    right = copy(half)
    right.val += 2
    root.right = right
    show("the same, one value raised by 2", root)


main()
