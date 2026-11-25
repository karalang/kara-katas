# LeetCode #1373: Maximum Sum BST in Binary Tree -- Python mirror of the ★
# arm: each subtree reports whether it is a search tree, its smallest and
# largest key, and its sum, from the leaves up.
import sys
from collections import deque

sys.setrecursionlimit(50000)

INF = 1 << 62


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def summarize(node, best):
    if node is None:
        return True, INF, -INF, 0
    ls, llo, lhi, lsum = summarize(node.left, best)
    rs, rlo, rhi, rsum = summarize(node.right, best)
    key = node.val
    if ls and rs and lhi < key < rlo:
        total = lsum + key + rsum
        best[0] = max(best[0], total)
        return True, min(llo, key), max(rhi, key), total
    return False, 0, 0, 0


def max_sum_bst(root):
    best = [0]
    summarize(root, best)
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


def draw(rng):
    return next_random() % (2 * rng + 1) - rng


def random_tree(n, rng):
    root = TreeNode(draw(rng))
    places = [(root, True), (root, False)]
    for _ in range(1, n):
        k = next_random() % len(places)
        parent, left = places[k]
        places[k] = places[-1]
        places.pop()
        node = TreeNode(draw(rng))
        if left:
            parent.left = node
        else:
            parent.right = node
        places.append((node, True))
        places.append((node, False))
    return root


def random_search_tree(n, rng, noise):
    root = TreeNode(draw(rng))
    for _ in range(1, n):
        key = draw(rng)
        at = root
        while key != at.val:
            child = at.left if key < at.val else at.right
            if child is None:
                if key < at.val:
                    at.left = TreeNode(key)
                else:
                    at.right = TreeNode(key)
                break
            at = child
    for _ in range(noise):
        at = root
        for _ in range(next_random() % 8):
            child = at.left if next_random() % 2 == 0 else at.right
            if child is None:
                break
            at = child
        at.val = draw(rng)
    return root


def main():
    global seed
    N = None
    examples = [
        [1, 4, 3, 2, 4, 2, 5, N, N, N, N, N, N, 4, 6],
        [4, 3, N, 1, 2],
        [-4, -2, -5],
        [2, 1, 3],
        [5, 4, 8, 3, N, 6, 3],
    ]
    shown = [str(max_sum_bst(from_level(level))) for level in examples]
    chain = None
    for v in range(10000):
        chain = TreeNode(10000 - v, None, chain)
    shown.append(str(max_sum_bst(chain)))
    print(" ".join(shown))
    seed = 1373
    total = 0
    check = 0
    for k in range(2000):
        n = 1 + next_random() % 300
        rng = 10 if next_random() % 2 == 0 else 10000
        if k % 2 == 0:
            root = random_tree(n, rng)
        else:
            root = random_search_tree(n, rng, next_random() % 4)
        got = max_sum_bst(root)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random trees: sums total {total}, checksum {check}")


main()
