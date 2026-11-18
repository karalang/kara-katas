# 2265. Count Nodes Equal to Average of Subtree

Given the `root` of a binary tree, return *the number of nodes where
the value of the node is equal to the **average** of the values in its
**subtree***.

Note:

- The **average** of `n` elements is the **sum** of the `n` elements
  divided by `n` and **rounded down** to the nearest integer.
- A **subtree** of `root` is a tree consisting of `root` and all of its
  descendants.

```
root = [4,8,5,0,1,null,6]  ->  5
root = [1]                 ->  1
```

**Constraints:** The number of nodes in the tree is in the range
`[1, 1000]`; `0 <= Node.val <= 1000`.

A subtree's sum and size come from its two children's, so one
post-order walk has both at every node and counts it on the way back
up. O(n).

## Approaches

| file | mechanism |
|---|---|
| `average.kara` ★ | one post-order walk: `sum_and_size` returns `(sum, size)` and counts a node whose `sum / size` is its value in a `mut ref` counter |
| `average_naive.kara` | node by node: every node's subtree walked again by `total` for its sum and size; O(n^2) on a chain |
| `average_stack.kara` | no recursion: an explicit stack lists the nodes root first, each with its parent's place; read backwards every child comes before its parent, and one pass adds each sum and size into the parent's slot |
| `average_struct.kara` | `struct Tally` of the count; `visit` (`mut ref self`) returns a `struct Part` of sum and size |
| `average_iter.kara` | each call returns `(sum, size, matches)`, the node's own triple a `fold` over its two children mapped from `[n.left, n.right]` |
| `average_solution.kara` | LeetCode's Rust template: `Option<Rc<RefCell<TreeNode>>>` in, `i32` out; a `dfs` nested in the method through `borrow()`, counting into `ans: &mut i32`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

The harness's node is LeetCode's own, `shared struct TreeNode` with an
`i32` value, so the template's sums need no cast. Every arm prints the
same 9 lines: LeetCode's two examples and five more (a leaf under a
smaller root, 2; five equal nodes, 5; a root that is the floor of its
average, 3; a falling chain, 1; three zeros, 3), each with its count;
then 2000 random trees of 1 to 60 nodes of values from 0 to 1, 3, 10 or
1000, with the total and a checksum; then three of the constraints'
largest, 1000 nodes: a random tree of values to 1000 (325), a chain of
left children all 7 (1000), and a chain of right children counting
down from 999 to 0 (1). `average.py` mirrors the ★ arm and its output
is byte-identical.

The stack arm's sums start as the nodes' `i32` values in a `Vec[i64]`;
`collect` does not widen, and `karac fix` writes the `map` as `|t|
(t.val) as i64`. The iter arm's `fold` seed is `(n.val as i64, 1, 0)`.
Written as `(n.val, 1, 0)`, the state takes an `i32` sum from the seed,
and `s + cs` with a child's `i64` sum is refused as a narrowing whose
advice is `as i32`, which would truncate the sum; the seed is not named
and nothing offers to widen it (B-2026-11-18-44).

`karac fix` carries the template in one round, reporting 28 edits: the
two `use` lines deleted, `Option<Rc<RefCell<TreeNode>>>` to
`Option[TreeNode]`, the nested `dfs` moved above the `impl`, `&Option`
to a bare parameter and `&mut i32` to `mut ref i32`, `let n =
n.borrow();` deleted, `&n.left` and `&root` to bare arguments, the
passed-on `ans` and `&mut ans` to `mut ans`, `struct Solution;` to
`struct Solution {}`, and the adapter's `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every node, its subtree's values gathered into a list
by a queue, and the node counted when its value `v` has `v * size <=
sum < (v + 1) * size`, the floor written as bounds. No sums are passed
up. It checks 300 random trees of 1 to 12 nodes of values from 0 to 1,
3, 10 or 1000; then 30 chains of values to 3 or 10; then 30 trees of
one value. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the tree mirrored, every left child made right: the same count |
| P3 | 1000 added to every value: the same count |
| P4 | at least the number of leaves and at most the number of nodes |
| P5 | hung as the left child of a new root of value 0: the count, plus one when the whole sum is below the new size |
| P6 | each arm agrees with at least three of the other five |

P3 holds because adding 1000 to every value adds exactly 1000 to every
average. P5 holds because the new root changes no other subtree, and
its own average, the old sum over the old size plus one, is 0 exactly
when that sum is below the new size.

The differential prints `360 cases: checksum 814972491, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that holds
the tree as lists of children and takes `sum // len` of each
subtree's values. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the right subtree's sum left out | P1 124, P2 126, P3 138, P5 75, P6 124 |
| M3 | ★: the average rounded up | P1 138, P5 92, P6 138 |
| M5 | ★: a match when the value is at most the average | P1 175, P5 252, P6 175 |
| M8 | naive: the right subtree never searched | P1 311, P2 208, P4 236, P6 311 |
| M9 | naive: the size counted twice | P1 150, P3 153, P5 127, P6 150 |
| M10 | naive: the average of the left child's subtree | P1 75, P2 99, P5 19, P6 75 |
| M12 | stack: the right child never stacked | P1 192, P2 211, P5 30, P6 192 |
| M13 | stack: the pass forwards | P1 272, P5 252, P6 272 |
| M15 | stack: every size 2 | P1 303, P3 193, P4 233, P5 64, P6 303 |
| M17 | struct: the left part counted twice | P1 189, P2 219, P5 29, P6 189 |
| M18 | struct: the size one short | P1 161, P2 158, P3 126, P5 57, P6 161 |
| M19 | struct: the count from 1 | P1 360, P4 88, P6 360 |
| M23 | iter: the children's matches dropped | P1 329, P4 298, P5 143, P6 329 |
| M25 | iter: a match by the floor plus one | P1 343, P4 303, P5 108, P6 343 |
| M26 | iter: only the left child | P1 278, P2 151, P4 192, P5 30, P6 278 |
| M29 | solution: the average by the node's value | P1 142, P3 106, P6 142 |
| M30 | solution: the match counted twice | P1 360, P4 190, P5 108, P6 360 |

P1 and P6 kill all seventeen, P5 fourteen, P2 seven, P4 seven, and P3
five. P2 catches the edits that favour one child. P3 catches the edits
whose error grows with the values rather than the shape: a sum or size
off by a part, and the average compared with the value times the
size. P4 catches counts out of range: one too many from the start,
matches counted twice or dropped, a subtree never searched, every size
2, a match by the floor plus one. The three P5
misses, the right subtree never searched, the count from 1 and the
average by the node's value, are each off by the same amount with the
new root as without it.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Ten fail as a kept one does or as one another: the
struct arm's right child's part empty (M21) as the iter arm's only the
left child (M26); the ★ arm's and the template's size without the node
(M2, M28) alike; the ★ arm's left walked twice and the template's left
counted for the right (M4, M27) alike; the naive arm's sum of the
children only and the iter arm's node's value never added (M7, M24)
alike; and the stack arm's sizes not passed up, the struct arm's match
by the sum and the iter arm's children's sizes dropped (M14, M20, M22)
alike, all three leaving every size at 1. Four fail in ways of their
own and are left out because their arms keep enough: the ★ arm's root
never counted (M6), the naive arm's leaf never counted (M11), the
stack arm's parent the grandparent (M16), and the template's value
above the average counted (M31).

Two edits of the first draft were replaced. The iter arm's node's size
0 divided by zero at a leaf, a crash; it is now M22. The naive arm's
leaf never counted matched the iter arm's line too, so its anchor took
the line before it.

## Verification

Every arm prints the same output as `average.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the struct arm takes 0.5 s, the ★ arm and the
template 0.6 s, the stack arm 0.8 s, the differential 1.0 s, the iter
arm 1.1 s, and the naive arm 2.2 s, which walks the 1000-node chains
once per node.

## Benchmarks

The bench builds 500 random trees of the constraints' largest, 1000
nodes of values from 0 to 1000, and counts each 20 times with the ★
arm, in all five languages. Every implementation prints `500 trees of
1000, 20 times: checksum 259693694`. Rust's nodes are LeetCode's
`Rc<RefCell<TreeNode>>`, the model of Kāra's `shared struct`; C's are
one `malloc`'d array linked by pointers, Go's `*TreeNode`, and
Python's objects with `__slots__`.

BENCHTAB
