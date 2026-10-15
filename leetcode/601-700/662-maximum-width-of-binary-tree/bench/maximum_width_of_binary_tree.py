# Benchmark for #662: level by level, as the Kara ★ arm.


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


def main():
    rng = Rng(662)
    trees = [grown_tree(3000, 31, rng) for _ in range(8)]
    rounds = 20000
    s = 0
    for r in range(rounds):
        w = width_of_binary_tree(trees[r % 8])
        s = (s * 31 + w + r) % 1000000007
    print(f"8 trees of 3000 nodes, {rounds} rounds: checksum {s}")


main()
