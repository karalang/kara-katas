# LeetCode #1367: Linked List in Binary Tree -- Python mirror of the ★
# arm: every tree node tried as the start of the list, and from each the
# list matched down the tree, either child carrying the next value.
import sys
from collections import deque

sys.setrecursionlimit(20000)


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def matches_from(head, node):
    if head is None:
        return True
    if node is None:
        return False
    return head.val == node.val and (matches_from(head.next, node.left) or matches_from(head.next, node.right))


def is_sub_path(head, root):
    if root is None:
        return False
    return matches_from(head, root) or is_sub_path(head, root.left) or is_sub_path(head, root.right)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_values(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


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


def random_tree(n, rng):
    root = TreeNode(1 + next_random() % rng)
    places = [(root, True), (root, False)]
    for _ in range(1, n):
        k = next_random() % len(places)
        parent, left = places[k]
        places[k] = places[-1]
        places.pop()
        node = TreeNode(1 + next_random() % rng)
        if left:
            parent.left = node
        else:
            parent.right = node
        places.append((node, True))
        places.append((node, False))
    return root


def random_child(node):
    if node.left is not None and node.right is not None:
        return node.left if next_random() % 2 == 0 else node.right
    return node.left if node.left is not None else node.right


def path_values(root, m):
    at = root
    for _ in range(next_random() % 12):
        child = random_child(at)
        if child is None:
            break
        at = child
    values = [at.val]
    while len(values) < m:
        child = random_child(at)
        if child is None:
            break
        values.append(child.val)
        at = child
    return values


def main():
    global seed
    N = None
    tree = [1, 4, 4, N, 2, 2, N, 1, N, 6, 8, N, N, N, N, 1, 3]
    e1 = is_sub_path(from_values([4, 2, 8]), from_level(tree))
    e2 = is_sub_path(from_values([1, 4, 2, 6]), from_level(tree))
    e3 = is_sub_path(from_values([1, 4, 2, 6, 8]), from_level(tree))
    chain = None
    for _ in range(2500):
        chain = TreeNode(1, None, chain)
    a = is_sub_path(from_values([1] * 100), chain)
    b = is_sub_path(from_values([1] * 99 + [2]), chain)
    print(" ".join(str(x).lower() for x in (e1, e2, e3, a, b)))
    seed = 1367
    found = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 300
        rng = [2, 3, 100][next_random() % 3]
        root = random_tree(n, rng)
        m = 1 + next_random() % (4 if next_random() % 2 == 0 else 12)
        if next_random() % 2 == 0:
            values = path_values(root, m)
        else:
            values = [1 + next_random() % rng for _ in range(m)]
        got = is_sub_path(from_values(values), root)
        found += got
        check = (check * 131 + len(values) * 2 + (1 if got else 0)) % 1000000007
    print(f"2000 random trees: {found} found, checksum {check}")


main()
