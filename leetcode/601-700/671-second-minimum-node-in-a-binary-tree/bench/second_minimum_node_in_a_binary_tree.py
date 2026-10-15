# Benchmark for #671: a pruned walk, as the Kara ★ arm.


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


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


def find_second_minimum_value(root):
    return -1 if root is None else smallest_above(root, root.val)


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def special(levels, val, spread, rng):
    n = TreeNode(val)
    if levels > 1:
        other = val + rng.next() % (spread + 1)
        n.left = special(levels - 1, val, spread, rng)
        n.right = special(levels - 1, other, spread, rng)
    return n


def main():
    rng = Rng(671)
    trees = [special(16, 7 + t, 0 if t % 4 == 0 else t, rng) for t in range(16)]
    rounds = 2000
    s = 0
    for r in range(rounds):
        x = find_second_minimum_value(trees[r % 16])
        s = (s * 31 + x + 1) % 1000000007
    print(f"16 trees of 65535 nodes, {rounds} rounds: checksum {s}")


main()
