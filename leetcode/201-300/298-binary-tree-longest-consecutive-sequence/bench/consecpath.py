"""LeetCode 298 benchmark lane - Python mirror of consecpath.kara.

Same tree, same passes, same sink: build one perfect depth-20 tree, then 40
full traversals with steps 1..40. See the .kara file's header for the workload
rationale.
"""

import sys


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def build(depth, parent_val, state):
    if depth <= 0:
        return None
    state[0] = (state[0] * 1103515245 + 12345) & 0x7FFFFFFF
    v = parent_val + state[0] % 3 - 1
    l = build(depth - 1, v, state)
    r = build(depth - 1, v, state)
    return Node(v, l, r)


def down(t, step, best):
    if t is None:
        return 0
    l = down(t.left, step, best)
    r = down(t.right, step, best)
    run = 1
    if t.left is not None and t.left.val == t.val + step and l + 1 > run:
        run = l + 1
    if t.right is not None and t.right.val == t.val + step and r + 1 > run:
        run = r + 1
    if run > best[0]:
        best[0] = run
    return run


def longest_with_step(t, step):
    best = [0]
    down(t, step, best)
    return best[0]


def main():
    sys.setrecursionlimit(100000)
    depth = 20
    passes = 40

    tree = build(depth, 0, [12345])

    checksum = 0
    for d in range(1, passes + 1):
        checksum = (checksum * 31 + longest_with_step(tree, d)) % 1000000007

    print(f"depth {depth} passes {passes} checksum {checksum}")


if __name__ == "__main__":
    main()
