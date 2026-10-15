# LeetCode #652: Find Duplicate Subtrees -- a number for every shape.
# Mirrors the ★ arm (find_duplicate_subtrees.kara) and its test harness.


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_duplicate_subtrees(root):
    ids = {}
    counts = []
    found = []

    def number(node):
        if node is None:
            return 0
        key = (node.val, number(node.left), number(node.right))
        if key in ids:
            i = ids[key]
        else:
            counts.append(0)
            ids[key] = len(counts)
            i = len(counts)
        counts[i - 1] += 1
        if counts[i - 1] == 2:
            found.append(node)
        return i

    number(root)
    return found


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def from_level(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(values):
        n = queue[head]
        head += 1
        if values[i] is not None:
            c = TreeNode(values[i])
            n.left = c
            queue.append(c)
        i += 1
        if i < len(values):
            if values[i] is not None:
                c = TreeNode(values[i])
                n.right = c
                queue.append(c)
            i += 1
    return root


def random_tree(size, lean, low, spread, rng):
    root = None
    for _ in range(size):
        c = TreeNode(low + rng.next() % spread)
        if root is None:
            root = c
            continue
        node = root
        while True:
            if rng.next() % 100 < lean:
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
    return root


def write(node):
    if node is None:
        return "#"
    return f"{node.val},{write(node.left)},{write(node.right)}"


def duplicates(root):
    return sorted(write(n) for n in find_duplicate_subtrees(root))


def checksum(texts):
    h = 0
    for t in texts:
        for b in t.encode():
            h = (h * 131 + b) % 1000000007
        h = (h * 131 + 59) % 1000000007
    return h


def show(values):
    texts = duplicates(from_level(values))
    line = f"{len(values)} values -> {len(texts)} kinds"
    for t in texts:
        line += f" [{t}]"
    print(line)


def main():
    show([1, 2, 3, 4, None, 2, 4, None, None, 4])
    show([2, 1, 1])
    show([2, 2, 2, 3, None, 3, None])
    show([5])
    show([1, 1, 1, 1, 1, 1, 1])
    show([1, 2, 2, 3, None, None, 3])
    show([0, 0, None, 0, None, 0, None, 0])
    show([-200, 200, 200, -200, None, -200, None])
    rng = Rng(652)
    kinds = 0
    total = 0
    for _ in range(300):
        leans = [20, 50, 80]
        size = 1 + rng.next() % 40
        lean = leans[rng.next() % 3]
        texts = duplicates(random_tree(size, lean, 0, 3, rng))
        kinds += len(texts)
        total = (total + checksum(texts)) % 1000000007
    print(f"300 random trees: {kinds} kinds, checksum {total}")
    texts = duplicates(random_tree(1500, 50, 0, 2, rng))
    print(f"1500 nodes of 2 values: {len(texts)} kinds, checksum {checksum(texts)}")
    texts = duplicates(random_tree(2000, 50, -200, 401, rng))
    print(f"2000 nodes of 401 values: {len(texts)} kinds, checksum {checksum(texts)}")


main()
