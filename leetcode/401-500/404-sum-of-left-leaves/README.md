# 404. Sum of Left Leaves

Given the root of a binary tree, return the sum of all its left leaves:
the leaves that are the left child of their parent.

```
root = [3,9,20,null,null,15,7]  -> 24   (9 + 15)
root = [1]                      -> 0
```

**Constraints:** the tree has 1 to 1000 nodes; `-1000 <= Node.val <=
1000`. The root alone is not a left leaf.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `sum_of_left_leaves.kara` ★ | recursion over the tree, passing down whether each node is a left child; a leaf answers its value only if it is | O(n) | O(height) stack |
| `sum_of_left_leaves_stack.kara` | the same walk with an explicit stack of (node, is left child) pairs | O(n) | O(n) stack entries |
| `sum_of_left_leaves_linked.kara` | over linked `shared struct TreeNode`s with optional children, as LeetCode hands the tree over: each node checks whether its left child is a leaf, and recurses into it if not | O(n) | O(height) stack |
| `sum_of_left_leaves_enum.kara` | over a recursive `shared enum Tree { Empty, Branch(i64, Tree, Tree) }`; a match pattern `Branch(val, Empty, Empty)` picks out a leaf | O(n) | O(height) stack |
| `differential.kara` | the four arms on 3,000 random cases whose answers are known by construction, five properties | — | — |

The first two arms work on the corpus index pool (`Vec[Node]`, child
indices, -1 = none), built from LeetCode's level-order array with a
NULL sentinel. The linked and enum arms take the same pool and convert
it before solving, as kata 333's linked arm does.

Every arm prints the same 12 lines: the two LeetCode examples, nine
edge cases (an empty tree, a single left or right child, chains of
right and of left children, a left leaf under a right child, negative
values, the perfect tree of 15 nodes), and for 2,000 random trees of 1
to 60 nodes, values from -100 to 100, each node hung on a random free
child slot of an earlier one, the total of the sums and a checksum.
`sum_of_left_leaves.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 3,000 random
cases builds trees whose answers are known without solving them:

| | property |
|---|---|
| P1 | a tree with no left children, a chain of right children, sums to 0 |
| P2 | a tree's sum plus its mirror image's sum is the sum of all its leaves but the root |
| P3 | a perfect tree of depth 2 to 6 sums to the values at the even positions of its last level |
| P4 | hanging a new leaf `v` as the left child of a leaf `w` changes the sum by `v`, less `w` if `w` was a left leaf |
| P5 | the sum is that of every leaf named by its parent's left index, found by a scan of the index pool with no tree walk |

It prints `3000 cases, 4 arms, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | rec: the root counts as a left child | P1 80, P2 52, P4 58, P5 52 |
| M2 | rec: the sides are swapped, so right leaves count | P1 2914, P3 2995, P4 2980, P5 2941 |
| M3 | stack: every leaf counts, on either side | P1 2994, P2 2991, P3 2993, P4 1530, P5 2883 |
| M4 | stack: a left child is pushed as a right child | P2 2939, P3 2985, P4 2980, P5 2846 |
| M5 | linked: a left child that is not a leaf is not searched | P2 2828, P3 2404, P4 2695, P5 2705 |
| M6 | linked: a leaf is any node with no left child | P2 2740, P4 879, P5 2539 |
| M7 | enum: a node with an empty left subtree is a leaf, whatever its right | P2 2789, P4 1507, P5 2645 |
| M8 | enum: the right subtree is searched as a left child | P1 2914, P2 2939, P3 2993, P4 1472, P5 2831 |

P2 cannot see M2: an arm that sums the right leaves still gives, with
the mirror image, the sum of all leaves. M1 is caught only where the
root is itself a leaf, a tree of one node, which is why its counts are
small.

## Verification

All four arms print the same output as `sum_of_left_leaves.py` on every
backend: `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run`, `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. `karac check` passes on every file.
The differential prints `60000 checks, 0 failures` on all six (20
minutes under `karac run --interp`, a debug build, and seconds on the
rest).

## Benchmarks

The bench program uses the ★ arm on 50 random trees of 30,000 nodes,
built as in the harness, each summed 50 times; it folds the sums into a
total and a checksum. Before each round it raises one node's value by
1, so that no compiler can hoist the sum out of the loop: with the
rounds identical, `clang -O3` computed it once per tree and ran in 0.11
s. The bench's `Node` declares `val` as `mut` for that, unlike the kata.
Trees stop at 30,000 nodes because the LCG gives 15-bit numbers, and a
parent is picked as one of them. Every implementation prints `50 trees
of 30000 nodes, 50 rounds: total 1162500, checksum 420402371`; a 2-tree
cut of the Kāra program under `karac __mir-run` prints the same as the
C program cut the same way. Spot timings on a shared 4-core container
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 1.03 s |
| C (`clang -O3`) | 1.08 to 1.13 s |
| Kāra (legacy `karac build`) | 1.06 to 1.23 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.07 to 1.18 s |
| Go | 1.22 to 1.38 s |
| Python | 17 s |

Most of the time is the walk's random accesses into a pool of 30,000
nodes, so the four compiled programs are close. The Kāra program also
prints the same line under `karac __mir-llvm-run` in 2.4 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark. The `karac build` time is the frozen legacy backend,
which also warns that `nodes` is moved twice in `visit`, since it
predates bare parameters borrowing. Not filed.

## Compiler findings

No new findings.
