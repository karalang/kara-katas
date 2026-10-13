# LeetCode #501: Find Mode in Binary Search Tree -- Python mirror of the
# ★ arm (in-order with a running count); see find_mode.kara.


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Walk:
    def __init__(self):
        self.prev = 0
        self.run = 0
        self.best = 0
        self.modes = []


def visit(node, walk):
    if node is None:
        return
    visit(node.left, walk)
    if walk.run > 0 and node.val == walk.prev:
        walk.run += 1
    else:
        walk.prev = node.val
        walk.run = 1
    if walk.run > walk.best:
        walk.best = walk.run
        walk.modes.clear()
        walk.modes.append(node.val)
    elif walk.run == walk.best:
        walk.modes.append(node.val)
    visit(node.right, walk)


def find_mode(root):
    walk = Walk()
    visit(root, walk)
    return walk.modes


# ---- test harness ---------------------------------------------------------

seed = 501


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    for i in range(1, len(values)):
        v = values[i]
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


def fmt(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def show(name, values):
    root = build(values)
    print(f"{name}: {fmt(values)} -> {fmt(find_mode(root))}")


def main():
    show("example 1", [1, 2, 2])
    show("example 2", [0])
    show("all equal", [5, 5, 5, 5, 5])
    show("all different", [4, 2, 6, 1, 3, 5, 7])
    show("two modes", [3, 1, 3, 7, 1, 5])
    show("the extremes", [-100000, 100000, -100000, 0, 100000])
    show("mode at the end", [1, 2, 3, 4, 4])
    show("mode at the start", [9, 1, 5, 1, 8])
    # 300 random trees of 1 to 40 values from 1 to 5 values, 50, or the
    # whole range -100,000 to 100,000, in turn.
    count = 300
    total = 0
    modes = 0
    checksum = 0
    for t in range(count):
        if t % 3 == 0:
            rng = 1 + next_random() % 5
        elif t % 3 == 1:
            rng = 50
        else:
            rng = 200001
        size = 1 + next_random() % 40
        values = []
        for _ in range(size):
            v = next_random() * 7 % rng
            values.append(v - 100000 if rng == 200001 else v)
        total += size
        root = build(values)
        for m in find_mode(root):
            modes += 1
            checksum = (checksum * 31 + m + 100000) % 1000000007
    print(f"{count} random trees: {total} values, {modes} modes, checksum {checksum}")


main()
