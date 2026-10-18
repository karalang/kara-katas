# LeetCode #701: Insert into a Binary Search Tree -- bench program, Python mirror of the loop arm.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


seed = 701


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def insert_into_bst(root, val):
    fresh = TreeNode(val)
    if root is None:
        return fresh
    at = root
    while True:
        if val < at.val:
            if at.left is not None:
                at = at.left
            else:
                at.left = fresh
                return root
        else:
            if at.right is not None:
                at = at.right
            else:
                at.right = fresh
                return root


def height(root):
    best = 0
    stack = [(root, 1)] if root is not None else []
    while stack:
        n, depth = stack.pop()
        if depth > best:
            best = depth
        if n.right is not None:
            stack.append((n.right, depth + 1))
        if n.left is not None:
            stack.append((n.left, depth + 1))
    return best


def main():
    n = 50000
    orders = []
    for _ in range(10):
        values = [2 * i for i in range(n)]
        for i in range(1, n):
            hi = next_random()
            lo = next_random()
            j = (hi * 32768 + lo) % (i + 1)
            values[i], values[j] = values[j], values[i]
        orders.append(values)
    rounds = 5
    total = 0
    checksum = 0
    for _ in range(rounds):
        for order in orders:
            root = None
            for v in order:
                root = insert_into_bst(root, v)
            h = height(root)
            total += h
            checksum = (checksum * 31 + h) % 1000000007
    print(f"{rounds} rounds of 10 trees grown to {n}: heights sum to {total}, checksum {checksum}")


main()
