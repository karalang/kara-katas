# LeetCode #1315: Sum of Nodes with Even-Valued Grandparent -- Python mirror
# of the ★ arm (a recursive walk handing each child its parent's and
# grandparent's values).
import sys
from collections import deque

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def walk(node, parent, grandparent):
    if node is None:
        return 0
    mine = node.val if grandparent % 2 == 0 else 0
    return mine + walk(node.left, node.val, parent) + walk(node.right, node.val, parent)


def sum_even_grandparent(root):
    return walk(root, 1, 1)


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


def random_tree(n):
    root = TreeNode(1 + next_random() % 100)
    places = [(root, True), (root, False)]
    for _ in range(1, n):
        k = next_random() % len(places)
        parent, left = places[k]
        places[k] = places[-1]
        places.pop()
        node = TreeNode(1 + next_random() % 100)
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
    e1 = sum_even_grandparent(from_level([6, 7, 8, 2, 7, 1, 3, 9, N, 1, 4, N, N, N, 5]))
    e2 = sum_even_grandparent(from_level([1]))
    chain = None
    for v in range(10000):
        chain = TreeNode(2 * (v % 50) + 2, None, chain)
    full = [i % 100 + 1 for i in range(8191)]
    print(f"{e1} {e2} {sum_even_grandparent(chain)} {sum_even_grandparent(from_level(full))}")
    seed = 1315
    total = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 300
        got = sum_even_grandparent(random_tree(n))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random trees: sums total {total}, checksum {check}")


main()
