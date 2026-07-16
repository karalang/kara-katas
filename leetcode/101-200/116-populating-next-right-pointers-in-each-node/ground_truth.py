#!/usr/bin/env python3
"""Ground-truth check for LeetCode #116 — three independent ways must agree.

For a perfect binary tree, populating each node's `next` pointer can be verified three ways that
must produce the identical wiring:

  1. O(1)-space `connect` — thread each wired level to stitch the level below (`connect.kara`, the ★).
  2. BFS level-order `connect` — a queue per level, link within the level (`connect_bfs.kara`).
  3. Literal invariant — the `next` chain starting at each level's leftmost node must equal that
     level's nodes in BFS left-to-right order, and the rightmost node's `next` must be None.

We check all three agree on a case battery AND 20,000 randomised perfect trees (depth 1..11), by
comparing the full per-level `next`-chain value sequence each method yields. Zero disagreements is
the pass. This is the oracle behind the kata: the Kara solvers' output is trusted only because these
three definitions coincide."""

import random


class Node:
    __slots__ = ("val", "left", "right", "next")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.next = None


def build_perfect(idx, max_idx, base):
    if idx > max_idx:
        return None
    node = Node(idx + base)
    node.left = build_perfect(2 * idx, max_idx, base)
    node.right = build_perfect(2 * idx + 1, max_idx, base)
    return node


def connect_o1(root):
    leftmost = root
    while leftmost is not None and leftmost.left is not None:
        head = leftmost
        while head is not None:
            head.left.next = head.right
            if head.next is not None:
                head.right.next = head.next.left
            head = head.next
        leftmost = leftmost.left


def connect_bfs(root):
    level = [root] if root is not None else []
    while level:
        nxt = []
        for i, node in enumerate(level):
            node.next = level[i + 1] if i + 1 < len(level) else None
            if node.left is not None:
                nxt.append(node.left)
            if node.right is not None:
                nxt.append(node.right)
        level = nxt


def chains_via_next(root):
    """The per-level value sequences produced by following `next` from each level's leftmost node.
    Descends via .left to reach each level head. Returns list-of-lists."""
    out = []
    leftmost = root
    while leftmost is not None:
        row = []
        cur = leftmost
        while cur is not None:
            row.append(cur.val)
            cur = cur.next
        out.append(row)
        leftmost = leftmost.left
    return out


def bfs_levels(root):
    """The literal invariant: BFS level-order grouping (independent of `next`)."""
    out = []
    level = [root] if root is not None else []
    while level:
        out.append([n.val for n in level])
        nxt = []
        for n in level:
            if n.left is not None:
                nxt.append(n.left)
            if n.right is not None:
                nxt.append(n.right)
        level = nxt
    return out


def check(max_idx, base):
    # Method 1
    r1 = build_perfect(1, max_idx, base)
    connect_o1(r1)
    c1 = chains_via_next(r1)
    # Method 2
    r2 = build_perfect(1, max_idx, base)
    connect_bfs(r2)
    c2 = chains_via_next(r2)
    # Method 3: literal BFS level grouping (the target wiring)
    r3 = build_perfect(1, max_idx, base)
    c3 = bfs_levels(r3)
    return c1 == c2 == c3


def main():
    battery = [(0, 0), (1, 0), (3, 0), (7, 5), (15, 100), (31, -3), (63, 7), (127, 1), (255, 2)]
    fails = 0
    for max_idx, base in battery:
        if not check(max_idx, base):
            fails += 1
            print(f"BATTERY FAIL: max_idx={max_idx} base={base}")

    rng = random.Random(116116)
    for _ in range(20000):
        depth = rng.randint(1, 11)
        max_idx = (1 << depth) - 1
        base = rng.randint(-50, 50)
        if not check(max_idx, base):
            fails += 1
            if fails <= 5:
                print(f"FUZZ FAIL: depth={depth} max_idx={max_idx} base={base}")

    if fails == 0:
        print("ground truth OK: O(1) == BFS == literal level-order (battery + 20000 fuzz, 0 disagreements)")
    else:
        print(f"GROUND TRUTH FAILED: {fails} disagreements")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
