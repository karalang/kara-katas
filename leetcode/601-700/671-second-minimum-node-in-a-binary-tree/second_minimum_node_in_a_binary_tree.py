# LeetCode #671: Second Minimum Node In a Binary Tree -- a pruned walk.
# Mirrors the ★ arm (second_minimum_node_in_a_binary_tree.kara) and its
# test harness.


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def find_second_minimum_value(root):
    if root is None:
        return -1
    return smallest_above(root, root.val)


def smallest_above(node, low):
    if node is None:
        return -1
    if node.val > low:
        return node.val
    a = smallest_above(node.left, low)
    b = smallest_above(node.right, low)
    if a == -1:
        return b
    if b == -1:
        return a
    return min(a, b)


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
            n.left = TreeNode(values[i])
            queue.append(n.left)
        i += 1
        if i < len(values):
            if values[i] is not None:
                n.right = TreeNode(values[i])
                queue.append(n.right)
            i += 1
    return root


def special(levels, val, chance, spread, rng):
    n = TreeNode(val)
    if levels > 1 and rng.next() % 100 < chance:
        other = val + rng.next() % (spread + 1)
        a = special(levels - 1, val, chance, spread, rng)
        b = special(levels - 1, other, chance, spread, rng)
        if rng.next() % 2 == 0:
            n.left, n.right = a, b
        else:
            n.left, n.right = b, a
    return n


def size(root):
    return 0 if root is None else 1 + size(root.left) + size(root.right)


def show(name, root):
    print(f"{name}: {find_second_minimum_value(root)}")


def main():
    for v in [[2, 2, 5, None, None, 5, 7], [2, 2, 2], [1], [5, 8, 5], [2, 2, 2147483647],
              [1, 1, 1, 1, 1, 1, 1, 1, 3], [3, 3, 3, 3, 3, 3, 3],
              [1, 1, 3, 1, 1, 3, 4, 3, 1, 1, 1, 3, 8, 4, 8, 3, 3, 1, 6, 2, 1]]:
        name = "[" + ",".join("null" if x is None else str(x) for x in v) + "]"
        show(name, from_level(v))
    rng = Rng(671)
    for spread in [0, 1, 3, 1000000]:
        t = special(16, 7, 100, spread, rng)
        print(f"full 16 levels, spread {spread}: {size(t)} nodes, "
              f"second {find_second_minimum_value(t)}")
    s = 0
    none = 0
    for _ in range(1000):
        val = 1 + rng.next() % 5
        spread = rng.next() % 4
        t = special(6, val, 60, spread, rng)
        r = find_second_minimum_value(t)
        if r == -1:
            none += 1
        s = (s * 31 + r + 1) % 1000000007
    print(f"1000 random trees: {none} with no second value, checksum {s}")


main()
