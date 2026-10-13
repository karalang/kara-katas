# LeetCode #530: Minimum Absolute Difference in BST -- Python mirror of
# the ★ arm (in-order, recursively); see get_minimum_difference.kara.
# Same algorithm, same harness, same output.


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Walk:
    def __init__(self):
        self.prev = None
        self.best = 2**63 - 1


def visit(node, walk):
    if node is None:
        return
    visit(node.left, walk)
    if walk.prev is not None:
        walk.best = min(walk.best, node.val - walk.prev)
    walk.prev = node.val
    visit(node.right, walk)


def get_minimum_difference(root):
    walk = Walk()
    visit(root, walk)
    return walk.best


# ---- test harness ---------------------------------------------------------

seed = 530


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    for v in values[1:]:
        node = root
        while True:
            if v < node.val or (v == node.val and next_random() % 2 == 0):
                if node.left is not None:
                    node = node.left
                else:
                    node.left = TreeNode(v)
                    break
            else:
                if node.right is not None:
                    node = node.right
                else:
                    node.right = TreeNode(v)
                    break
    return root


def show(name, values):
    root = build(values)
    print(f"{name}: {values} -> {get_minimum_difference(root)}")


def main():
    show("example 1", [4, 2, 6, 1, 3])
    show("example 2", [1, 0, 48, 12, 49])
    show("two nodes", [0, 100000])
    show("equal values", [7, 7, 3])
    show("rising chain", [1, 3, 6, 10, 15])
    show("falling chain", [100, 50, 20, 5])
    show("closest across the root", [50, 20, 80, 45, 56])
    count = 300
    total = zeros = checksum = 0
    for t in range(count):
        rng = 10 if t % 3 == 0 else 1000 if t % 3 == 1 else 100001
        size = 2 + next_random() % 59
        values = []
        for _ in range(size):
            high = next_random()
            values.append((high * 32768 + next_random()) % rng)
        total += size
        answer = get_minimum_difference(build(values))
        if answer == 0:
            zeros += 1
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"{count} random trees: {total} values, {zeros} with a repeat, checksum {checksum}")
    values = [i * 10 for i in range(10000)]
    values[5000] = 50007
    for i in range(9999, 0, -1):
        high = next_random()
        j = (high * 32768 + next_random()) % (i + 1)
        values[i], values[j] = values[j], values[i]
    print(f"10000 values: {get_minimum_difference(build(values))}")


main()
