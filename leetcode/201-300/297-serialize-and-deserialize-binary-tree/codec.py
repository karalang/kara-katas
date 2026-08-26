"""LeetCode 297 - Serialize and Deserialize Binary Tree (preorder + sentinels).

Mirror of codec.kara: same algorithm, same output.

Preorder walk emitting `#` at every empty slot, and a deserializer that
consumes the token list in exactly that order through one moving cursor. See
the Kara file's header for why the nulls, not the values, are the problem.
"""

import sys


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def node(v, l=None, r=None):
    return TreeNode(v, l, r)


def leaf(v):
    return TreeNode(v)


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


def de_at(tokens, i):
    """Returns (node, next_index). `i` is the cursor Kara passes as `mut ref`."""
    tok = tokens[i]
    i += 1
    if tok == "#":
        return None, i
    v = int(tok)
    l, i = de_at(tokens, i)
    r, i = de_at(tokens, i)
    return node(v, l, r), i


def deserialize(s):
    if len(s) == 0:
        return None
    tokens = s.split(",")
    t, _ = de_at(tokens, 0)
    return t


def report(t):
    s = serialize(t)
    print(f"{s}  |  round-trip {serialize(deserialize(s))}")


def main():
    sys.setrecursionlimit(100000)
    report(node(1, leaf(2), node(3, leaf(4), leaf(5))))
    report(None)
    report(leaf(7))
    report(node(-1, leaf(-2), None))
    report(node(5, node(5, leaf(5), None), leaf(5)))


if __name__ == "__main__":
    main()
