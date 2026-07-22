"""LeetCode 206 — Reverse Linked List (Python mirror / oracle).

Iterative three-cursor reversal (prev/cur/nxt) on an index-pool list (list of
nodes, i64 next, -1 = null). Mirrors the Kāra version.
"""


class Node:
    def __init__(self, val, nxt):
        self.val = val
        self.next = nxt


def build(vals):
    nodes = []
    n = len(vals)
    for i in range(n):
        nodes.append(Node(vals[i], i + 1 if i + 1 < n else -1))
    return nodes


def reverse(nodes, head):
    prev = -1
    cur = head
    while cur != -1:
        nxt = nodes[cur].next
        nodes[cur].next = prev
        prev = cur
        cur = nxt
    return prev


def show(nodes, head):
    out = []
    cur = head
    while cur != -1:
        out.append(str(nodes[cur].val))
        cur = nodes[cur].next
    print(" ".join(out))


def report(vals):
    nodes = build(vals)
    head = 0 if nodes else -1
    show(nodes, reverse(nodes, head))


def main():
    report([1, 2, 3, 4, 5])
    report([1, 2])
    report([])
    report([7])
    report([-1, 0, 9, -3])


main()
