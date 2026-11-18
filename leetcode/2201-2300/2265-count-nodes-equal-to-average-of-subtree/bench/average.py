# LeetCode #2265: Count Nodes Equal to Average of Subtree -- Python mirror
# of the ★ arm (average.kara) on the bench workload: the same random
# trees, each counted by one post-order walk returning (sum, size).
# Output is byte-identical to average.kara.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def average_of_subtree(root):
    matches = 0

    def sum_and_size(node):
        nonlocal matches
        if node is None:
            return 0, 0
        ls, lc = sum_and_size(node.left)
        rs, rc = sum_and_size(node.right)
        s = ls + rs + node.val
        c = lc + rc + 1
        if s // c == node.val:
            matches += 1
        return s, c

    sum_and_size(root)
    return matches


# ---- bench harness ---------------------------------------------------------

seed = 2265


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n, top):
    nodes = [TreeNode(next_random() % (top + 1)) for _ in range(n)]
    for k in range(1, n):
        at = nodes[next_random() % k]
        while True:
            if next_random() % 2 == 0:
                if at.left is not None:
                    at = at.left
                else:
                    at.left = nodes[k]
                    break
            else:
                if at.right is not None:
                    at = at.right
                else:
                    at.right = nodes[k]
                    break
    return nodes[0]


def main():
    check = 0
    for _ in range(500):
        root = random_tree(1000, 1000)
        for _ in range(20):
            check = (check * 31 + average_of_subtree(root)) % 1000000007
    print(f"500 trees of 1000, 20 times: checksum {check}")


main()
