# LeetCode #687: Longest Univalue Path -- one walk, two arms per node.
# Mirrors the ★ arm (longest_univalue_path.kara) and its test harness.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def longest_univalue_path(root):
    best = [0]
    arm(root, best)
    return best[0]


# The node's longest downward path of its own value, in edges; `best`
# takes the longest path that bends at the node.
def arm(node, best):
    if node is None:
        return 0
    l = arm(node.left, best)
    r = arm(node.right, best)
    left = 0
    right = 0
    if node.left is not None and node.left.val == node.val:
        left = l + 1
    if node.right is not None and node.right.val == node.val:
        right = r + 1
    if left + right > best[0]:
        best[0] = left + right
    return max(left, right)


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


# A tree from LeetCode's level order: `None` for a missing child.
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


def show(name, root):
    print(f"{name}: {longest_univalue_path(root)}")


# The tree of `n` nodes whose shape is number `shape` among the
# catalan[n] shapes, its values taken in preorder from the binary digits
# of `code`, 1 for a 0 digit and 2 for a 1.
def build(n, shape, catalan, code):
    if n == 0:
        return None
    k = 0
    rest = shape
    while rest >= catalan[k] * catalan[n - 1 - k]:
        rest -= catalan[k] * catalan[n - 1 - k]
        k += 1
    node = TreeNode(1 + code[0] % 2)
    code[0] //= 2
    node.left = build(k, rest // catalan[n - 1 - k], catalan, code)
    node.right = build(n - 1 - k, rest % catalan[n - 1 - k], catalan, code)
    return node


# A random tree at most `levels` deep: each child is there with chance
# `chance` in 100, its value from 1 to `values`.
def random_tree(rng, levels, values, chance):
    n = TreeNode(1 + rng.next() % values)
    if levels > 1:
        if rng.next() % 100 < chance:
            n.left = random_tree(rng, levels - 1, values, chance)
        if rng.next() % 100 < chance:
            n.right = random_tree(rng, levels - 1, values, chance)
    return n


def main():
    show("[5,4,5,1,1,null,5]", from_level([5, 4, 5, 1, 1, None, 5]))
    show("[1,4,5,4,4,null,5]", from_level([1, 4, 5, 4, 4, None, 5]))
    show("[]", from_level([]))
    show("[1]", from_level([1]))
    show("[1,1,1,1,null,null,1]", from_level([1, 1, 1, 1, None, None, 1]))
    show("[1,1,1,2,null,null,2,1,null,null,1]", from_level([1, 1, 1, 2, None, None, 2, 1, None, None, 1]))
    show("[1,2,3,2,2,3,3,2,2,2,2]", from_level([1, 2, 3, 2, 2, 3, 3, 2, 2, 2, 2]))
    show("[-5,-5,-5,1000,-5,-5]", from_level([-5, -5, -5, 1000, -5, -5]))

    # A zigzag of 1,000 nodes of one value, then with one node changed.
    top = TreeNode(7)
    at = top
    middle = top
    for i in range(1, 1000):
        c = TreeNode(7)
        if i % 2 == 0:
            at.left = c
        else:
            at.right = c
        if i == 600:
            middle = c
        at = c
    before = longest_univalue_path(top)
    middle.val = 8
    print(f"zigzag of 1000: {before}, with node 600 changed: {longest_univalue_path(top)}")

    # A full tree of 15 levels holding one value.
    rng = Rng(687)
    full = random_tree(rng, 15, 1, 100)
    print(f"full 15 levels of one value: {longest_univalue_path(full)}")

    # Every tree of 1 to 6 nodes with values 1 and 2.
    catalan = [1]
    for n in range(1, 7):
        catalan.append(sum(catalan[k] * catalan[n - 1 - k] for k in range(n)))
    counts = [0] * 6
    trees = 0
    total = 0
    for n in range(1, 7):
        for shape in range(catalan[n]):
            for values in range(1 << n):
                t = build(n, shape, catalan, [values])
                r = longest_univalue_path(t)
                counts[r] += 1
                trees += 1
                total = (total * 31 + r + 1) % 1000000007
    print(f"all {trees} trees of 1 to 6 nodes over values 1 and 2, by answer 0 to 5: {counts}, checksum {total}")

    # 1,000 random trees up to 8 levels, values 1 to 1, 2 or 3.
    checksum = 0
    for _ in range(1000):
        values = 1 + rng.next() % 3
        chance = 50 + rng.next() % 40
        t = random_tree(rng, 8, values, chance)
        checksum = (checksum * 31 + longest_univalue_path(t) + 1) % 1000000007
    print(f"1000 random trees: checksum {checksum}")


main()
