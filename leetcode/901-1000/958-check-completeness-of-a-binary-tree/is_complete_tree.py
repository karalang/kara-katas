# LeetCode #958: Check Completeness of a Binary Tree -- the first gap.
#
# Mirrors is_complete_tree.kara: walk the tree in level order, the missing
# children included as gaps; once a gap has been seen, any node after it
# means the tree is not complete.

from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_complete_tree(root):
    queue = deque([root])
    gap = False
    while queue:
        node = queue.popleft()
        if node is None:
            gap = True
        else:
            if gap:
                return False
            queue.append(node.left)
            queue.append(node.right)
    return True


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


def new_node():
    return TreeNode(1 + next_random() % 1000)


def side_of(i):
    return (i + 1) % 2


def set_child(parent, side, child):
    if side == 0:
        parent.left = child
    else:
        parent.right = child


def complete_tree(n):
    if n == 0:
        return None
    nodes = [new_node() for _ in range(n)]
    for i in range(1, n):
        set_child(nodes[(i - 1) // 2], side_of(i), nodes[i])
    return nodes[0]


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


def random_tree(n):
    if n == 0:
        return None
    root = new_node()
    for _ in range(1, n):
        attach(root, new_node())
    return root


def in_order(root):
    out = [root]
    i = 0
    while i < len(out):
        node = out[i]
        if node.left is not None:
            out.append(node.left)
        if node.right is not None:
            out.append(node.right)
        i += 1
    return out


def make_tree(kind, n):
    if kind == 3:
        return random_tree(n)
    t = complete_tree(n)
    if n < 2:
        return t
    nodes = in_order(t)
    if kind == 1:
        last = nodes[n - 1]
        set_child(nodes[(n - 2) // 2], side_of(n - 1), None)
        parents = []
        sides = []
        for i in range(n - 1):
            if nodes[i].left is None:
                parents.append(nodes[i])
                sides.append(0)
            if nodes[i].right is None:
                parents.append(nodes[i])
                sides.append(1)
        k = next_random() % len(parents)
        set_child(parents[k], sides[k], last)
    elif kind == 2:
        leaves = [i for i in range(1, n) if nodes[i].left is None and nodes[i].right is None]
        i = leaves[next_random() % len(leaves)]
        set_child(nodes[(i - 1) // 2], side_of(i), None)
    elif kind == 4:
        node = nodes[next_random() % n]
        node.left, node.right = node.right, node.left
    return t


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
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, N, 7],
        [1],
        [1, 2],
        [1, N, 2],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 2, 3, 4, N, 6],
        [1, 2, 3, N, N, 6, 7],
        [1, 2, 3, 4, 5, 6, 7, 8],
        [1, 2, 3, 4, 5, 6, 7, N, 8],
        [1, 2, N, 3],
    ]
    for i, c in enumerate(cases):
        print(f"case {i + 1}: {show(is_complete_tree(from_level_order(c)))}")
    seed = 958
    nodes = 0
    yes = 0
    by_kind = [0] * 5
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 12
        kind = next_random() % 5
        t = make_tree(kind, n)
        nodes += size(t)
        bit = 1 if is_complete_tree(t) else 0
        yes += bit
        by_kind[kind] += bit
        check = (check * 31 + bit + 1) % 1000000007
    print(f"300 random trees of {nodes} nodes: {yes} complete ({by_kind[0]}, {by_kind[1]}, {by_kind[2]}, {by_kind[3]}, {by_kind[4]} by kind), checksum {check}")
    for kind in range(5):
        t = make_tree(kind, 100)
        print(f"{size(t)} nodes, kind {kind}: {show(is_complete_tree(t))}")
    path = TreeNode(100)
    for k in range(1, 100):
        path = TreeNode(100 - k, path)
    print(f"a path of 100 nodes: {show(is_complete_tree(path))}")


main()
