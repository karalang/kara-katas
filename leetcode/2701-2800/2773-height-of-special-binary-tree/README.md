# 2773. Height of Special Binary Tree

*A premium problem.*

You are given a `root`, which is the root of a **special** binary tree
with `n` nodes. The nodes of the special binary tree are numbered from
`1` to `n`. Suppose the tree has `k` leaves in the following order:
`b1 < b2 < ... < bk`.

The leaves of this tree have a **special** property! That is, for every
leaf `bi`, the following conditions hold:

- The right child of `bi` is `b(i + 1)` if `i < k`, and `b1` otherwise.
- The left child of `bi` is `b(i - 1)` if `i > 1`, and `bk` otherwise.

Return *the height of the given tree.*

**Note:** The height of a binary tree is the length of the **longest
path** from the root to any other node.

```
root = [1, 2, 3, null, null, 4, 5]           ->  2
root = [1, 2]                                ->  1
root = [1, 2, 3, null, null, 4, null, 5, 6]  ->  3
```

**Constraints:** `n == number of nodes in the tree`, `2 <= n <= 10^4`,
`1 <= node.val <= n`, the input is generated such that each `node.val`
is unique.

## Approaches

A link from a node is a real child unless it points straight back: a
leaf's left neighbour has the leaf as its right, and its right neighbour
has it as its left, while no real child links back to its parent. That
holds for a ring of one leaf joined to itself, or of two, as well.

The arms take the tree as two arrays of child indices, -1 for none, the
ring already in them; the harness joins the leaves left to right.

| file | mechanism |
|---|---|
| `height.kara` ★ | the height by recursion over the real children, each link followed unless the child links straight back. O(n), recursing as deep as the tree |
| `height_levels.kara` | a breadth-first walk from the root over a `VecDeque`, a level at a time, each node passing on only its real children; the height is the levels less one. O(n) |
| `height_weak.kara` | the tree as `shared` nodes whose child fields are `weak`, the strong handles all kept in one `Vec`, so the ring is no cycle of strong handles; a child read is an `Option`, and its other side compared with the parent by `ref_eq`. O(n), recursing as deep as the tree |
| `height_parents.kara` | no walk from the root: every node's parent found from the real links, then each node's depth by climbing its parents, remembered in a `Vec[Option[i64]]` so no chain is climbed twice. O(n) |
| `height_solution.kara` | a Rust solution as LeetCode's Rust users write it, `Option<Rc<RefCell<TreeNode>>>` in, a nested `dfs` over `borrow()` of each node, a child skipped when its other side is the node itself by `Rc::ptr_eq`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

LeetCode's own tree holds the ring in strong handles, a cycle that Kāra,
with no cycle collector, never frees: the solution arm's adapter builds
that tree of `shared struct TreeNode`s from the arrays and clears every
link after the call. Without the clearing, `karac __mir-llvm-asan`
reports the nodes leaked.

Every arm prints the same 7 lines: LeetCode's three examples; `10^4`
nodes, LeetCode's most, as a chain of left children with one leaf
joined to itself, and as a complete tree of 8191 under a chain; 3000
random trees of 2 to 20 nodes; and 20 of `10^4`, each new node hung on
one of the last few with a free side, the last two with the sum of the
heights and a checksum. `height.py` mirrors the ★ arm and its output is
byte-identical.

```
2
1
3
9999
1821
3000 small trees: heights sum to 15227, checksum 414605956
20 trees of 10^4: heights sum to 2387, checksum 697691553
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the tree as it was grown, before its leaves were joined into
a ring, and its height by the recursive definition, the longest path
down from the root; no ring to see through. It draws 2000 random trees
of 2 to 20 nodes, then 60 of up to 3000, all before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the nodes numbered backwards: the same answer |
| P3 | the tree mirrored, left and right swapped throughout: the same answer |
| P4 | a new root above the old one: one more |
| P5 | from the least height of n nodes, ceil(log2(n + 1)) - 1, to n - 1 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2060 cases: checksum 310721158, 61800 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same trees by the same recursion gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1 and M10 make the same edit, a step to a
right child not counted, in the ★ arm and the solution, and fail the
same checks; M3 and M7 both answer one more than the height.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a step to a right child not counted | P1 1788, P3 1554, P5 664, P6 1788 |
| M2 | ★: the left subtree's height dropped | P1 1799, P3 1685, P4 2060, P5 1430, P6 1799 |
| M3 | levels: the levels counted for the height | P1 2060, P5 377, P6 2060 |
| M4 | levels: every node taken as a level of its own | P1 1683, P6 1683 |
| M5 | weak: a right child never followed | P1 1788, P3 1685, P5 1400, P6 1788 |
| M6 | weak: a step to a left child not counted | P1 1799, P3 1554, P4 2060, P5 673, P6 1799 |
| M7 | parents: the root put at depth 1 | P1 2060, P5 377, P6 2060 |
| M8 | parents: each step down counted twice | P1 2060, P4 2060, P5 942, P6 2060 |
| M9 | solution: a left child with no right taken as pointing back | P1 725, P3 1127, P4 317, P5 269, P6 725 |
| M10 | solution: a step to a right child not counted | P1 1788, P3 1554, P5 664, P6 1788 |

## Benchmarks

The bench draws 20 random trees of `10^4` nodes, LeetCode's most, each
grown by hanging every new node on one of the last 1 to 50 with a free
side and its leaves joined into a ring, all of them first, then answers
each 200 times by the ★ arm in all five languages, every one by
recursion over two arrays of child indices. Every implementation prints
`20 trees of 10^4, 200 rounds: heights sum to 2485000, checksum
578954623`.

BENCHTAB

## Verification

All five arms print the same output as `height.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 29 `karac fix` edits, the wrapper
included: the `use std::rc::Rc` and `use std::cell::RefCell` lines went,
and with them every `Rc<RefCell<TreeNode>>` became `TreeNode`, a
`shared struct` already; `Option<..>` became `Option[..]`; the nested
`dfs` moved out to the top level, its `&` parameter dropped; the
`.borrow()`s went; `&n.left` became `ref n.left`; `Rc::ptr_eq(r, node)`
became `r.ref_eq(node)`; `!back` became `not back`; `let mut best = 0`
gained its type, `: i32`; `struct Solution {}` was added; and
`Solution::` became `Solution.`. The `Rc::ptr_eq` diagnostic on its own
reads `Rc.ptr_eq`, but the rewrite that removes `Rc` writes `ref_eq`.
