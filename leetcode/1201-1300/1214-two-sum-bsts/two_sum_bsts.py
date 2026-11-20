# LeetCode #1214: Two Sum BSTs -- a Python mirror of the ★ arm: each tree's
# values read in order, then two pointers, one climbing the first list and
# one coming down the second.


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def in_order(node, out):
    # iterative here, as Python's recursion limit is below the chains' depth
    stack = []
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right


def two_sum_bsts(root1, root2, target):
    a, b = [], []
    in_order(root1, a)
    in_order(root2, b)
    i, j = 0, len(b) - 1
    while i < len(a) and j >= 0:
        s = a[i] + b[j]
        if s == target:
            return True
        if s < target:
            i += 1
        else:
            j -= 1
    return False


def bst(values):
    root = None
    for v in values:
        node = TreeNode(v)
        if root is None:
            root = node
            continue
        at = root
        while True:
            if v < at.val:
                if at.left is None:
                    at.left = node
                    break
                at = at.left
            else:
                if at.right is None:
                    at.right = node
                    break
                at = at.right
    return root


def balanced(sorted_values, low, high):
    if low >= high:
        return None
    mid = (low + high) // 2
    return TreeNode(sorted_values[mid], balanced(sorted_values, low, mid), balanced(sorted_values, mid + 1, high))


seed = 1214


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def distinct_values(n, rng):
    seen = set()
    while len(seen) < n:
        hi = next_random()
        lo = next_random()
        seen.add((hi * 32768 + lo) % (2 * rng + 1) - rng)
    return sorted(seen)


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    cases = [
        ([2, 1, 4], [1, 0, 3], 5),
        ([0, -10, 10], [5, 1, 7, 0, 2], 18),
        ([1], [1], 2),
        ([1], [1], 3),
        ([-1000000000], [1000000000], 0),
        ([1000000000], [1000000000, -1000000000], 1000000000),
        ([5, 3, 8, 1, 4], [6, 2, 9], 17),
        ([5, 3, 8, 1, 4], [6, 2, 9], 16),
    ]
    for a, b, t in cases:
        print(f"{show(a)} {show(b)} {t}: {str(two_sum_bsts(bst(a), bst(b), t)).lower()}")
    yes = check = 0
    for _ in range(1000):
        n1 = next_random() % 8 + 1
        n2 = next_random() % 8 + 1
        a = [next_random() % 21 - 10 for _ in range(n1)]
        b = [next_random() % 21 - 10 for _ in range(n2)]
        t = next_random() % 41 - 20
        answer = two_sum_bsts(bst(a), bst(b), t)
        yes += answer
        check = (check * 131 + (2 if answer else 1)) % 1000000007
    print(f"1000 small cases: {yes} true, checksum {check}")
    a = distinct_values(5000, 1000000000)
    b = distinct_values(5000, 1000000000)
    t1 = balanced(a, 0, 5000)
    t2 = balanced(b, 0, 5000)
    hit = a[1234] + b[4321]
    print(f"5000 and 5000 nodes, a sum they hold: {str(two_sum_bsts(t1, t2, hit)).lower()}")
    misses = 0
    for _ in range(20):
        hi = next_random()
        lo = next_random()
        t = (hi * 32768 + lo) % 2000000001 - 1000000000
        if not two_sum_bsts(t1, t2, t):
            misses += 1
    print(f"5000 and 5000 nodes, 20 random targets: {misses} not found")
    c1 = bst([i * 2 for i in range(5000)])
    c2 = bst([-1 - i * 2 for i in range(5000)])
    print(f"two chains of 5000, the two ends: {str(two_sum_bsts(c1, c2, 9998 - 1)).lower()}, an even target: {str(two_sum_bsts(c1, c2, 100)).lower()}")


main()
