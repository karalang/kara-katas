# Benchmark for #669: recursion, in place, as the Kara ★ arm.


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def trim_bst(root, low, high):
    if root is None:
        return None
    if root.val < low:
        return trim_bst(root.right, low, high)
    if root.val > high:
        return trim_bst(root.left, low, high)
    root.left = trim_bst(root.left, low, high)
    root.right = trim_bst(root.right, low, high)
    return root


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def bst(values):
    root = TreeNode(values[0])
    for v in values[1:]:
        at = root
        while True:
            if v < at.val:
                if at.left is None:
                    at.left = TreeNode(v)
                    break
                at = at.left
            else:
                if at.right is None:
                    at.right = TreeNode(v)
                    break
                at = at.right
    return root


def checksum(root):
    s = 0
    stack = [root] if root is not None else []
    while stack:
        n = stack.pop()
        s = (s * 31 + n.val) % 1000000007
        if n.right is not None:
            stack.append(n.right)
        if n.left is not None:
            stack.append(n.left)
    return s


def main():
    rng = Rng(669)
    order = list(range(10000))
    for i in range(1, 10000):
        j = rng.next() % (i + 1)
        order[i], order[j] = order[j], order[i]
    rounds = 300
    s = 0
    for r in range(rounds):
        low = r * 37 % 10000
        high = low + r * 53 % 5000
        kept = trim_bst(bst(order), low, high)
        s = (s * 31 + checksum(kept)) % 1000000007
    print(f"10000 nodes, {rounds} rounds: checksum {s}")


main()
