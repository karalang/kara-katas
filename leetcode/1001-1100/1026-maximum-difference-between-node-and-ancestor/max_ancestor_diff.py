# LeetCode #1026: Maximum Difference Between Node and Ancestor -- recursion
# Mirrors max_ancestor_diff.kara (the ★ arm) and prints the same output.

import sys
from collections import deque

sys.setrecursionlimit(20000)


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def max_ancestor_diff(root):
    if root is None:
        return 0
    return best_below(root, root.val, root.val)


def best_below(node, low, high):
    if node is None:
        return high - low
    lo = min(low, node.val)
    hi = max(high, node.val)
    return max(best_below(node.left, lo, hi), best_below(node.right, lo, hi))


seed = 1026


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_level_order(values):
    if not values or values[0] < 0:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    k = 1
    while k < len(values):
        node = queue.popleft()
        if values[k] >= 0:
            node.left = TreeNode(values[k])
            queue.append(node.left)
        k += 1
        if k < len(values) and values[k] >= 0:
            node.right = TreeNode(values[k])
            queue.append(node.right)
        k += 1
    return root


def random_value(top):
    high = next_random()
    return (high * 32768 + next_random()) % top


def random_tree(n, top):
    root = TreeNode(random_value(top))
    placed = 1
    while placed < n:
        node = root
        while True:
            go_left = next_random() % 2 == 0
            nxt = node.left if go_left else node.right
            if nxt is not None:
                node = nxt
            else:
                leaf = TreeNode(random_value(top))
                if go_left:
                    node.left = leaf
                else:
                    node.right = leaf
                placed += 1
                break
    return root


def chain(n, zigzag):
    root = TreeNode(0)
    node = root
    for k in range(1, n):
        if zigzag:
            v = k if k % 2 == 0 else 100000 - k
        else:
            v = k * 20
        node.right = TreeNode(v)
        node = node.right
    return root


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    examples = [
        [8, 3, 10, 1, 6, -1, 14, -1, -1, 4, 7, 13],
        [1, -1, 2, -1, 0, 3],
        [5, 5],
        [0, 100000],
        [7, 1, 9, -1, 4, 2, 12],
        [50, 40, 60, 30, 45, 55, 70, 45, -1, -1, 46, 54],
        [3, 3, 3, 3, -1, -1, 3, 0],
    ]
    for values in examples:
        print(f"{show(values)} -> {max_ancestor_diff(from_level_order(values))}")
    groups = [(3000, 7, 10), (1000, 30, 100), (300, 200, 100000), (300, 200, 2), (50, 1000, 100000), (10, 5000, 100000)]
    for count, n, top in groups:
        total = 0
        most = 0
        check = 0
        for _ in range(count):
            answer = max_ancestor_diff(random_tree(n, top))
            total += answer
            most = max(most, answer)
            check = (check * 31 + answer) % 1000000007
        print(f"{count} random trees of {n} nodes (values below {top}): sum {total}, most {most}, checksum {check}")
    print(f"a rising chain of 5000: {max_ancestor_diff(chain(5000, False))}; a zigzag chain of 5000: {max_ancestor_diff(chain(5000, True))}")


main()
