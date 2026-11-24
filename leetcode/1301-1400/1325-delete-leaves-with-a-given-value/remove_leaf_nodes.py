# LeetCode #1325: Delete Leaves With a Given Value -- Python mirror of the ★
# Kāra arm: a recursive walk that settles both children first, so that a
# node whose children were both deleted is already a leaf when it is looked
# at; a leaf with the target's value is deleted by returning None in its
# place.
import sys
from collections import deque

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def remove_leaf_nodes(root, target):
    if root is None:
        return None
    root.left = remove_leaf_nodes(root.left, target)
    root.right = remove_leaf_nodes(root.right, target)
    if root.left is None and root.right is None and root.val == target:
        return None
    return root


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level(values):
    if not values or values[0] is None:
        return None
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


def to_level(root):
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is not None:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


def show(root):
    return "[" + ",".join("null" if v is None else str(v) for v in to_level(root)) + "]"


def ask(values, target):
    return show(remove_leaf_nodes(from_level(values), target))


def random_tree(n, k, deep):
    root = TreeNode(1 + next_random() % k)
    places = [(root, True), (root, False)]
    for _ in range(1, n):
        r = next_random()
        if deep and r % 4 != 0:
            at = len(places) - 1 - next_random() % 2
        else:
            at = next_random() % len(places)
        parent, left = places[at]
        places[at] = places[-1]
        places.pop()
        node = TreeNode(1 + next_random() % k)
        if left:
            parent.left = node
        else:
            parent.right = node
        places.append((node, True))
        places.append((node, False))
    return root


def main():
    global seed
    N = None
    e1 = ask([1, 2, 3, 2, N, 2, 4], 2)
    e2 = ask([1, 3, 3, 3, 2], 3)
    e3 = ask([1, 2, N, 2, N, 2], 2)
    e4 = ask([7], 7)
    chain = None
    for _ in range(3000):
        chain = TreeNode(5, chain, None)
    e5 = show(remove_leaf_nodes(chain, 5))
    chain2 = None
    for _ in range(2999):
        chain2 = TreeNode(5, chain2, None)
    e6 = show(remove_leaf_nodes(TreeNode(6, chain2, None), 5))
    full = [1000] * 2047
    full[0] = 1
    e7 = ask(full, 1000)
    print(f"{e1} {e2} {e3} {e4} {e5} {e6} {e7}")
    seed = 1325
    total = 0
    check = 0
    for t in range(1000):
        n = 1 + next_random() % 3000 if t % 10 == 0 else 1 + next_random() % 60
        k = 2 if t % 3 == 0 else 3 if t % 3 == 1 else 1000
        root = random_tree(n, k, t % 2 == 1)
        target = 1 + next_random() % min(k, 3)
        for v in to_level(remove_leaf_nodes(root, target)):
            if v is not None:
                total += 1
                check = (check * 131 + v) % 1000000007
            else:
                check = (check * 131 + 1001) % 1000000007
        check = (check * 131 + 1002) % 1000000007
    print(f"1000 random trees: nodes left {total}, checksum {check}")


main()
