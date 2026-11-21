# LeetCode #2471: Minimum Number of Operations to Sort a Binary Tree by
# Level -- the bench, the ★ arm in Python: the levels by a breadth-first
# walk, and in each the cycles of the permutation that sorts it, a dict
# from each value to its sorted place. The nodes are objects with
# `__slots__`.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def minimum_operations(root):
    total = 0
    level = [root] if root is not None else []
    while level:
        values = [n.val for n in level]
        target = {v: i for i, v in enumerate(sorted(values))}
        seen = [False] * len(values)
        for i in range(len(values)):
            length = 0
            at = i
            while not seen[at]:
                seen[at] = True
                at = target[values[at]]
                length += 1
            if length > 1:
                total += length - 1
        nxt = []
        for n in level:
            if n.left is not None:
                nxt.append(n.left)
            if n.right is not None:
                nxt.append(n.right)
        level = nxt
    return total


seed = 2471


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random()
    return high * 32768 + next_random()


# the nodes of a random tree, the root first: the values 1 to `n` in a
# random order, each node after the first hung below a random earlier
# one, a random side taken down from it until a free one is found
def random_tree(n):
    values = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = wide() % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = [TreeNode(v) for v in values]
    for k in range(1, n):
        at = nodes[wide() % k]
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
    return nodes


def main():
    # 20 random trees of 10^4 nodes built once; then 110 passes, each
    # answering every tree, folding the count plus the pass into the
    # checksum, then swapping two of its values chosen by the checksum
    n = 10000
    trees = [random_tree(n) for _ in range(20)]
    check = 0
    for p in range(110):
        for nodes in trees:
            check = (check * 31 + minimum_operations(nodes[0]) + p) % 1000000007
            a = nodes[check % n]
            b = nodes[(check // n + p) % n]
            a.val, b.val = b.val, a.val
    print(f"110 passes over 20 trees of 10^4: checksum {check}")


main()
