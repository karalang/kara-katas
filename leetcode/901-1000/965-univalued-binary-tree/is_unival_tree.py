# LeetCode #965: Univalued Binary Tree -- depth first.
#
# Mirrors is_unival_tree.kara: every node must hold the root's value, so
# check the root's value against each subtree recursively, stopping at the
# first node that differs.

from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def holds(t, v):
    if t is None:
        return True
    return t.val == v and holds(t.left, v) and holds(t.right, v)


def is_unival_tree(root):
    if root is None:
        return True
    return holds(root.left, root.val) and holds(root.right, root.val)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(vals):
    if not vals or vals[0] is None:
        return None
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
            if cur.left is not None:
                cur = cur.left
            else:
                cur.left = node
                return
        else:
            if cur.right is not None:
                cur = cur.right
            else:
                cur.right = node
                return


def random_tree(n, v, spoiled):
    odd = [False] * n
    for _ in range(spoiled):
        odd[next_random() % n] = True
    root = TreeNode(next_random() % 100 if odd[0] else v)
    for i in range(1, n):
        val = next_random() % 100 if odd[i] else v
        attach(root, TreeNode(val))
    return root


def size(t):
    if t is None:
        return 0
    return 1 + size(t.left) + size(t.right)


def show(b):
    return "true" if b else "false"


def main():
    global seed
    N = None
    cases = [
        [1, 1, 1, 1, 1, N, 1],
        [2, 2, 2, 5, 2],
        [1],
        [0, N, 0],
        [1, 1, 2],
        [2, 1, 1],
        [1, 1, N, 1, N, 1],
        [1, 1, 1, 1, 1, 1, 0],
        [5, 5, 5, N, N, 5, 6],
        [3, N, 3, N, 3, N, 4],
        [9, 9, 9, 9, N, N, 9, N, 8],
        [99, 99, 99, 99, 99, 99, 99],
    ]
    for i, c in enumerate(cases):
        print(f"case {i + 1}: {show(is_unival_tree(from_level_order(c)))}")
    seed = 965
    nodes = 0
    yes = 0
    by_spoiled = [0] * 3
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 12
        v = next_random() % 100
        spoiled = next_random() % 3
        t = random_tree(n, v, spoiled)
        nodes += size(t)
        bit = 1 if is_unival_tree(t) else 0
        yes += bit
        by_spoiled[spoiled] += bit
        check = (check * 31 + bit + 1) % 1000000007
    print(f"300 random trees of {nodes} nodes: {yes} univalued ({by_spoiled[0]}, {by_spoiled[1]}, {by_spoiled[2]} by spoiled picks), checksum {check}")
    for spoiled in range(3):
        t = random_tree(100, 50, spoiled)
        print(f"{size(t)} nodes, {spoiled} spoiled: {show(is_unival_tree(t))}")
    path = TreeNode(7)
    bent = TreeNode(8)
    for _ in range(1, 100):
        path = TreeNode(7, path)
        bent = TreeNode(7, bent)
    print(f"a path of 100 nodes: {show(is_unival_tree(path))}")
    print(f"the same with its deepest node changed: {show(is_unival_tree(bent))}")


main()
