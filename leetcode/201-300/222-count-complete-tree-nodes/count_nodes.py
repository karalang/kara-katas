"""LeetCode 222 — Count Complete Tree Nodes (Python mirror / oracle).

Index-pool complete tree (children 2i+1, 2i+2); O(log^2 n) count via left/right
spine heights (perfect subtree => 2^h - 1, else recurse). Mirrors the Kara
version.
"""


class Node:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def build(vals):
    n = len(vals)
    nodes = []
    for i in range(n):
        l = 2 * i + 1
        r = 2 * i + 2
        lc = l if l < n else -1
        rc = r if r < n else -1
        nodes.append(Node(vals[i], lc, rc))
    return nodes


def left_height(nodes, idx):
    h = 0
    cur = idx
    while cur != -1:
        h += 1
        cur = nodes[cur].left
    return h


def right_height(nodes, idx):
    h = 0
    cur = idx
    while cur != -1:
        h += 1
        cur = nodes[cur].right
    return h


def count_nodes(nodes, idx):
    if idx == -1:
        return 0
    lh = left_height(nodes, idx)
    rh = right_height(nodes, idx)
    if lh == rh:
        return (1 << lh) - 1
    return 1 + count_nodes(nodes, nodes[idx].left) + count_nodes(nodes, nodes[idx].right)


def report(vals):
    nodes = build(vals)
    root = 0 if nodes else -1
    print(count_nodes(nodes, root))


def main():
    report([1, 2, 3, 4, 5, 6])
    report([1, 2, 3, 4, 5, 6, 7])
    report([])
    report([1])
    report([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    report([1, 2])
    report([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])


main()
