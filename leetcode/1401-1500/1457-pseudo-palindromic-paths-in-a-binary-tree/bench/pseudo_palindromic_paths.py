# LeetCode #1457 bench in Python: the ★ arm (a walk down by recursion,
# the parity of the values on the path carried as a bit mask) on the same
# 50 trees of 10^4 nodes and 50 passes.
from collections import deque


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def pseudo_palindromic_paths(root):
    return paths(root, 0)


# the pseudo-palindromic paths through `node`, `seen` with bit v set when
# the value v is on the path above it an odd number of times: at a leaf
# the path can be rearranged into a palindrome when at most one bit is set
def paths(node, seen):
    if node is None:
        return 0
    seen ^= 1 << node.val
    if node.left is None and node.right is None:
        return 1 if seen & (seen - 1) == 0 else 0
    return paths(node.left, seen) + paths(node.right, seen)


seed = 1457


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(n, level_order):
    root = TreeNode(1 + next_random() % 9)
    nodes = [root]
    if level_order:
        level = deque([root])
        while len(nodes) < n:
            at = level.popleft()
            for side in range(2):
                if len(nodes) < n and next_random() % 4 != 0:
                    node = TreeNode(1 + next_random() % 9)
                    if side == 0:
                        at.left = node
                    else:
                        at.right = node
                    level.append(node)
                    nodes.append(node)
            if not level:
                level.append(at)
    else:
        places = [(root, True), (root, False)]
        while len(nodes) < n:
            k = next_random() % len(places)
            parent, left = places[k]
            places[k] = places[-1]
            places.pop()
            node = TreeNode(1 + next_random() % 9)
            if left:
                parent.left = node
            else:
                parent.right = node
            places.append((node, True))
            places.append((node, False))
            nodes.append(node)
    return nodes


def main():
    n = 10000
    trees = [build(n, t % 2 == 1) for t in range(50)]
    check = 0
    for p in range(50):
        for t in range(50):
            nodes = trees[t]
            nodes[check % n].val = 1 + (check // 7) % 9
            found = pseudo_palindromic_paths(nodes[0])
            check = (check * 31 + found + p) % 90000007
    print(f"50 passes over 50 trees of 10^4: checksum {check}")


main()
