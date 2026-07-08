# 98. Validate Binary Search Tree

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Binary Search Tree · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/validate-binary-search-tree](https://leetcode.com/problems/validate-binary-search-tree/)

Decide whether a binary tree is a valid **binary search tree**: for *every* node, its value must be strictly greater than **all** values in its left subtree and strictly less than **all** values in its right subtree.

```
    2               5                  5
   / \             / \                / \
  1   3   ✓       1   4     ✗        4   6      ✗
                     / \                / \
                    3   6              3   7
  valid BST     4's left child 3    3 is in 5's right subtree
                is < 5 (its         yet 3 < 5 — a distant
                grandparent)        ancestor violation
```

**Constraints:** `1 ≤ nodes ≤ 10⁴`; `−2³¹ ≤ Node.val ≤ 2³¹ − 1`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Recursive (lo, hi) bounds** ★ — a node must lie in the open interval inherited from its ancestors | O(n) time, O(h) stack | [`validate_bst.kara`](validate_bst.kara) ✓ via `karac run` / `karac build` | [`validate_bst.py`](validate_bst.py) ✓ |
| **Inorder is sorted** — collect the inorder traversal, check it strictly increases | O(n) time, O(n) space | [`validate_bst_inorder.kara`](validate_bst_inorder.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all ten test trees, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## The trap: local rule ≠ BST

The mistake the problem is built to catch is checking only `left < node < right` at each node. That misses a value that is a valid immediate child but violates the invariant against a *distant* ancestor — `[5,4,6,null,null,3,7]`: the `3` is the left child of `6` (so `3 < 6`, locally fine) but it sits in `5`'s **right** subtree, where everything must exceed `5`. A correct check carries the full legal range, not just the parent.

**Recursive (lo, hi) bounds** ([`validate_bst.kara`](validate_bst.kara)) is the ★. Thread an open interval `(lo, hi)` down the tree: the value must land strictly inside it, the **left** child inherits `(lo, node.val)`, the **right** child inherits `(node.val, hi)`. The bounds are `Option[i64]` with `None` meaning "unbounded on that side," and the root starts `(None, None)` — so there is no sentinel `i64::MIN`/`MAX` that a legitimate node value (which can span the full i32 range) might equal. A node outside its interval short-circuits the whole tree to `false` via `and`.

**Inorder is sorted** ([`validate_bst_inorder.kara`](validate_bst_inorder.kara)) uses the defining property directly: an inorder walk (left, node, right) of a BST emits values in strictly increasing order. Collect the traversal into a `Vec[i64]` and verify every adjacent pair increases. It trades O(n) space for the most literal statement of the property, and cross-checks the ★.

## Kāra features exercised

- **`shared struct TreeNode` (RC) with `Option[TreeNode]` children** — the recursive reference type `shared struct TreeNode { val: i64, mut left: Option[TreeNode], mut right: Option[TreeNode] }`, and nested `Some(TreeNode { … })` construction (with a `leaf` helper), the tree idiom shared with kata [#226](../../201-300/226-invert-binary-tree/).
- **`match` on the node and on each `Option[i64]` bound** — `match node { None => …, Some(n) => … }` drives the recursion, and the ★ matches each bound (`match lo { Some(l) => …, None => {} }`) to apply it only when present; a mid-arm `return false` short-circuits.
- **Recursion carrying accumulators two different ways** — the ★ threads by-value `Option[i64]` bounds *down* and returns a `bool` (with short-circuiting `and`); the inorder solver threads a **`mut ref Vec[i64]`** accumulator *through* the recursion, forwarding the existing mutable borrow to the child calls without a call-site marker (`inorder(n.left, out)`) and marking only the fresh owned binding at the top (`inorder(root, mut vals)`). Two distinct codegen shapes over the same `shared struct`.
- **Bool-folding `report` harness** — one `valid=true`/`valid=false` per tree plus a `sums:` fold of `1`/`0`, the byte-for-byte diff anchor; both solvers and the Python mirror print it identically.

**v1 note.** Node values are i64 (the problem's i32 range fits with room to spare); no arithmetic here can overflow — the only operations are comparisons. Using `Option[i64]` bounds rather than sentinels means the validator is correct even for a node whose value equals `i64`'s extremes. Both solvers verified byte-identical under `karac run` and `karac build`, including the default auto-parallelizing build and `KARAC_AUTO_PAR=0` — the recursive `shared struct` traversal lowers consistently across all three surfaces.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   validate_bst.kara
karac build validate_bst.kara && ./validate_bst

# The inorder approach (identical output):
karac run validate_bst_inorder.kara

# Python
python3 validate_bst.py

# Verify they all agree
diff <(karac run validate_bst.kara) <(python3 validate_bst.py)             && echo OK
diff <(karac run validate_bst.kara) <(karac run validate_bst_inorder.kara) && echo OK
```
