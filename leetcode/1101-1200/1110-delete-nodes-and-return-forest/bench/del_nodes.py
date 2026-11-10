# LeetCode #1110: Delete Nodes And Return Forest -- the bench's Python
# mirror: the ★ arm over the same 16 trees of 1000 nodes and rounds.
import sys

sys.setrecursionlimit(10000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def prune(node, parent_gone, gone, roots):
    if node is None:
        return None
    deleted = node.val in gone
    if parent_gone and not deleted:
        roots.append(node)
    node.left = prune(node.left, deleted, gone, roots)
    node.right = prune(node.right, deleted, gone, roots)
    return None if deleted else node


def del_nodes(root, to_delete):
    gone = set(to_delete)
    roots = []
    prune(root, True, gone, roots)
    return roots


seed = 1110


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shape():
    values = list(range(1, 1001))
    for i in range(1000):
        j = i + next_random() % (1000 - i)
        values[i], values[j] = values[j], values[i]
    left = [-1] * 1000
    right = [-1] * 1000
    for k in range(1, 1000):
        while True:
            at = next_random() % k
            if next_random() % 2 == 0:
                if left[at] < 0:
                    left[at] = k
                    break
            elif right[at] < 0:
                right[at] = k
                break
    return values, left, right


def build(s):
    values, left, right = s
    nodes = [TreeNode(v) for v in values]
    for k in range(1000):
        if left[k] >= 0:
            nodes[k].left = nodes[left[k]]
        if right[k] >= 0:
            nodes[k].right = nodes[right[k]]
    return nodes[0]


def main():
    shapes = [shape() for _ in range(16)]
    trees = 0
    check = 0
    for rnd in range(200):
        for j in range(len(shapes)):
            third = (rnd + j) % 3
            to_delete = [v for v in range(1, 1001) if v % 3 == third]
            roots = del_nodes(build(shapes[j]), to_delete)
            trees += len(roots)
            for r in roots:
                check = (check * 31 + r.val) % 1000000007
    print(f"200 rounds over 16 trees of 1000 nodes: {trees} trees, checksum {check}")


main()
