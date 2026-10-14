# LeetCode #549: Binary Tree Longest Consecutive Sequence II -- Python
# mirror of the ★ arm (post-order, two lengths a node); see
# binary_tree_longest_consecutive_sequence_ii.kara. The walk recurses
# 30,000 deep, so it runs on a thread with a large stack.
import sys
import threading


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(node, best):
    rise = 1
    fall = 1
    if node.left is not None:
        l = node.left
        r1, f1 = walk(l, best)
        if l.val == node.val + 1:
            rise = r1 + 1
        elif l.val == node.val - 1:
            fall = f1 + 1
    if node.right is not None:
        r = node.right
        r2, f2 = walk(r, best)
        if r.val == node.val + 1:
            rise = max(rise, r2 + 1)
        elif r.val == node.val - 1:
            fall = max(fall, f2 + 1)
    best[0] = max(best[0], rise + fall - 1)
    return rise, fall


def longest_consecutive(root):
    best = [0]
    if root is not None:
        walk(root, best)
    return best[0]


# ---- test harness ---------------------------------------------------------

seed = 549


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def random_tree(size, spread):
    root = TreeNode(next_random() % spread)
    for _ in range(1, size):
        c = TreeNode(next_random() % spread)
        node = root
        while True:
            if next_random() % 2 == 0:
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


def written(values):
    return "[" + ",".join("null" if v is None else str(v) for v in values) + "]"


def show(name, values):
    print(f"{name}: {written(values)} -> {longest_consecutive(from_level(values))}")


def main():
    N = None
    show("example 1", [1, 2, 3])
    show("example 2", [2, 1, 3])
    show("one node", [5])
    show("falling down the left", [4, 3, N, 2, N, 1])
    show("a bend below the root", [9, 5, N, 4, 6, 3, N, N, 7])
    show("both children one higher", [1, 2, 2, 3, N, N, 3])
    show("negative values", [-1, 0, -2, N, 1, -3])
    show("a run that skips a value", [1, 3, 2, 4, N, 3])
    nodes = total = h = 0
    for t in range(300):
        size = 1 + next_random() % 80
        spread = 3 if t % 3 == 0 else 5 if t % 3 == 1 else 10
        d = longest_consecutive(random_tree(size, spread))
        nodes += size
        total += d
        h = (h * 31 + d) % 1000000007
    print(f"300 random trees: {nodes} nodes, lengths {total}, checksum {h}")
    print(f"30000 nodes at random: {longest_consecutive(random_tree(30000, 4))}")
    top = TreeNode(-15000)
    last = top
    for v in range(1, 30000):
        c = TreeNode(v - 15000)
        last.left = c
        last = c
    print(f"30000 nodes rising down the left: {longest_consecutive(top)}")
    root = TreeNode(0)
    l = r = root
    for v in range(1, 15000):
        a = TreeNode(-v)
        l.left = a
        l = a
        b = TreeNode(v)
        r.right = b
        r = b
    print(f"two chains of 14999 nodes: {longest_consecutive(root)}")
    values = []
    depth, width, placed = 0, 1, 0
    while len(values) < 30000:
        values.append(depth)
        placed += 1
        if placed == width:
            depth += 1
            width *= 2
            placed = 0
    print(f"a complete tree of 30000 nodes: {longest_consecutive(from_level(values))}")


sys.setrecursionlimit(100000)
threading.stack_size(512 * 1024 * 1024)
t = threading.Thread(target=main)
t.start()
t.join()
