# 235. Lowest Common Ancestor of a Binary Search Tree

Given a BST and two values `p` and `q` that are present in it, return the value
of their **lowest common ancestor** (LCA) — the deepest node having both `p` and
`q` as descendants, where a node is a descendant of itself.

## Approach

The BST ordering collapses this to a single root-to-split walk — no parent
pointers, no second pass. Starting at the root, at each node:

- both `p` and `q` **less than** the node → the LCA is in the **left** subtree;
- both **greater than** the node → the LCA is in the **right** subtree;
- otherwise the two search paths diverge here (or one value *is* this node), so
  this node is the split point and therefore the LCA.

`O(h)` time, `O(1)` extra space (`h` = tree height).

The tree is an **index pool** (`Vec[Node]` with `i64` `left`/`right`, `-1` =
null), built by BST insertion from a value list — the same shape as
[#230](../230-kth-smallest-element-in-a-bst/).

## Files

- [`lca_bst.kara`](lca_bst.kara) — Kāra implementation.
- [`lca_bst.py`](lca_bst.py) — Python mirror (oracle); same tree, same output.

Expected output (both): `6 2 4 2 8 2 5 4` (one per line).
