# LeetCode #1302: Deepest Leaves Sum -- Python mirror of the ★ arm (a
# breadth-first walk a level at a time, each level's values summed afresh).
from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def deepest_leaves_sum(root):
    queue = deque()
    if root is not None:
        queue.append(root)
    total = 0
    while queue:
        total = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            total += node.val
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
    return total


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
    e1 = deepest_leaves_sum(from_level([1, 2, 3, 4, 5, N, 6, 7, N, N, N, N, 8]))
    e2 = deepest_leaves_sum(from_level([6, 7, 8, 2, 7, 1, 3, 9, N, 1, 4, N, N, N, 5]))
    one = deepest_leaves_sum(from_level([42]))
    chain = None
    for v in range(10000):
        chain = TreeNode(v % 100 + 1, None, chain)
    full = [i % 100 + 1 for i in range(8191)]
    print(f"{e1} {e2} {one} {deepest_leaves_sum(chain)} {deepest_leaves_sum(from_level(full))}")
    seed = 1302
    total = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 300
        got = deepest_leaves_sum(random_tree(n))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random trees: sums total {total}, checksum {check}")


main()
