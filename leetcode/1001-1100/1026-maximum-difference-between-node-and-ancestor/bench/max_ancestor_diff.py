# LeetCode #1026: Maximum Difference Between Node and Ancestor -- bench
# Mirrors ./max_ancestor_diff.kara; see ../README.md § Benchmarks.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def max_ancestor_diff(root):
    if root is None:
        return 0
    return best_below(root, root.val, root.val)


def best_below(node, low, high):
    if node is None:
        return high - low
    lo = min(low, node.val)
    hi = max(high, node.val)
    return max(best_below(node.left, lo, hi), best_below(node.right, lo, hi))


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_value(seed, top):
    high = next_random(seed)
    return (high * 32768 + next_random(seed)) % top


def random_tree(seed, n):
    root = TreeNode(random_value(seed, 100001))
    placed = 1
    while placed < n:
        node = root
        while True:
            go_left = next_random(seed) % 2 == 0
            nxt = node.left if go_left else node.right
            if nxt is not None:
                node = nxt
            else:
                leaf = TreeNode(random_value(seed, 100001))
                if go_left:
                    node.left = leaf
                else:
                    node.right = leaf
                placed += 1
                break
    return root


def main():
    count = 200
    rounds = 50
    seed = [1026]
    trees = []
    nodes = 0
    for _ in range(count):
        n = next_random(seed) % 4999 + 2
        nodes += n
        trees.append(random_tree(seed, n))
    total = 0
    check = 0
    for _ in range(rounds):
        for tree in trees:
            answer = max_ancestor_diff(tree)
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"{count} trees, {nodes} nodes, {rounds} rounds: sum {total}, checksum {check}")


main()
