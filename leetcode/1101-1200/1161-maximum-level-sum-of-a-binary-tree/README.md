# 1161. Maximum Level Sum of a Binary Tree

Given the `root` of a binary tree, the level of its root is 1, the level
of its children is 2, and so on.

Return the smallest level `x` such that the sum of all the values of
nodes at level `x` is maximal.

```
root = [1,7,0,7,-8,null,null]                          ->  2
root = [989,null,10250,98693,-89388,null,null,null,-32127]  ->  2
```

**Constraints:** the number of nodes is in `[1, 10^4]`; `-10^5 <=
Node.val <= 10^5`.

The arms are `fn max_level_sum(root: Option[TreeNode]) -> i64`, over a
`shared struct TreeNode` with an `i32` value and `Option[TreeNode]`
children.

## Approaches

Every level's sum is needed, so every arm visits each node once; they
differ in how a node's level is known and in how a tie between levels
goes to the smaller one.

| file | mechanism |
|---|---|
| `max_level_sum.kara` ★ | level by level: the nodes of one level in a `Vec`, summed while the next level's are gathered; a level takes the lead only with a strictly larger sum, so the smallest of tied levels is kept. O(n) |
| `max_level_sum_dfs.kara` | depth first: a recursive walk adds each node into its depth's sum, the `Vec` of sums growing as deeper levels are met; the answer is the first `position` of the largest. O(n) |
| `max_level_sum_counted.kara` | one queue: every node in a single `Vec` read from a moving head, each level the nodes queued when it began; the sums go into a `SortedMap` from level to sum, read back for the first entry holding the largest. O(n log h) |
| `max_level_sum_stack.kara` | an explicit stack of `(node, depth)` pairs, right child pushed before left, the sums kept by depth in a `Map`; the deepest level is the map's size, so the levels are read back in order from 1. O(n) |
| `max_level_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `Option<Rc<RefCell<TreeNode>>>`, a `VecDeque` drained a level at a time by its length, `node.borrow()`, `i32` sums and levels from `i32::MIN`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's examples (2, 2); one node
(1); every level negative, the root's the largest (`[-1,-2,-3]`: 1); two
levels tied (`[1,1,0]`: 1); all zero (1); a deeper level less negative
than the root (`[-5,-1,-1]`: 2); a chain whose last level wins
(`[1,2,null,3,null,4,null,5]`: 5). Then 1000 random trees of 1 to 1000
nodes, a quarter grown deep and half with values from -2 to 2 so that
levels tie (`1000 random trees: levels 12307, checksum 173056104`), and
two trees of 10^4 nodes over the whole range, the constraints' most, one
wide (level 1) and one grown deep (level 77). `max_level_sum.py` mirrors
the ★ arm and its output is byte-identical; a Python reading that finds
each node's level by walking up its parents gives the same output.

The Mend loop: the four Kāra arms take one fix each, the same one: `sum
+= node.val as i64` loses its `as i64`, since an `i32` widens to the
`i64` sum without it. The Rust arm takes four rounds (20, 4, 1 and 4
edits): the generics to brackets, `::` to `.`, the tuple of `let mut`
bindings to `let mut (ans, best, level)`, `!` to `not`, and the `use`
lines for `VecDeque` and `Rc` deleted; then `Option<Rc<RefCell<TreeNode>>>`
reduced to `Option[TreeNode]`, the shared struct, with `node.borrow()`
and the `RefCell` line gone; then `struct Solution {}`; then the
literals typed `1i32` and `0i32`, the sum annotated `i32`, and the
adapter's `as i64` dropped. The `VecDeque`, its `push_back` and
`pop_front`, and the `clone()` of each child are kept. Its output
matches on the first run.

Writing this arm found a gap in the Mend loop: each `use` line took a
fix round of its own, so the arm took seven rounds, because after one
`use` line's diagnostic the parser's recovery skipped to the next `fn`,
past the other `use` lines. That is kara B-2026-11-15-17, fixed at
`f5f9065de8`.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each node's level found by walking up its parents to the
root, each level's sum from those, and the smallest level whose sum no
level beats. A tree is plain data (each node's value and its children's
indices), and every arm call builds its own linked tree from it, so no
arm sees another's. It checks 1200 trees in four kinds of 300: 1 to 12
nodes with values from -2 to 2; 1 to 300 nodes over the whole range,
half of them grown deep; a chain-like tree of 1 to 200 nodes from -2 to
2; and a full tree of 1 to 7 levels whose nodes share one value per
level, from -2 to 2, so that whole levels tie. Every random choice the
properties make is drawn before any arm answers.

| | property |
|---|---|
| P1 | the level is the literal one |
| P2 | the tree mirrored (children swapped at every node) gives the same level |
| P3 | a new root above, of a drawn value, gives the old level plus one when some level sums above that value, and 1 otherwise |
| P4 | a node of the winning level raised by one keeps the level |
| P5 | a leaf hung below the deepest level wins exactly when its value beats the best sum |
| P6 | the tree twice under a new root, every level's sum doubled, gives the old level plus one when twice the best sum beats the root, and 1 otherwise |

All 36,000 checks pass on every arm: `1200 trees: checksum 100010064,
36000 checks over 5 arms: 0 failures`, in 11.5 s under `karac
__mir-run`. A Python reading of the same draws, with the mirror against
the parent-walk reading, gives the same checksum.

## Mutation testing

Seventeen edits to the differential, three or four to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run` with
`KARAC_HASH_SEED=1`, each failing the same way under both. Sixteen are
caught and one is equivalent: the depth-first arm opening a new level
when its depth is past the sums' length (D3), which never happens, since
a walk goes one level deeper at a time.

| # | mutation | failures by property |
|---|---|---|
| B1 | ★: a tied deeper level takes the lead | P1 188, P3 60, P4 188, P5 74, P6 33 |
| B2 | ★: the second level always taken | P1 297, P3 399, P5 145, P6 505 |
| B3 | ★: the left child queued twice, the right never | P1 557, P2 379, P3 457, P4 10, P5 197, P6 119 |
| B4 | ★: values counted without their sign | P1 833, P3 157, P4 114, P5 171, P6 393 |
| D1 | dfs: the deepest of tied levels | P1 188, P3 60, P4 188, P5 74, P6 33 |
| D2 | dfs: a right child summed into its parent's level | P1 908, P2 688, P3 229, P4 95, P5 258, P6 763 |
| C1 | counted: every level read as one | P1 815, P3 1044, P5 165, P6 799 |
| C2 | counted: the least sum | P1 1100, P3 298, P4 12, P5 245, P6 490 |
| C3 | counted: negative sums read as 0 | P1 170, P3 338, P4 24, P5 111, P6 29 |
| S1 | stack: the deepest level never read | P1 196, P3 76, P5 340, P6 78 |
| S2 | stack: a tied deeper level taken | P1 188, P3 60, P4 188, P5 74, P6 33 |
| S3 | stack: a right child summed into its parent's level | P1 908, P2 688, P3 229, P4 95, P5 258, P6 763 |
| X1 | solution: a tied deeper level taken | P1 188, P3 60, P4 188, P5 74, P6 33 |
| X2 | solution: the best sum starts at 0 | P1 170, P3 338, P4 24, P5 111, P6 29 |
| X3 | solution: at most four nodes a level | P1 395, P2 278, P3 5, P4 113, P5 89, P6 410 |
| X4 | solution: levels counted by twos | P1 1200, P3 1200, P5 165, P6 1200 |

P1, P3, P5 and P6 catch all sixteen, P4 twelve, and P2 four: the edits
that treat the two children differently (B3, D2, S3) and the one that
reads only the first nodes of a level (X3), the only ones a mirror can
see. The four that let a tied deeper level win (B1, D1, S2, X1) fail
alike, on the trees whose levels tie; the fourth kind exists for them.
The best sum starting at 0 (X2) fails exactly as negative sums read as 0
(C3) does: both answer 1 whenever no level sums above 0, and are right
otherwise.

## Benchmarks

`bench/` times the ★ arm against the same level-by-level walk in C, Rust,
Go and Python, each with its own linked nodes (`Rc<RefCell<…>>` in Rust,
pointers in C and Go). 16 random trees of 10^4 nodes, the constraints'
most, with values over the whole range, are built once; each of 200
rounds hangs one more node on every tree, at a random free place, and
solves it. Every program prints `200 rounds over 16 trees of 10^4 nodes:
levels total 53081, checksum 533943244`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `f5f9065de8`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.312 to 0.403 s | 0.326 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.305 to 0.429 s | 0.342 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.388 to 0.467 s | 0.418 s |
| Kāra (`karac build`) | 0.396 to 0.464 s | 0.424 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.390 to 0.518 s | 0.428 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.393 to 0.569 s | 0.436 s |
| Rust (`rustc -O`) | 0.422 to 0.607 s | 0.532 s |
| Go | 0.739 to 1.054 s | 0.855 s |
| Python | 5.100 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, byte
for byte, so the two Kāra rows are one program timed twice. Kāra takes
about 0.96x overflow-checked Rust's time, the equal-safety comparison,
and 1.3x C's. Unchecked Rust is no faster than checked here, and its runs
spread widest: the walk is bound by following child pointers, not by
the additions. Go's collector runs beside the walk (1.9 s of user time
in 0.86 s), and Python takes about 12x Kāra's time.
