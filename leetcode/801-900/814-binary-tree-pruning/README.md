# 814. Binary Tree Pruning

Given the root of a binary tree whose values are all 0 or 1, return the
same tree with every subtree that does not hold a 1 removed. A subtree
of a node is that node and every node below it.

```
root = [1, null, 0, 0, 1]           ->  [1, null, 0, null, 1]
root = [1, 0, 1, 0, 0, 0, 1]        ->  [1, null, 1, null, 1]
root = [1, 1, 0, 1, 1, 0, 1, 0]     ->  [1, 1, 0, 1, 1, null, 1]
```

**Constraints:** the tree has 1 to 200 nodes, and every value is 0 or 1.

## Approaches

A node stays exactly when its subtree holds a 1. Every arm cuts the
nodes that fail that test and leaves the rest where they were, changing
the tree in place.

| file | mechanism |
|---|---|
| `prune_tree.kara` ★ | post-order recursion: prune both children, then the node goes when its value is 0 and nothing is left under it. O(n) time, O(height) stack |
| `prune_tree_keep.kara` | `keep(node)` prunes the node's subtree and says whether it holds a 1, cutting each child whose subtree holds none; the root goes when even it is not worth keeping. O(n) time, O(height) stack |
| `prune_tree_stack.kara` | post-order with an explicit stack, each node visited twice: once to push its children, once after them to cut any child that has become a leaf of value 0. O(n) time, O(n) stack |
| `prune_tree_search.kara` | top down: search each subtree for a 1, drop it when there is none and otherwise ask its children in turn. O(n * height) time |
| `differential.kara` | the four arms against the nodes whose subtree holds a 1, four properties |

The ★ arm's test, a 0 with nothing left under it, is the statement's
test in disguise: the children are already pruned, so a child that is
still there holds a 1, and a node with no child left holds a 1 only if
it is one.

Every arm prints the same 11 lines: LeetCode's three examples; one 0 and
one 1 alone; a tree of 0s, which goes entirely; a 1 under a 0 that keeps
the 0; a line of 0s down to a 1 at the bottom; LeetCode's largest, 200
random nodes with one value in ten a 1, and 200 nodes in a zigzag line
with a 1 only at the bottom, each with the number of nodes kept and a
checksum of the values in pre-order; and 300 random rounds of 1 to 30
nodes, with a total and a checksum. The trees are read and written in
LeetCode's level order. `prune_tree.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, sharing the ★ arm's
`TreeNode`, and the statement itself on a tree held as arrays: every
node after the first hangs from an earlier one, so one pass from the
back marks every node whose subtree holds a 1, and the answer is the
marked nodes in pre-order. Its 1,600 cases have 1 to 25 nodes and come
in four kinds of 400: a 1 one time in two; one time in ten, so that most
subtrees go; no 1 at all or a single one, so that the whole tree goes or
one path to the root stays; and lines, one child per node, with a 1 one
time in six. 444 of the cases prune to nothing.

| | property |
|---|---|
| P1 | the statement's tree |
| P2 | every 1 kept, and no leaf of value 0 left |
| P3 | pruning the pruned tree again changes nothing |
| P4 | the mirrored tree prunes to the mirror of the answer |

It prints `1600 cases (444 pruned to nothing), 25600 checks over 4 arms:
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a 0 with a left child but no right one cut | P1 865, P2 865, P4 858 |
| M2 | ★: the right subtree never pruned | P1 1366, P2 1366, P4 1385 |
| M3 | ★: leaves holding 1 cut, not 0 | P1 1600, P2 1600, P4 1600 |
| M4 | keep: a node kept only for its children | P1 1156, P2 1156, P4 1156 |
| M5 | keep: a right child never cut | P1 769, P2 769, P4 779 |
| M6 | keep: the root never cut | P1 444, P2 444, P4 444 |
| M7 | stack: right children never visited | P1 1270, P2 1270, P4 1299 |
| M8 | stack: the root never cut | P1 444, P2 444, P4 444 |
| M9 | stack: a 0 with only a left child counted as a leaf | P1 865, P2 865, P4 858 |
| M10 | search: only the right subtree searched for a 1 | P1 865, P2 865, P4 858 |
| M11 | search: every 0 cut, ones below or not | P1 1051, P2 1051, P4 1051 |
| M12 | search: the left subtree never pruned | P1 984, P2 984, P4 974 |

P1 and P2 kill all twelve. P3 kills none: every edit still prunes the
children before the node, or in M11 cuts without looking down, so a
second pass finds nothing new to cut. M6 and M8, which never cut the
root, are seen only on the 444 cases that prune to nothing. M1, M9 and
M10 fail on the same cases: each one, by a different road, loses a 0
whose only child left after pruning is its left one.

## Verification

Every arm prints the same output as `prune_tree.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`d0ad6409f5`, whose last compiler change is `c120cafada`; the release
build that runs `check` and `__mir-run` is at `f6f2efb14`, one parser
change behind it. The runtime archives were built after the last runtime
change in that tree, `45d6c491fc`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak. Every pruned
node must be freed here, as nothing else holds it once its parent lets
go.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for all four arms, `karac build` with a warning that the harness uses
`vals` after a move, legacy taking a bare parameter as owned. Legacy
refuses the differential, as it types the item of `shape.vals.iter()` as
an `i64` rather than a reference and so refuses its `*`, and the bench
program, reading `build(vals[g], ..)` as moving a `Vec` out of an index
(`E_INDEX_MOVE_NON_COPY`). Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 random trees
of 200 nodes, LeetCode's largest, are drawn once as arrays, about one
value in eight a 1, each node after the first hung from a free child
place of an earlier one. Each of 300,000 rounds flips one value of the
next tree, builds it as nodes, prunes it and weighs what is left, every
value plus one times its depth. C frees each pruned node and each
round's tree; Rust's tree is `Rc<RefCell<TreeNode>>`, LeetCode's Rust
signature and the closest match to a `shared struct`. Every
implementation prints `300000 rounds of 200 nodes: checksum 414835152`,
the Kāra program under `karac __mir-run` included, in 413 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 3.07 to 3.43 s |
| Rust (`rustc -O`) | 4.16 to 4.65 s |
| Rust (`rustc -O -C overflow-checks=on`) | 4.13 to 4.49 s |
| Go | 3.66 to 4.55 s |
| Python | 23.52 to 23.80 s |
| Kāra (`karac build --mir`) | 3.84 to 4.37 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 6.4 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 4.02 s,
against C's 3.21, Go's 3.89 and Rust's 4.54 (4.29 under overflow checks,
within the noise of the plain build). A round allocates 200 nodes, walks
them three times and frees them, so the time goes to the allocator and
to following pointers; there is little arithmetic to check. Under
valgrind's cachegrind v2 runs 21.1 billion instructions and 3.52 billion
branches, C 16.3 billion and 2.44 billion, Rust 25.2 billion and 3.43
billion: Rust pays for `RefCell`'s borrow flags and for taking each
child out and putting it back, and v2's extra over C is most likely its
reference counts (not traced). Built for `x86-64-v3`, the target `karac
build` uses, C (`clang -O3 -march=x86-64-v3`) takes 3.13 to 3.41 s and
runs the same 16.3 billion instructions, as nothing here vectorizes, and
Rust with overflow checks (`-C target-cpu=x86-64-v3`) 4.12 to 4.51 s,
against v2's 3.97 to 4.39 s in the same five interleaved runs. Python
takes 23.6 s, seven times C's time. Legacy refuses the bench program
(see Verification), so there is no legacy timing to set v2 against. The
comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench passed
`karac check` and every v2 lane as first written.
