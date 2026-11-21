# LeetCode #2415: Reverse Odd Levels of Binary Tree -- the bench, the ★ arm
# in Python: mirror pairs walked down together, the values of each pair on
# an odd level swapped.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def swap_pairs(a, b, odd):
    if a is not None and b is not None:
        if odd:
            a.val, b.val = b.val, a.val
        swap_pairs(a.left, b.right, not odd)
        swap_pairs(a.right, b.left, not odd)


def reverse_odd_levels(root):
    if root is not None:
        swap_pairs(root.left, root.right, True)
    return root


seed = 2415


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def edge(root, left):
    at = root
    while True:
        nxt = at.left if left else at.right
        if nxt is None:
            return at.val
        at = nxt


def main():
    roots = []
    for _ in range(10):
        nodes = [TreeNode((next_random() * 32768 + next_random()) % 100000) for _ in range(16383)]
        for i in range(8191):
            nodes[i].left = nodes[2 * i + 1]
            nodes[i].right = nodes[2 * i + 2]
        roots.append(nodes[0])
    check = 0
    for p in range(1000):
        for root in roots:
            r = reverse_odd_levels(root)
            a = r.left.val
            b = r.right.val
            check = (check * 31 + a + p) % 1000000007
            check = (check * 31 + b + edge(r, True) + edge(r, False)) % 1000000007
    print(f"1000 passes over 10 trees of 2^14 - 1 nodes: checksum {check}")


main()
