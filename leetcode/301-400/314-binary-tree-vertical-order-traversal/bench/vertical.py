"""Benchmark lane for LeetCode 314 — Python mirror of bench/vertical.kara.

Grow POOL random trees of NODES nodes once, then PASSES vertical-order
traversals (extent pass + level-frontier BFS into an offset-indexed list of
lists), each on the tree the running checksum selects. Every column's length
and every value is folded into the masked checksum.
"""
import sys

POOL = 8
NODES = 50000
PASSES = 240
MASK = 1073741823


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def lcg(s):
    return (s * 1103515245 + 12345) & 0x7FFFFFFF


def grow(n, seed):
    # seed is a one-element list, the mutable cell the other mirrors pass by reference.
    if n <= 0:
        return None
    seed[0] = lcg(seed[0])
    v = seed[0] % 1000 - 500
    seed[0] = lcg(seed[0])
    left_n = 0 if n <= 1 else seed[0] % n
    right_n = n - 1 - left_n
    l = grow(left_n, seed)
    r = grow(right_n, seed)
    return Node(v, l, r)


def extent(t, col, box):
    if t is None:
        return
    if col < box[0]:
        box[0] = col
    if col > box[1]:
        box[1] = col
    extent(t.left, col - 1, box)
    extent(t.right, col + 1, box)


def vertical_order(root):
    out = []
    if root is None:
        return out
    box = [0, 0]
    extent(root, 0, box)
    lo, hi = box
    out = [[] for _ in range(hi - lo + 1)]
    current = [(root, 0)]
    while current:
        nxt = []
        for n, c in current:
            out[c - lo].append(n.val)
            if n.left is not None:
                nxt.append((n.left, c - 1))
            if n.right is not None:
                nxt.append((n.right, c + 1))
        current = nxt
    return out


def main():
    sys.setrecursionlimit(10000)
    seed = [314159]
    pool = [grow(NODES, seed) for _ in range(POOL)]
    checksum = 0
    for _ in range(PASSES):
        which = checksum % POOL
        cols = vertical_order(pool[which])
        checksum = (checksum + len(cols)) & MASK
        for col in cols:
            checksum = (checksum * 31 + len(col)) & MASK
            for v in col:
                checksum = (checksum + v + 500) & MASK
    print(f"checksum {checksum}")


if __name__ == "__main__":
    main()
