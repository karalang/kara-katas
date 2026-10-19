# 783. Minimum Distance Between BST Nodes

Given the `root` of a binary search tree, return the minimum difference
between the values of any two different nodes in the tree.

```
root = [4, 2, 6, 1, 3]                 ->  1
root = [1, 0, 48, null, null, 12, 49]  ->  1
```

**Constraints:** the tree has 2 to 100 nodes, and every value is from 0
to 100,000.

This is the same problem as kata 530, Minimum Absolute Difference in
BST, with LeetCode's smaller limits. Kata 530's arms walk the tree in
order (recursively, with a stack and by Morris traversal) or sort the
values, so this kata takes other mechanisms.

## Approaches

Every arm is `fn min_diff_in_bst(root: Option[TreeNode]) -> i64` over a
`shared struct TreeNode`. The trees are built by inserting distinct
values in the order given, a smaller value going left and a larger one
right. The values are distinct, so the answer is the smallest gap
between two values next to each other in order.

| file | mechanism |
|---|---|
| `min_diff_in_bst.kara` ★ | ancestor bounds: two values next to each other in order are always an ancestor and its descendant, so walk down carrying each node's nearest ancestor below it and nearest above it, and take the smallest gap to a bound; O(n) |
| `min_diff_in_bst_subtrees.kara` | from the leaves up: each subtree reports its smallest value, its largest and the best gap inside it, and a node takes its own gaps to its left subtree's largest and its right subtree's smallest; O(n) |
| `min_diff_in_bst_sortedset.kara` | the tree walked level by level with a `VecDeque`, every value put in a `SortedSet`, and the gaps read off its ascending walk; never uses that the tree is a search tree; O(n log n) |
| `min_diff_in_bst_descending.kara` | the values in descending order, the right subtree first, by an explicit stack of the nodes on the way down the right edges; O(n) |
| `differential.kara` | the four arms against every pair of values, four properties |

Every arm prints the same 10 lines: LeetCode's two examples, inserted as
`4, 2, 6, 1, 3` and `1, 0, 48, 12, 49`; two values at the ends of the
range; a tree whose closest pairs cross the root, one where the closest
pair is the root and a node two levels down its left subtree; a rising
chain and a falling one; an ascending chain of 100 multiples of 1,000
with one moved 1 up; 100 random values from 0 to 100,000; then 300
random trees of 2 to 100 values, with the sum of the answers and a
checksum. `min_diff_in_bst.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the smallest gap between any two of the values, over every pair. Its
2,000 trees hold 2 to 100 values. A fifth hold planted values: the
multiples of a step from 3 to 1,000, and one more value 1 above one of
them, the only gap of 1, which is the pair 0 and 1 a third of the time
and the largest value and the one below it a third. Of the rest a third
are on 0 to about twice their size, so gaps of 1 are common, a third on
up to about 2,000 and a third on up to 100,000. A quarter of each are
inserted in a random order, a quarter ascending or descending (a chain),
a quarter middle first (a balanced tree) and a quarter from the two ends
alternately (a zigzag path).

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the same values inserted in another random order, a tree of another shape, give the same answer |
| P3 | every value `v` made `top - v`, the tree's mirror image, gives the same answer |
| P4 | one more value, not among them, gives the least of the answer and that value's gap to its nearest |

It prints `2000 trees (smallest gaps sum to 97710), 4 arms, 32000
checks, 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the bound above never looked at | P1 650, P2 860, P3 1343, P4 193 |
| M2 | ★: the left child keeping its parent's bound above | P1 650, P2 860, P3 1343, P4 193 |
| M3 | ★: a bound of `0` taken as missing | P1 82, P2 75, P3 158, P4 1 |
| M4 | subtrees: the right gap to the right subtree's largest | P1 420, P2 526, P3 847, P4 117 |
| M5 | subtrees: a subtree's least left as its root | P1 207, P2 332, P3 436, P4 35 |
| M6 | subtrees: the left subtree's own best dropped | P1 879, P2 844, P3 1053, P4 482 |
| M7 | sortedset: the right child's value taken without its subtree | P1 1262, P2 1212, P3 1485, P4 996 |
| M8 | sortedset: the walk starting from `0` | P1 864, P3 350, P4 9 |
| M9 | sortedset: every gap taken from the smallest | P1 1396, P3 1533, P4 1092 |
| M10 | descending: the left subtrees never walked | P1 1475, P2 1592, P3 1847, P4 1252 |
| M11 | descending: the last gap kept, not the least | P1 1396, P3 1533, P4 1092 |
| M12 | descending: only the first gap | P1 1376, P3 1533, P4 1049 |

P1 kills all twelve. P2 sees only mutants whose answer depends on the
shape of the tree, so not the sortedset and descending arms' M8, M9, M11
and M12, which read the values in order whatever the shape. M1 and M2
fail the same checks, and M9 and M11 do too, because each pair computes
the same wrong function. M1 never compares a node with its bound above
and M2 gives a left child its parent's bound above rather than the
parent: either way the only pairs missed are a node and the largest
value of its left subtree, and M2's farther bound can never give a gap
below the answer. M9 takes every gap from the smallest value and M11
keeps the last gap of the descending walk, and both are the gap between
the two smallest values. M3 is the one first choice that nearly
survived: it takes a bound of 0, the smallest legal value, for a missing
one, which matters only when 0 is an ancestor of the value just above it
and that pair is the only closest one. On the first version of the
differential, without the planted values, it failed 9 of 32,000 checks;
with them it fails 316. Two first choices never ended on a long chain, a
left child queued twice (M7) and a walk down the left edges (M10), and
were replaced by these.

## Verification

Every arm prints the same output as `min_diff_in_bst.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The subtrees arm's summary was first a `struct Span`, and `karac check`
warned that it shadows the prelude type `Span`; the struct is `Summary`
now.

The frozen legacy backends refuse all four arms, the differential and
the bench program at the type check: in `for v in values.iter()` they
take the items for `i64` rather than references, so `*v` is an error.
Copies of the four arms with those `*`s removed print the same output
under the legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build, each build with a
warning that a borrowed `values` is used after a move, since legacy
predates borrowed parameters. The bench timing below is of such a copy.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 search trees
of 100 values from 0 to 100,000, LeetCode's limits, are built once: half
by inserting the values in a random order, a quarter middle first
(balanced) and a quarter in ascending order (a chain of 100). Each of
2,000,000 rounds answers the next tree. Every implementation prints
`2000000 rounds of 100-value trees: gaps sum to 26906250, checksum
58682360`, the Kāra program under `karac __mir-run` included (in 608 s).

Every round walks a tree of 100 nodes and its 101 missing children
recursively, so the bench measures calls and pointer chasing. The Kāra
nodes are a `shared struct`, counted by reference; Rust's are
`Option<Box<TreeNode>>`, and C's and Go's plain pointers. Spot timings
on a shared 4-core container, eight runs of each compiled program, five
of them interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.68 to 0.80 s |
| Rust (`rustc -O`) | 0.62 to 0.83 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.60 to 0.87 s |
| Go | 1.46 to 1.88 s |
| Python | 102.5 to 103.7 s |
| Kāra (`karac build --mir`) | 1.90 to 2.70 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 5.0 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.00 s,
against C's 0.73, Rust's 0.68 (0.63 under overflow checks) and Go's
1.59. Under valgrind's cachegrind v2 runs 16.0 billion instructions and
1.34 billion branches, against C's 8.27 billion and 0.48 billion and
Rust's 7.46 billion and 0.48 billion; it mispredicts 130 million
branches to their 101 and 99 million. Where v2's extra instructions lie
is not profiled. The legacy build of the copy ran 1.42 to 1.74 s, a
median of 1.63 s in the interleaved runs, so v2 takes 1.23 times legacy.
The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new.
