# LeetCode #662: Maximum Width of Binary Tree -- level by level.
# Mirrors the ★ arm (maximum_width_of_binary_tree.kara) and its test harness.


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def width_of_binary_tree(root):
    best = 0
    level = [] if root is None else [(root, 0)]
    while level:
        first = level[0][1]
        last = level[-1][1]
        best = max(best, last - first + 1)
        nxt = []
        for node, place in level:
            p = (place - first) * 2
            if node.left is not None:
                nxt.append((node.left, p))
            if node.right is not None:
                nxt.append((node.right, p + 1))
        level = nxt
    return best


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


def chain(top, count, steps):
    bottom = top
    for i in range(count):
        c = TreeNode(i % 201 - 100)
        if steps[i % len(steps)] == 0:
            bottom.left = c
        else:
            bottom.right = c
        bottom = c
    return bottom


def full(levels):
    if levels == 0:
        return None
    n = TreeNode(levels)
    n.left = full(levels - 1)
    n.right = full(levels - 1)
    return n


def random_tree(levels, chance, rng):
    if levels == 0:
        return None
    n = TreeNode(rng.next() % 201 - 100)
    if rng.next() % 100 < chance:
        n.left = random_tree(levels - 1, chance, rng)
    if rng.next() % 100 < chance:
        n.right = random_tree(levels - 1, chance, rng)
    return n


def grown_tree(count, levels, rng):
    root = TreeNode(rng.next() % 201 - 100)
    made = 1
    while made < count:
        at = root
        depth = 1
        placed = False
        while not placed and depth < levels:
            if rng.next() % 2 == 0:
                if at.left is not None:
                    at = at.left
                else:
                    at.left = TreeNode(rng.next() % 201 - 100)
                    placed = True
            else:
                if at.right is not None:
                    at = at.right
                else:
                    at.right = TreeNode(rng.next() % 201 - 100)
                    placed = True
            depth += 1
        if placed:
            made += 1
    return root


def show(label, root):
    print(f"{label}: {width_of_binary_tree(root)}")


def main():
    show("[1,3,2,5,3,null,9]", from_level([1, 3, 2, 5, 3, None, 9]))
    show("[1,3,2,5,null,null,9,6,null,7]", from_level([1, 3, 2, 5, None, None, 9, 6, None, 7]))
    show("[1,3,2,5]", from_level([1, 3, 2, 5]))
    show("one node", from_level([0]))
    show("full, 4 levels", full(4))
    root, left, right = TreeNode(0), TreeNode(1), TreeNode(2)
    root.left, root.right = left, right
    chain(left, 29, [0])
    chain(right, 29, [1])
    show("spreading chains, 31 levels", root)
    root, left, right = TreeNode(0), TreeNode(1), TreeNode(2)
    root.left, root.right = left, right
    chain(left, 1498, [1])
    chain(right, 1498, [0])
    show("chains growing together, 2999 nodes", root)
    root = TreeNode(0)
    foot = chain(root, 2984, [0, 1, 1, 0, 1])
    foot.left = full(4)
    show("zigzag chain with a full foot, 3000 nodes", root)
    rng = Rng(662)
    s = 0
    widest = 0
    for _ in range(200):
        levels = 1 + rng.next() % 12
        chance = 40 + rng.next() % 61
        w = width_of_binary_tree(random_tree(levels, chance, rng))
        widest = max(widest, w)
        s = (s * 31 + w) % 1000000007
    print(f"200 random trees: widest {widest}, checksum {s}")
    for _ in range(2):
        show("3000 nodes grown at random", grown_tree(3000, 31, rng))


main()
