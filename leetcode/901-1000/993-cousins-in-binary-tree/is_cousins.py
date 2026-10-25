# LeetCode #993: Cousins in Binary Tree -- mirror of the ★ arm
# (is_cousins.kara), level by level with each node's parent.
from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_cousins(root, x, y):
    level = [(root, -1)]
    while level:
        px = -1
        py = -1
        nxt = []
        for node, parent in level:
            if node.val == x:
                px = parent
            if node.val == y:
                py = parent
            if node.left:
                nxt.append((node.left, node.val))
            if node.right:
                nxt.append((node.right, node.val))
        if px >= 0 and py >= 0:
            return px != py
        if px >= 0 or py >= 0:
            return False
        level = nxt
    return False


seed = 993


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(vals):
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while i < len(vals):
        node = queue.popleft()
        if vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals):
            if vals[i] is not None:
                node.right = TreeNode(vals[i])
                queue.append(node.right)
            i += 1
    return root


def attach(root, node):
    cur = root
    while True:
        if next_random() % 2 == 0:
            if cur.left:
                cur = cur.left
            else:
                cur.left = node
                return
        else:
            if cur.right:
                cur = cur.right
            else:
                cur.right = node
                return


# n nodes in a random shape, holding 1 to n in a random order
def random_tree(n):
    vals = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        vals[i], vals[j] = vals[j], vals[i]
    root = TreeNode(vals[0])
    for i in range(1, n):
        attach(root, TreeNode(vals[i]))
    return root


def complete_tree(n):
    nodes = [TreeNode(i + 1) for i in range(n)]
    for i in range(1, n):
        if i % 2 == 1:
            nodes[(i - 1) // 2].left = nodes[i]
        else:
            nodes[(i - 1) // 2].right = nodes[i]
    return nodes[0]


def path(n):
    t = TreeNode(n)
    for i in range(n - 1, 0, -1):
        if i % 2 == 0:
            t = TreeNode(i, None, t)
        else:
            t = TreeNode(i, t, None)
    return t


def level_order_text(vals):
    return "[" + ", ".join("null" if v is None else str(v) for v in vals) + "]"


def tf(b):
    return "true" if b else "false"


def all_pairs(root, n):
    found = 0
    for x in range(1, n + 1):
        for y in range(x + 1, n + 1):
            if is_cousins(root, x, y):
                found += 1
    return found


def main():
    N = None
    cases = [
        ([1, 2, 3, 4], 4, 3),
        ([1, 2, 3, N, 4, N, 5], 5, 4),
        ([1, 2, 3, N, 4], 2, 3),
        ([1, 2, 3, 4, 5, 6, 7], 4, 6),
        ([1, 2, 3, 4, 5, 6, 7], 4, 5),
        ([1, 2, 3, 4, 5, 6, 7], 1, 2),
        ([1, 2, 3, 4, N, N, 5, 6, N, N, 7], 6, 7),
        ([1, 2, 3, 4, N, N, 5, 6, N, N, 7], 7, 6),
        ([1, 2, 3, 4, N, N, 5, 6], 6, 5),
        ([1, 2], 1, 2),
    ]
    for vals, x, y in cases:
        print(f"root = {level_order_text(vals)}, x = {x}, y = {y} -> {tf(is_cousins(from_level_order(vals), x, y))}")
    print(f"the complete tree of 100 nodes: {all_pairs(complete_tree(100), 100)} of 4950 pairs are cousins")
    print(f"a zigzag path of 100 nodes: {all_pairs(path(100), 100)} of 4950 pairs are cousins")
    for count, most in [(300, 10), (3000, 100)]:
        nodes = 0
        found = 0
        check = 0
        for _ in range(count):
            n = 2 + next_random() % (most - 1)
            root = random_tree(n)
            nodes += n
            for _ in range(20):
                x = 1 + next_random() % n
                y = 1 + next_random() % (n - 1)
                if y >= x:
                    y += 1
                ok = is_cousins(root, x, y)
                if ok:
                    found += 1
                check = (check * 31 + (2 if ok else 1)) % 1000000007
        print(f"{count} random trees of {nodes} nodes, 20 pairs each: {found} cousins, checksum {check}")
    for t in range(3):
        root = random_tree(100)
        print(f"random tree {t + 1} of 100 nodes: {all_pairs(root, 100)} of 4950 pairs are cousins")


main()
