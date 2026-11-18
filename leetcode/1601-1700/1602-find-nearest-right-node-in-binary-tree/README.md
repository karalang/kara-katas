# 1602. Find Nearest Right Node in Binary Tree

Given the `root` of a binary tree and a node `u` in the tree, return
*the **nearest** node on the **same level** that is to the **right** of*
`u`*, or return* `null` *if* `u` *is the rightmost node in its level*.

```
root = [1,2,3,null,4,5,6], u = 4  ->  5
root = [3,null,4,2],       u = 2  ->  null
```

**Constraints:** the number of nodes in the tree is in `[1, 10^5]`;
`1 <= Node.val <= 10^5`; all values in the tree are **distinct**; `u` is
a node in the binary tree rooted at `root`.

## Approaches

`u` is the node itself, so each arm finds it by identity, with
`ref_eq`, the identity test every `shared` handle has (design.md §
Equality), not by its value.

| file | mechanism |
|---|---|
| `nearest_right.kara` ★ | breadth first a level at a time over a `VecDeque[TreeNode]`: the queue holds exactly one level as a level starts, so the node taken after `u` in its level is the answer, and `u` taken last has none. O(n) time, O(width) space |
| `nearest_right_dfs.kara` | a preorder walk visits each level left to right, so the next node met at `u`'s depth is the answer; the depth (`Option[i64]`), the answer and a stop flag in a struct passed down by `mut ref`, matched with guards (`Some(d) if d == depth`). O(n) time, O(h) stack |
| `nearest_right_levels.kara` | one recursive walk files every node under its depth in a `Vec[Vec[TreeNode]]`, then `u`'s level is searched with `position` and `get(i + 1).cloned()` taken. O(n) time and space |
| `nearest_right_solution.kara` | LeetCode's Rust template (`Option<Rc<RefCell<TreeNode>>>` for `root` and `u`, `u.unwrap()`, a `VecDeque` drained a level at a time, `Rc::ptr_eq(&node, &u)`, `node.borrow().left.clone()`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one node, a cousin far to the right, the last node of a full level, and
a chain), then the answers found and a checksum for 3000 trees of up to 8
nodes asked 5 nodes each, 300 of up to 1000 asked 20, and 3 of up to
100000 asked 20. Each tree holds 1 to `n` in a random order, each node
hung on a random free child slot of the nodes before it. `nearest_right.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every node's level is its depth, and one node lies to the
right of another on a level when its path from the root, written left 0
and right 1, is the larger string; the nearest is the one with the
smallest such path. It checks 3000 trees of 1 to 8 nodes, each asked one
random node, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | in the mirrored tree the answer's own answer is `u` (checked when there is an answer) |
| P3 | the values relabelled (`v` made `n + 1 - v`) leave the answer, relabelled |
| P4 | a child hung below the deepest node leaves the answer |
| P5 | the tree put under a new root as its left child leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 606098002, 62436 checks
over 4 arms: 0 failures` under every lane in Verification: P2 is checked
only where `u` has a node to its right, so there are fewer than 72000.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M9, the template's level loop started at 1, sent each level's
count out of step with the queue and hung; it was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `u` last in its level answered with the next level's first | P1 250, P2 250, P4 62, P6 250 |
| M2 | ★: a level of more than three nodes cut at three | P1 9, P2 4, P6 9 |
| M3 | dfs: the next node at `u`'s depth or above taken | P1 323, P2 323, P6 323 |
| M4 | dfs: the right subtree walked first | P1 1109, P6 1109 |
| M5 | dfs: the walk not stopped at the answer | P1 57, P2 52, P6 57 |
| M6 | levels: the level's last node taken | P1 2448, P2 552, P6 2448 |
| M7 | levels: right children filed first | P1 1109, P6 1109 |
| M8 | template: the queue's back taken for the answer | P1 67, P2 52, P4 2, P6 67 |
| M9 | template: `u` next to last in its level answered with none | P1 552, P2 53, P6 552 |
| M10 | ★: right children never queued | P1 609, P6 609 |

## Benchmarks

The bench makes 10 random trees of 100000 nodes, 100 nodes of each asked for, all of it first. Then: breadth first a level at a time, nodes counted by reference. Every implementation prints `10 trees of 100000 nodes: 1000 queries, 1000 found, checksum 190630735`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.738 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.784 s |
| Kāra (`karac build`) | 0.839 s |
| Rust (`rustc -O`) | 0.889 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.900 s |
| Go | 2.307 s |
| Python | 9.5 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (0.726 s and 0.766 s on one run).

## Verification

All four arms print the same output as `nearest_right.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5bb1708545`.

## Writing it

The three Kāra arms were written in Kāra and checked as written. The
shared harness wrote `from_level_order(items, *u)` on the `i32` a tuple
pattern binds by value, and `n.val as i64` where the cast widens anyway;
`karac check` named both, and they were edited by hand to what `karac
fix` writes. The differential wrote `*d == depth` on a copied `i64`, a
`match best` that moved the `Option` out inside a loop, and `n + 1`
passed for an `i32`; `karac check` named each and they were edited by
hand: `d`, `Some((ref q, _))`, and one `top = (n + 1) as i32`.

The Rust template took one `karac fix` of 30 edits: the three `use`
lines dropped, `struct Solution;` to `struct Solution {}`,
`Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`, `::new` to
`.new`, `!` to `not`, `Rc::ptr_eq(&node, &u)` to `node.ref_eq(u)`, the
`let node = node.borrow();` dropped, and `Solution::` to `Solution.`. It
then checks and agrees with no hand edit. Before B-2026-11-18-5 the rewrite of
`Rc<RefCell<T>>` left `Rc.ptr_eq(node, u)` behind, refused with no fix
and no word of `ref_eq`.
