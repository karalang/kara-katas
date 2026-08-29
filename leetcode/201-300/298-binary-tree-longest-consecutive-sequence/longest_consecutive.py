"""LeetCode 298 - Binary Tree Longest Consecutive Sequence (bottom-up).

Mirror of longest_consecutive.kara: same algorithm, same output.

Each node answers one local question - "how long is the consecutive run whose
first node is me?" - and the global maximum is folded in during the walk. See
the Kara file's header for why the local and global quantities must stay
separate.
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


def down(t, best):
    """Returns the run starting at `t`; `best` is a one-element list acting as
    Kara's `mut ref i64`."""
    if t is None:
        return 0
    l = down(t.left, best)
    r = down(t.right, best)

    run = 1
    if t.left is not None and t.left.val == t.val + 1 and l + 1 > run:
        run = l + 1
    if t.right is not None and t.right.val == t.val + 1 and r + 1 > run:
        run = r + 1

    if run > best[0]:
        best[0] = run
    return run


def longest_consecutive(t):
    best = [0]
    down(t, best)
    return best[0]


def report(name, t):
    print(f"{name} {longest_consecutive(t)}")


def main():
    sys.setrecursionlimit(100000)
    report("ascending-right", node(1, None, node(3, leaf(2), node(4, None, leaf(5)))))
    report("descending", node(2, None, node(3, node(2, leaf(1), None), None)))
    report("empty", None)
    report("single", leaf(7))
    report("left-spine", node(1, node(2, node(3, leaf(4), None), None), None))
    report("two-branches", node(5, node(6, leaf(7), None), node(6, None, leaf(7))))
    report("plateau", node(4, node(4, leaf(4), None), None))
    report("crosses-zero", node(-2, node(-1, node(0, leaf(1), None), None), None))


if __name__ == "__main__":
    main()
