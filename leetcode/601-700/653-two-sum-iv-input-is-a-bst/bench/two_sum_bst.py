# Benchmark for #653: in order, then two ends, as the Kara ★ arm.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def find_target(root, k):
    values = []

    def in_order(node):
        if node is not None:
            in_order(node.left)
            values.append(node.val)
            in_order(node.right)

    in_order(root)
    if len(values) < 2:
        return False
    low, high = 0, len(values) - 1
    while low < high:
        s = values[low] + values[high]
        if s == k:
            return True
        elif s < k:
            low += 1
        else:
            high -= 1
    return False


seed = 653


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    size = 200000
    queries = 300
    seen = set()
    root = None
    count = 0
    while count < size:
        hi = next_random()
        v = (hi * 32768 + next_random()) % 1000000
        if v in seen:
            continue
        seen.add(v)
        count += 1
        c = TreeNode(v)
        if root is None:
            root = c
            continue
        node = root
        while True:
            if v < node.val:
                if node.left is not None:
                    node = node.left
                else:
                    node.left = c
                    break
            else:
                if node.right is not None:
                    node = node.right
                else:
                    node.right = c
                    break
    found = 0
    checksum = 0
    for _ in range(queries):
        hi = next_random()
        k = (hi * 32768 + next_random()) % 3000000
        hit = find_target(root, k)
        found += hit
        checksum = (checksum * 2 + (1 if hit else 0)) % 1000000007
    print(f"{size} values, {queries} targets: {found} found, checksum {checksum}")


main()
