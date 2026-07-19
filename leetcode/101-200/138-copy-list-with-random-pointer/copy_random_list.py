"""LeetCode 138 — Copy List with Random Pointer (Python mirror / oracle).

Same algorithm as copy_random_list.kara: build the original list from parallel
arrays, deep-copy by cloning every node then re-wiring `next` and `random`
against the fresh copies (indexed by id). The Kāra version models `random` as a
`weak` reference (non-owning) so the random-cyclic graph is reclaimed cleanly;
Python is GC'd, so the mirror just uses ordinary references.
"""


class Node:
    def __init__(self, val, id):
        self.val = val
        self.id = id
        self.next = None
        self.random = None


def build(vals, rnd):
    nodes = [Node(vals[i], i) for i in range(len(vals))]
    for i in range(len(vals)):
        if i + 1 < len(vals):
            nodes[i].next = nodes[i + 1]
        if rnd[i] >= 0:
            nodes[i].random = nodes[rnd[i]]
    return nodes


def deep_copy(orig):
    n = len(orig)
    copies = [Node(orig[i].val, orig[i].id) for i in range(n)]
    for i in range(n):
        if i + 1 < n:
            copies[i].next = copies[i + 1]
        if orig[i].random is not None:
            copies[i].random = copies[orig[i].random.id]
    return copies


def main():
    vals = [7, 13, 11, 10, 1]
    rnd = [-1, 0, 4, 2, 0]
    orig = build(vals, rnd)
    copies = deep_copy(orig)
    for c in copies:
        rv = c.random.val if c.random is not None else -1
        print(f"{c.val}|{rv}")


main()
