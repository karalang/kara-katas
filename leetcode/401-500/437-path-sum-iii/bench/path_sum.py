# Benchmark for #437: mirror of path_sum.kara (prefix sums along the
# path) on one random tree of 100,000 nodes, queried for 200 targets.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def count_from(node, prefix, target, seen):
    if node is None:
        return 0
    total = prefix + node.val
    found = seen.get(total - target, 0)
    seen[total] = seen.get(total, 0) + 1
    found += count_from(node.left, total, target, seen)
    found += count_from(node.right, total, target, seen)
    seen[total] -= 1
    return found


def path_sum(root, target):
    return count_from(root, 0, target, {0: 1})


seed = 437


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    size = 100000
    queries = 200
    # Each node hangs under a random earlier node that still has a free
    # side, values in [-1000, 1000].
    root = TreeNode(next_random() % 2001 - 1000)
    open_nodes = [root]
    for _ in range(1, size):
        at = next_random() % len(open_nodes)
        parent = open_nodes[at]
        child = TreeNode(next_random() % 2001 - 1000)
        if parent.left is None and (parent.right is not None or next_random() % 2 == 0):
            parent.left = child
        else:
            parent.right = child
        if parent.left is not None and parent.right is not None:
            open_nodes[at] = open_nodes[-1]
            open_nodes.pop()
        open_nodes.append(child)
    total = 0
    checksum = 0
    for _ in range(queries):
        target = next_random() % 4001 - 2000
        count = path_sum(root, target)
        total += count
        checksum = (checksum * 31 + count) % 1000000007
    print(f"{queries} targets on a tree of {size}: {total} paths, checksum {checksum}")


main()
