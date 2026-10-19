# 776. Split BST

Given the root of a binary search tree and an integer `target`, split
the tree into two subtrees: one of the nodes whose values are at most
`target`, and one of the nodes whose values are greater. Most of the
structure must remain: if a child and its parent end up in the same
subtree, the child must still be that parent's child. Return the roots
of the two subtrees, the small one first.

```
root = [4,2,6,1,3,5,7], target = 2  ->  [[2,1],[4,3,6,null,null,5,7]]
root = [1], target = 1              ->  [[1],[]]
```

**Constraints:** the tree has 1 to 50 nodes; values and `target` are
from 0 to 1000, and the values are distinct.

## Approaches

Every arm is `fn split_bst(root: Option[TreeNode], target: i64) ->
(Option[TreeNode], Option[TreeNode])` over the same `shared struct
TreeNode` with `mut` children. The answer is unique: in each part, a
node's parent is its nearest ancestor in the original tree on the same
side of the target. So the harness prints both parts in LeetCode's
level-order form.

| file | mechanism |
|---|---|
| `split_bst.kara` ★ | recursive: a node no greater than the target keeps its left subtree, and the small part of its right subtree becomes its new right child; a greater node is the mirror image. One path is walked; O(height) time and stack |
| `split_bst_topdown.kara` | iterative: walk the same path, hanging each small node as the right child of the small tree's last node and each large one as the left child of the large tree's last node, then cut the two tails; placeholder heads save a special case. O(1) extra space |
| `split_bst_stack.kara` | the path's nodes on a stack, then taken off from the bottom up, each small node taking the small tree so far as its right child and each large node the large tree as its left: the ★ arm's recursion made explicit |
| `split_bst_copying.kara` | path copying: as the ★ arm, but each node on the path is copied with the split subtree in place of the child the path left by, and the subtrees off the path are shared, so the input tree is left whole |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: LeetCode's two examples; one node
split the other way; a tree of nine split at four targets, two below or
above every value; an ascending and a descending chain; a zigzag; then
300 random trees of 1 to 50 distinct values from 0 to 1000 with a random
target, with the number of nodes in the small parts and a checksum of
both parts' level-order forms. `split_bst.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, all on the ★ arm's
`TreeNode`, and the definition: each node's parent is its nearest
ancestor on its own side of the target, found by one walk of the
original tree, and a node with none is its side's root. Its 1,300 random
trees are 1,200 within LeetCode's limits and 100 of 51 to 250 values
from 0 to 5,000. The in-place arms take the tree apart, so each split is
of a tree built afresh from the same values.

| | property |
|---|---|
| P1 | the split is the definition's: every node has the expected parent, every small value is at most the target and every large one above it, and each part is in order |
| P2 | splitting the small part again at a lower target, or the large part at a higher one, gives what splitting the whole tree there gives |
| P3 | the mirror image (values negated, inserted in the same order) split at `-target - 1` gives the mirror images of the two parts, swapped |
| P4 | the target lowered to the largest value at most it, or below every value, gives the same split |

It prints `1300 trees (22963 small nodes), 4 arms, 20800 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error; it runs in 22 s under
`karac __mir-run`.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node equal to the target sent to the large side | P1 43, P3 69, P4 1185 |
| M2 | ★: the right subtree's large part hung back under the node | P1 1144, P2 500, P3 1252 |
| M3 | ★: the two parts swapped below a greater node | P1 1197, P2 1113, P3 1300 |
| M4 | topdown: the small tree's tail not cut | P1 564, P2 114, P3 1125 |
| M5 | topdown: the walk going left from a small node | P1 1181, P3 1281 |
| M6 | topdown: the large tree's tail not moved down | P1 1197, P3 1300 |
| M7 | stack: the small tree hung as a left child | P1 1181, P2 952, P3 1281 |
| M8 | stack: the path taken off from the top down | P1 1218, P2 1176 |
| M9 | stack: a large node keeping its old left child | P1 993, P2 344, P3 1125 |
| M10 | copying: a small node's left subtree dropped | P1 1100, P2 724, P3 1256 |
| M11 | copying: a greater node's right child split | P1 1158, P3 1281 |
| M12 | copying: a small node returned uncopied | P1 983, P3 1125 |

P1 kills all twelve. M1 shows what P4 is for: it differs from the right
answer only when the target is one of the tree's values, which a random
target rarely is, so P1 sees it 43 times; P4 lowers the target to a
value in the tree whenever any value is at most it, and sees it 1185
times. P3 sees every mutant but M8, since each of the others treats the
small and large sides differently, which the mirror image swaps. M8
takes the path from the top down and hangs each node under the one below
it, the same on both sides, so the mirror image does not tell; P2 does,
because the part it splits again is wrong. No first choice survived.

## Verification

Every arm prints the same output as `split_bst.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`4f079681eb`, whose last compiler change is `ecb1a0322e`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) prints the same
output for all four arms and the differential's line (in 477 s). The
legacy compiled backends accept every file and then corrupt the heap on
every arm: under the legacy JIT (`karac run`) and `karac build` the arms
stop with `free(): double free detected in tcache 2`, `malloc():
unaligned fastbin chunk detected` or a segmentation fault, and so does
the built differential. The legacy build of the bench, the same source,
stops with `integer overflow` in `weigh`, where a value of at most 1000
times a depth of at most 50 cannot overflow; the legacy interpreter did
not finish the bench in 15 minutes. Legacy is frozen, so all this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 orders of 50
distinct values from 0 to 1000, LeetCode's limits, each with a target,
are drawn once. Each of 200,000 rounds inserts the next order's values
into a fresh tree, splits it at its target and weighs both parts (every
value times its depth). Every implementation prints `200000 rounds of
50 values: checksum 986184091`, the Kāra program under `karac
__mir-run` included (in 116 s).

A split takes the tree apart, so every round builds its tree again, and
the 50 insertions and the walks cost far more than the split's walk down
one path: the bench measures building, splitting and walking small trees
of shared nodes. Rust's tree is `Rc<RefCell<TreeNode>>`, the closest
match to a `shared struct`; C frees each round's nodes, Go leaves them
to the collector. Spot timings on a shared 4-core container, eight runs
of each compiled program, five of them interleaved, and three of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.62 to 0.77 s |
| Rust (`rustc -O`) | 0.74 to 0.95 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.69 to 0.97 s |
| Go | 0.79 to 0.96 s |
| Python | 4.97 to 5.57 s |
| Kāra (`karac build --mir`) | 0.91 to 1.20 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` does not run it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 2.9 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 0.95 s,
against C's 0.64, Rust's 0.88 (0.85 under overflow checks) and Go's
0.83. Under valgrind's cachegrind v2 runs 4.13 billion instructions,
Rust 4.17 billion and C 2.66 billion. There is no legacy time to compare
with. The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new.
