# LeetCode #2476: Closest Nodes Queries in a Binary Search Tree -- the
# bench, the ★ arm in Python: an in-order walk reads the values ascending,
# and a bisection by hand finds the first value at least each query. The
# nodes are objects with `__slots__`.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(node, values):
    if node is not None:
        walk(node.left, values)
        values.append(node.val)
        walk(node.right, values)


def closest_nodes(root, queries):
    values = []
    walk(root, values)
    answers = []
    for q in queries:
        lo, hi = 0, len(values)
        while lo < hi:
            mid = (lo + hi) // 2
            if values[mid] < q:
                lo = mid + 1
            else:
                hi = mid
        ceiling = values[lo] if lo < len(values) else -1
        if lo < len(values) and values[lo] == q:
            floor = q
        elif lo > 0:
            floor = values[lo - 1]
        else:
            floor = -1
        answers.append([floor, ceiling])
    return answers


seed = 2476


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


# the search tree of `n` distinct random values from 1 to 10^6, inserted
# in the order drawn
def random_search_tree(n):
    used = set()
    root = None
    while len(used) < n:
        v = 1 + wide_random() % 1000000
        if v in used:
            continue
        used.add(v)
        if root is None:
            root = TreeNode(v)
            continue
        at = root
        while True:
            if v < at.val:
                if at.left is not None:
                    at = at.left
                else:
                    at.left = TreeNode(v)
                    break
            else:
                if at.right is not None:
                    at = at.right
                else:
                    at.right = TreeNode(v)
                    break
    return root


def main():
    # 10 random search trees of 10^4 nodes built once; then 220 passes,
    # each asking every tree 1000 values stepped from the checksum so far,
    # folding every answer and the pass into the checksum
    trees = [random_search_tree(10000) for _ in range(10)]
    check = 0
    for p in range(220):
        for root in trees:
            queries = [1 + (check + 997 * i) % 1000000 for i in range(1000)]
            for floor, ceiling in closest_nodes(root, queries):
                check = (check * 31 + floor + ceiling + 2 + p) % 1000000007
    print(f"220 passes over 10 trees of 10^4: checksum {check}")


main()
