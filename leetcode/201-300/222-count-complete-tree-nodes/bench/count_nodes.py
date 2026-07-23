"""Benchmark workload for LeetCode #222 — Count Complete Tree Nodes (Python; scale lane)."""

import sys


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def build(n):
    nodes = []
    for i in range(n):
        l = 2 * i + 1
        r = 2 * i + 2
        lc = l if l < n else -1
        rc = r if r < n else -1
        nodes.append(Node(i, lc, rc))
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


def main():
    n = 2000000
    passes = 2000000
    top_span = 2048
    modulus = 1000000007

    nodes = build(n)

    sink = 0
    for p in range(passes):
        start = p % top_span
        sink = (sink + count_nodes(nodes, start)) % modulus
    print(sink)


sys.setrecursionlimit(10000)
main()
