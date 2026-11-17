# LeetCode #1586: Binary Search Tree Iterator II -- the Python mirror of
# bst_iterator.kara: the lazy in-order stack and the list of values met.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BSTIterator:
    def __init__(self, root):
        self.spine = []
        self.seen = []
        self.at = -1
        self.push_left(root)

    def push_left(self, node):
        while node is not None:
            self.spine.append(node)
            node = node.left

    def has_next(self):
        return self.at + 1 < len(self.seen) or len(self.spine) > 0

    def next(self):
        self.at += 1
        if self.at == len(self.seen):
            n = self.spine.pop()
            self.seen.append(n.val)
            self.push_left(n.right)
        return self.seen[self.at]

    def has_prev(self):
        return self.at > 0

    def prev(self):
        self.at -= 1
        return self.seen[self.at]


def insert(root, v):
    node = root
    while True:
        if v == node.val:
            return False
        child = node.left if v < node.val else node.right
        if child is not None:
            node = child
        else:
            leaf = TreeNode(v)
            if v < node.val:
                node.left = leaf
            else:
                node.right = leaf
            return True


def build(values):
    if not values:
        return None, 0
    root = TreeNode(values[0])
    n = 1
    for v in values[1:]:
        if insert(root, v):
            n += 1
    return root, n


def drive(root, calls):
    it = BSTIterator(root)
    out = []
    for c in calls:
        if c == 0:
            out.append(1 if it.has_next() else 0)
        elif c == 1:
            out.append(it.next())
        elif c == 2:
            out.append(1 if it.has_prev() else 0)
        else:
            out.append(it.prev())
    return out


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def draw_calls(n, count, rng):
    at = -1
    calls = []
    for _ in range(count):
        r = rng.next() % 6
        if 2 <= r <= 4 and at + 1 < n:
            at += 1
            calls.append(1)
        elif r == 5 and at > 0:
            at -= 1
            calls.append(3)
        else:
            calls.append(r % 2 * 2)
    return calls


def batch(count, most, below, calls, rng):
    check = 0
    nodes = 0
    made = 0
    for _ in range(count):
        size = (rng.next() * 32768 + rng.next()) % most + 1
        values = [(rng.next() * 32768 + rng.next()) % below for _ in range(size)]
        root, n = build(values)
        todo = draw_calls(n, calls, rng)
        for answer in drive(root, todo):
            check = mix(check, answer)
        nodes += n
        made += calls
    print(f"{count} trees of up to {most} values: {nodes} nodes, {made} calls, checksum {check}")


def shown(calls, answers):
    parts = ["null"]
    for c, a in zip(calls, answers):
        parts.append(str(a) if c % 2 == 1 else ("true" if a == 1 else "false"))
    return "[" + ",".join(parts) + "]"


def main():
    examples = [
        ([7, 3, 15, 9, 20], [1, 1, 3, 1, 0, 1, 1, 1, 0, 2, 3, 3]),
        ([1], [0, 2, 1, 0, 2]),
        ([1, 2, 3, 4, 5], [1, 1, 1, 1, 1, 0, 3, 3, 3, 3, 2, 0]),
        ([5, 4, 3, 2, 1], [1, 1, 3, 1, 1, 1, 1, 0, 2, 3]),
        ([4, 2, 6, 1, 3, 5, 7], [1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 0, 3, 3, 3, 3, 3, 2]),
    ]
    for values, calls in examples:
        root, _ = build(values)
        print(shown(calls, drive(root, calls)))
    rng = Rng(1586)
    batch(3000, 8, 20, 20, rng)
    batch(300, 1000, 1000000, 2000, rng)
    batch(3, 100000, 1000001, 100000, rng)


main()
