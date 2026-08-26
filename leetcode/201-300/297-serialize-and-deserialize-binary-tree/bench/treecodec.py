"""LeetCode 297 benchmark lane - Python mirror of treecodec.kara.

Same algorithm, same tree shape, same sink: build one balanced 200k-node tree,
then 24 chained serialize/deserialize round trips, hashing every encoded
string. See the .kara file's header for the workload rationale.
"""

import sys


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def build(vals, lo, hi):
    if lo >= hi:
        return None
    mid = lo + (hi - lo) // 2
    l = build(vals, lo, mid)
    r = build(vals, mid + 1, hi)
    return Node(vals[mid], l, r)


def ser_into(t, out):
    if t is None:
        out.append("#")
        return
    out.append(str(t.val))
    ser_into(t.left, out)
    ser_into(t.right, out)


def serialize(t):
    out = []
    ser_into(t, out)
    return ",".join(out)


def de_at(toks, i):
    tok = toks[i]
    i += 1
    if tok == "#":
        return None, i
    v = int(tok)
    l, i = de_at(toks, i)
    r, i = de_at(toks, i)
    return Node(v, l, r), i


def deserialize(s):
    toks = s.split(",")
    t, _ = de_at(toks, 0)
    return t


def hash_string(s, seed):
    h = seed
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    sys.setrecursionlimit(200000)
    n = 200000
    rounds = 24

    vals = []
    state = 12345
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        vals.append(state % 1000003 - 500000)

    tree = build(vals, 0, n)
    checksum = 0

    for _ in range(rounds):
        s = serialize(tree)
        checksum = hash_string(s, checksum)
        tree = deserialize(s)

    print(f"nodes {n} rounds {rounds} checksum {checksum}")


if __name__ == "__main__":
    main()
