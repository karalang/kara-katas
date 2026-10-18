# LeetCode #700: Search in a Binary Search Tree -- bench program, Python mirror of the loop arm.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


seed = 700


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def search_bst(root, val):
    at = root
    while at is not None:
        if val == at.val:
            return at
        at = at.left if val < at.val else at.right
    return None


def insert(root, v):
    at = root
    while True:
        if v < at.val:
            if at.left is not None:
                at = at.left
            else:
                at.left = TreeNode(v)
                return
        else:
            if at.right is not None:
                at = at.right
            else:
                at.right = TreeNode(v)
                return


def main():
    n = 50000
    trees = []
    for _ in range(10):
        values = [2 * i for i in range(n)]
        for i in range(1, n):
            hi = next_random()
            lo = next_random()
            j = (hi * 32768 + lo) % (i + 1)
            values[i], values[j] = values[j], values[i]
        root = TreeNode(values[0])
        for i in range(1, n):
            insert(root, values[i])
        trees.append(root)
    searches = 40000
    queries = []
    for _ in range(searches):
        hi = next_random()
        lo = next_random()
        queries.append((hi * 32768 + lo) % (2 * n))
    rounds = 5
    found = 0
    checksum = 0
    for _ in range(rounds):
        for root in trees:
            for q in queries:
                hit = search_bst(root, q)
                if hit is not None:
                    found += 1
                    checksum = (checksum * 31 + hit.val) % 1000000007
    print(f"{rounds} rounds of 10 trees of {n}, {searches} searches each: {found} found, checksum {checksum}")


main()
