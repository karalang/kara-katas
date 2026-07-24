# 236. Lowest Common Ancestor of a Binary Tree

Given a binary tree and two present values `p` and `q`, return the value of their
**lowest common ancestor** — the deepest node having both as descendants (a node
is a descendant of itself).

## Approach

Unlike [#235](../235-lowest-common-ancestor-of-a-bst/) there is **no BST order**
to steer the search, so each node must inspect *both* subtrees. Classic recursive
post-order — each node reports what it found beneath it:

- an empty subtree, or a node that **is** `p` or `q`, reports itself upward;
- a node that gets a non-null answer from **both** children is the split point →
  it is the LCA;
- a node with only one non-null child answer forwards that answer up.

The first node to see the two targets arrive from different subtrees (or to be
one target with the other beneath it) is the LCA. `O(n)` time, `O(h)` stack.

The tree is an **index pool** (`Vec[Node]`, `i64` `left`/`right`, `-1` = null),
built from explicit `(val, left, right)` parallel arrays so *any* shape — not
just a BST — can be described.

## Files

- [`lca_binary_tree.kara`](lca_binary_tree.kara) — Kāra implementation.
- [`lca_binary_tree.py`](lca_binary_tree.py) — Python mirror (oracle).

Expected output (both): `3 5 5 2 3 3 1` (one per line).
