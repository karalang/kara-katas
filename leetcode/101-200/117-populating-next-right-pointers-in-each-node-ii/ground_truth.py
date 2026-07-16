#!/usr/bin/env python3
"""Ground-truth check for LeetCode #117 — three independent ways must agree.

For an ARBITRARY binary tree, populating each node's `next` pointer can be verified three ways that
must produce the identical wiring:

  1. O(1)-space `connect` — dummy-head + tail builds each next level's chain (`connect.kara`, the ★).
  2. BFS level-order `connect` — a queue per level, link within the level (`connect_bfs.kara`).
  3. Literal invariant — the `next` chain reachable at each level must equal that level's nodes in
     BFS left-to-right order, and the rightmost node's `next` must be None.

We compare the full per-level `next`-chain value sequence each method yields, on a case battery AND
20,000 randomised trees of varied shape (random BSTs of random size 0..80). Zero disagreements is the
pass — this is the oracle the Kara solvers are trusted against."""

import random


class Node:
    __slots__ = ("val", "left", "right", "next")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.next = None


def insert(root, v):
    if root is None:
        return Node(v)
    if v < root.val:
        root.left = insert(root.left, v)
    else:
        root.right = insert(root.right, v)
    return root


def build(vals):
    root = None
    for v in vals:
        root = insert(root, v)
    return root


def connect_o1(root):
    leftmost = root
    while leftmost is not None:
        dummy = Node(0)
        tail = dummy
        cur = leftmost
        while cur is not None:
            if cur.left is not None:
                tail.next = cur.left
                tail = cur.left
            if cur.right is not None:
                tail.next = cur.right
                tail = cur.right
            cur = cur.next
        leftmost = dummy.next


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
    """Per-level value sequences following `next` from each level's head. The level head is found by
    scanning the current level via `next` for the first child (left or right)."""
    out = []
    head = root
    while head is not None:
        row = []
        cur = head
        while cur is not None:
            row.append(cur.val)
            cur = cur.next
        out.append(row)
        nh = None
        scan = head
        while scan is not None:
            if scan.left is not None:
                nh = scan.left
                break
            if scan.right is not None:
                nh = scan.right
                break
            scan = scan.next
        head = nh
    return out


def bfs_levels(root):
    """Literal invariant: BFS level-order grouping (independent of `next`)."""
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


def check(vals):
    r1 = build(vals)
    connect_o1(r1)
    c1 = chains_via_next(r1)
    r2 = build(vals)
    connect_bfs(r2)
    c2 = chains_via_next(r2)
    r3 = build(vals)
    c3 = bfs_levels(r3)
    return c1 == c2 == c3


def main():
    battery = [
        [],
        [5],
        [5, 3, 8],
        [1, 2, 3, 4, 5, 6, 7],  # right-skewed via sorted insert
        [50, 25, 75, 10, 30, 60, 90, 5],
        [10, 5, 15, 3, 7, 12, 18, 1, 4, 6, 8],
    ]
    fails = 0
    for vals in battery:
        if not check(vals):
            fails += 1
            print(f"BATTERY FAIL: {vals}")

    rng = random.Random(117117)
    for _ in range(20000):
        n = rng.randint(0, 80)
        vals = [rng.randint(0, 200) for _ in range(n)]
        if not check(vals):
            fails += 1
            if fails <= 5:
                print(f"FUZZ FAIL: n={n} vals={vals}")

    if fails == 0:
        print("ground truth OK: O(1) == BFS == literal level-order (battery + 20000 fuzz, 0 disagreements)")
    else:
        print(f"GROUND TRUTH FAILED: {fails} disagreements")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
