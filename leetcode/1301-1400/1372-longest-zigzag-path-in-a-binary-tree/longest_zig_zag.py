# LeetCode #1372: Longest ZigZag Path in a Binary Tree -- Python mirror of
# the ★ arm: each node reports the longest zigzag starting at it going
# left and going right, each one more than its child's the other way.
import sys
from collections import deque

sys.setrecursionlimit(50000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lengths(node, best):
    left = right = 0
    if node.left is not None:
        left = 1 + lengths(node.left, best)[1]
    if node.right is not None:
        right = 1 + lengths(node.right, best)[0]
    best[0] = max(best[0], left, right)
    return left, right


def longest_zig_zag(root):
    best = [0]
    if root is not None:
        lengths(root, best)
    return best[0]


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
    e1 = longest_zig_zag(from_level([1, N, 1, 1, 1, N, N, 1, 1, N, 1, N, N, N, 1]))
    e2 = longest_zig_zag(from_level([1, 1, 1, N, 1, N, N, 1, 1, N, 1]))
    e3 = longest_zig_zag(from_level([1]))
    zig = None
    for k in range(10000):
        zig = TreeNode(1, zig, None) if k % 2 == 0 else TreeNode(1, None, zig)
    print(f"{e1} {e2} {e3} {longest_zig_zag(zig)}")
    seed = 1372
    total = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 300
        got = longest_zig_zag(random_tree(n))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random trees: lengths total {total}, checksum {check}")


main()
