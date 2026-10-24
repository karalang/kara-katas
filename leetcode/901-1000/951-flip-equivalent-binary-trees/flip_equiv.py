# LeetCode #951: Flip Equivalent Binary Trees -- both pairings tried.
# Mirrors flip_equiv.kara (the ★ arm) and its harness.
from collections import deque


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def flip_equiv(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and (
        (flip_equiv(a.left, b.left) and flip_equiv(a.right, b.right))
        or (flip_equiv(a.left, b.right) and flip_equiv(a.right, b.left)))


seed = 951


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


def random_tree(values):
    if not values:
        return None
    root = TreeNode(values[0])
    for v in values[1:]:
        attach(root, TreeNode(v))
    return root


def flipped_copy(t, rename):
    if t is None:
        return None
    l = flipped_copy(t.left, rename)
    r = flipped_copy(t.right, rename)
    if next_random() % 2 == 0:
        return TreeNode(rename[t.val], l, r)
    return TreeNode(rename[t.val], r, l)


def is_leaf(n):
    return n.left is None and n.right is None


def detach_leaf(root):
    parents = []
    sides = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node.left is not None:
            if is_leaf(node.left):
                parents.append(node)
                sides.append(0)
            else:
                stack.append(node.left)
        if node.right is not None:
            if is_leaf(node.right):
                parents.append(node)
                sides.append(1)
            else:
                stack.append(node.right)
    if not parents:
        return None
    k = next_random() % len(parents)
    p = parents[k]
    if sides[k] == 0:
        leaf = p.left
        p.left = None
    else:
        leaf = p.right
        p.right = None
    return leaf


def some_values(n):
    v = list(range(100))
    for i in range(n):
        j = i + next_random() % (100 - i)
        v[i], v[j] = v[j], v[i]
    return v[:n]


def partner(t, values, kind):
    rename = list(range(100))
    if kind == 1 and len(values) >= 2:
        a = values[next_random() % len(values)]
        b = values[next_random() % len(values)]
        rename[a] = b
        rename[b] = a
    if kind == 3:
        shuffled = list(values)
        for i in range(len(shuffled)):
            j = i + next_random() % (len(shuffled) - i)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        if shuffled:
            for i in range(len(shuffled)):
                if shuffled[i] == values[0]:
                    shuffled[0], shuffled[i] = shuffled[i], shuffled[0]
        return random_tree(shuffled)
    copy = flipped_copy(t, rename)
    if copy is not None:
        if kind == 2:
            leaf = detach_leaf(copy)
            if leaf is not None:
                attach(copy, leaf)
        elif kind == 4:
            if is_leaf(copy):
                return None
            detach_leaf(copy)
    return copy


def main():
    N = None
    cases = [
        ([1, 2, 3, 4, 5, 6, N, N, N, 7, 8], [1, 3, 2, N, 6, 4, 5, N, N, N, N, 8, 7]),
        ([], []),
        ([], [1]),
        ([1], [1]),
        ([1], [2]),
        ([1, 2], [1, N, 2]),
        ([1, 2, 3, 4], [1, 3, 2, N, N, 4]),
        ([1, 2, 3, 4], [1, 3, 2, 4]),
        ([0, 1, 2], [0, 1, N, 2]),
    ]
    for i, (a, b) in enumerate(cases):
        print(f"case {i + 1}: {str(flip_equiv(from_level_order(a), from_level_order(b))).lower()}")
    nodes = 0
    yes = 0
    by_kind = [0, 0, 0, 0, 0]
    check = 0
    for _ in range(300):
        n = next_random() % 13
        values = some_values(n)
        t = random_tree(values)
        kind = next_random() % 5
        u = partner(t, values, kind)
        nodes += n
        bit = 1 if flip_equiv(t, u) else 0
        yes += bit
        by_kind[kind] += bit
        check = (check * 31 + bit + 1) % 1000000007
    print(f"300 random pairs, the first trees of {nodes} nodes: {yes} flip equivalent ({by_kind[0]}, {by_kind[1]}, {by_kind[2]}, {by_kind[3]}, {by_kind[4]} by kind), checksum {check}")
    for kind in range(5):
        values = some_values(100)
        t = random_tree(values)
        u = partner(t, values, kind)
        print(f"100 nodes, kind {kind}: {str(flip_equiv(t, u)).lower()}")
    lefts = TreeNode(99)
    rights = TreeNode(99)
    for k in range(98, -1, -1):
        lefts = TreeNode(k, lefts, None)
        rights = TreeNode(k, None, rights)
    print(f"a path of 100 nodes and its mirror: {str(flip_equiv(lefts, rights)).lower()}")


main()
