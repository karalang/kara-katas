# 1302. Deepest Leaves Sum

Given the `root` of a binary tree, return the sum of values of its
deepest leaves.

```
root = [1,2,3,4,5,null,6,7,null,null,null,null,8]  ->  15
root = [6,7,8,2,7,1,3,9,null,1,4,null,null,null,5] ->  19
```

**Constraints:** the number of nodes is in `[1, 10^4]`, and `1 <=
Node.val <= 100`.

The arms are `fn deepest_leaves_sum(root: Option[TreeNode]) -> i32`, over
`shared struct TreeNode { mut val: i32, mut left: Option[TreeNode], mut
right: Option[TreeNode] }`.

## Approaches

Every node on the deepest level is a leaf, since a child would be deeper
still, so the answer is the sum of the last level.

| file | mechanism |
|---|---|
| `deepest_leaves_sum.kara` ★ | a breadth-first walk a level at a time from a `VecDeque`, each level's values summed afresh, so the sum left when the queue runs out is the last level's. O(n) |
| `deepest_leaves_sum_dfs.kara` | one recursive walk carrying each node's depth, with the deepest depth met so far and the sum of the values met there; a deeper node starts the sum over. O(n), as deep as the tree |
| `deepest_leaves_sum_twopass.kara` | the tree's height first, by recursion on the taller child, then a second walk summing the values found at that depth. O(n), as deep as the tree |
| `deepest_leaves_sum_stack.kara` | the depth-first walk without recursion, a `Vec` of (node, depth) pairs used as a stack, the deepest depth and its sum kept as each pair comes off. O(n) |
| `deepest_leaves_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `VecDeque<Rc<RefCell<TreeNode>>>` emptied a level at a time, `let node = node.borrow();`, the children pushed through `node.left.clone()`), carried to Kāra by `karac fix` |
| `deepest_leaves_sum_recursive.kara` | a second Rust solution as LeetCode's Rust users write it (a `fn dfs(node: &Option<Rc<RefCell<TreeNode>>>, depth: i32, max_depth: &mut i32, sum: &mut i32)` nested inside the method, the node read through `n.borrow()`, the sum taken only at leaves), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, one node, a
chain of `10^4` nodes each the right child of the one before, and a full
tree of `2^13 - 1` nodes (`15 19 42 1 206676`); then 2000 random trees of
1 to 300 nodes, each node hung on a random empty place (`2000 random
trees: sums total 189479, checksum 163959775`). `deepest_leaves_sum.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run` and `karac
__mir-llvm-run`, the chain taking the recursive arms `10^4` calls deep.

The Mend loop: the ★ arm's `let mut sum = 0`, added to with an `i32` and
returned as one, is refused, and `karac fix` writes `let mut sum: i32 =
0` (1 fix); the other three Kāra arms checked clean as first written.
The first Rust arm takes one round of 15 fixes by `karac fix`'s count,
from 8 errors: its three `use` lines deleted, `struct Solution;` to
`struct Solution {}`, `Option<Rc<RefCell<TreeNode>>>` to
`Option[TreeNode]`, `VecDeque::new()` to `VecDeque.new()`, `let mut sum
= 0` to `let mut sum: i32 = 0`, `!` to `not`, `let node =
node.borrow();` dropped, since a `shared struct`'s fields read directly,
and `::` to `.`. The second takes one round of 32 fixes from 16 errors:
the same rewrites, the nested `fn dfs` moved out of the method to the top
level, `&Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`, `&mut i32`
to `mut ref i32`, `let n = n.borrow();` dropped, `&&` to `and`, and the
calls' `&n.left` to `n.left` and `&mut max_depth` to `mut max_depth`.
Both outputs match on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every path from the root down to a leaf written out as its
list of values, and the last values of the longest lists summed. 2000
trees of 1 to 16 nodes in four kinds, 500 each: each node hung on a
random empty place; a chain, each node a child of the one before on a
random side, now and then with a second child; filled level by level
with gaps; and random hanging with values from 1 to 3. Every tree, place
and leaf is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the tree mirrored: the same answer |
| P3 | every value doubled: the answer doubled |
| P4 | one leaf hung on an empty place: the leaf alone if it is deeper than the tree, the answer plus the leaf if it is as deep, the same answer otherwise |
| P5 | two copies of the tree under a new root: the answer doubled |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 trees: checksum 451820739,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Thirteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. One is left out: the first Rust
arm summing only the last node of each level fails exactly as the
depth-first arm starting the sum again at a tie (M3) does, since both
keep the last deepest node alone. The twelve kept, two to each arm, are
each killed, fail the same way under both backends and not by a crash,
and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the sum never reset for a new level | P1 1846, P4 2000, P5 2000, P6 9230 |
| M2 | ★: no right child queued | P1 1543, P2 1662, P4 1646, P5 2000, P6 7715 |
| M3 | depth first: a tie starting the sum again | P1 696, P2 641, P4 736, P5 2000, P6 696 |
| M4 | depth first: the right child kept at its parent's depth | P1 1355, P2 1771, P4 1309, P5 2000, P6 1355 |
| M5 | two passes: the height by the shorter side | P1 1709, P4 1894, P6 1709 |
| M6 | two passes: the level above the deepest summed | P1 1902, P4 1978, P5 154, P6 1902 |
| M7 | stack: the sum never reset at a deeper node | P1 1846, P2 1424, P4 2000, P5 1967, P6 1846 |
| M8 | stack: the left child pushed at its parent's depth | P1 1410, P2 1771, P4 1792, P5 2000, P6 1410 |
| M9 | solution: a left child queued twice | P1 1722, P2 1657, P4 1974, P5 2000, P6 1722 |
| M10 | solution: each node counted as 1 | P1 1861, P3 2000, P4 1933, P6 1861 |
| M11 | recursive: a deeper leaf added, not starting the sum | P1 800, P2 1270, P4 1040, P5 800, P6 800 |
| M12 | recursive: the right child two levels down | P1 842, P2 949, P4 985, P5 2000, P6 842 |

P1, P4 and P6 kill all twelve, P5 ten, P2 eight and P3 one. A leaf hung
on an empty place (P4) moves the answer in one of three ways the depths
decide, and every edit misreads at least one of them. Two copies under a
new root (P5) double a wrong answer as well as a right one when the
wrong answer is itself a sum over levels: the shorter side's height (M5)
and the count of nodes (M10) double, and the level above the deepest
(M6) does too, except on a tree of one node, where it is empty and the
new root is not. Mirroring the tree (P2) passes the edits that treat
both children and every deepest node alike (M1, M5, M6, M10), and fails
the ones that treat one side differently (M2, M4, M8, M9, M12) or depend
on which deepest node is met first (M3, M7, M11). Doubling every value
(P3) doubles any sum of values, right or wrong, and so sees only M10,
which counts nodes instead.

## Benchmarks

The bench builds 50 trees of `10^4` nodes, the constraints' most, with
values from 1 to 100, once from its own generator: half with each node
hung on a random empty place, half filled level by level with gaps; then
makes 50 passes, each setting one node of every tree from the checksum
so far, so no answer carries over, answering it with the ★ arm and
folding the sum plus the pass into the checksum. The nodes are `shared
struct`s in Kāra and LeetCode's own `Rc<RefCell<TreeNode>>` in Rust. The
queue is `VecDeque` in Kāra and Rust and `collections.deque` in Python;
Go reads a slice from a moving head, and C an array of n, since each
node is queued once. Every implementation prints `50 passes over 50
trees of 10^4: checksum 871374528`.

BENCHTAB
