# LeetCode #1379: Find a Corresponding Node of a Binary Tree in a Clone of
# That Tree -- Python mirror of the ★ arm: the two trees walked together,
# depth first; the clone's node where the original's is the target itself
# is the answer.

import sys
from collections import deque

sys.setrecursionlimit(100000)

seed = 1379


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find(o, c, target):
    if o is target:
        return c
    if o.left is not None and c.left is not None:
        found = find(o.left, c.left, target)
        if found is not None:
            return found
    if o.right is not None and c.right is not None:
        return find(o.right, c.right, target)
    return None


def get_target_copy(original, cloned, target):
    return find(original, cloned, target)


def from_level(values):
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while i < len(values):
        if not queue:
            break
        node = queue.popleft()
        if values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


def clone_tree(root):
    # iterative, node for node, so a chain of 10^4 needs no deep recursion
    copy = TreeNode(root.val)
    stack = [(root, copy)]
    while stack:
        o, c = stack.pop()
        if o.left is not None:
            c.left = TreeNode(o.left.val)
            stack.append((o.left, c.left))
        if o.right is not None:
            c.right = TreeNode(o.right.val)
            stack.append((o.right, c.right))
    return copy


def pairs(original, cloned):
    out = [(original, cloned)]
    i = 0
    while i < len(out):
        o, c = out[i]
        if o.left is not None and c.left is not None:
            out.append((o.left, c.left))
        if o.right is not None and c.right is not None:
            out.append((o.right, c.right))
        i += 1
    return out


def random_tree(n, kind):
    values = [v * 37 % 100003 for v in range(1, n + 1)]
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    root = TreeNode(values[0])
    places = [(root, True), (root, False)]
    for k in range(1, n):
        if kind == 0:
            at = next_random() % len(places)
        elif kind == 1:
            at = len(places) - 1 - next_random() % 2
        else:
            at = next_random() % 2
        parent, left = places.pop(at)
        node = TreeNode(values[k])
        if left:
            parent.left = node
        else:
            parent.right = node
        places.append((node, True))
        places.append((node, False))
    return root


def ask(both, original, cloned, k):
    target, copy = both[k]
    found = get_target_copy(original, cloned, target)
    return found.val, found is copy


def show(v, own):
    return f"{v}" if own else f"{v}?"


def main():
    shown = []
    examples = [
        ([7, 4, 3, None, None, 6, 19], 3),
        ([7], 7),
        ([8, None, 6, None, 5, None, 4, None, 3, None, 2, None, 1], 4),
    ]
    for level, want in examples:
        original = from_level(level)
        cloned = clone_tree(original)
        both = pairs(original, cloned)
        k = next(i for i, p in enumerate(both) if p[0].val == want)
        shown.append(show(*ask(both, original, cloned, k)))
    chain = TreeNode(1)
    for v in range(2, 10001):
        chain = TreeNode(v, chain, None)
    chain_copy = clone_tree(chain)
    shown.append(show(*ask(pairs(chain, chain_copy), chain, chain_copy, 9999)))
    full = from_level(list(range(1, 10001)))
    full_copy = clone_tree(full)
    full_pairs = pairs(full, full_copy)
    for k in [9999, 4321]:
        shown.append(show(*ask(full_pairs, full, full_copy, k)))
    print(" ".join(shown))
    own_copies = 0
    check = 0
    for c in range(2000):
        n = 1 + next_random() % 300
        original = random_tree(n, c % 3)
        cloned = clone_tree(original)
        both = pairs(original, cloned)
        k = next_random() % n
        v, own = ask(both, original, cloned, k)
        if own:
            own_copies += 1
        check = (check * 131 + v) % 1000000007
    print(f"2000 random trees: {own_copies} own copies found, checksum {check}")


main()
