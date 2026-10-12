# 437. Path Sum III

Given the `root` of a binary tree and an integer `targetSum`, return
the number of paths where the sum of the values along the path equals
`targetSum`. The path does not need to start or end at the root or a
leaf, but it must go downwards (from parent nodes to child nodes only).

```
root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8              ->  3
root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22        ->  3
```

**Constraints:** the number of nodes is in `[0, 1000]`;
`-10^9 <= Node.val <= 10^9`; `-1000 <= targetSum <= 1000`.

## Approaches

The tree is a `shared struct TreeNode` with `mut left` and `mut right`
links, the binary tree type the other katas use. Every arm is
`path_sum(root: Option[TreeNode], target: i64) -> i64`. A path can sum
past the range of 32 bits, so the sums are `i64`.

| file | mechanism |
|---|---|
| `path_sum.kara` ★ | prefix sums: walk depth first keeping a `Map` from each prefix sum on the path from the root to how often it occurs. The paths ending at a node that hit the target are the earlier prefixes equal to the node's prefix minus the target. The node's prefix is added before its children and removed after. O(n) expected |
| `path_sum_double.kara` | a walk from every node: for each node, count the paths that start there by walking down with the remaining sum. O(n x height) |
| `path_sum_suffix.kara` | keep the values on the path from the root in a vector, and at each node add them up from the node back to the root, counting each hit. O(n x height) |
| `path_sum_stack.kara` | the ★ arm's prefix-sum walk on an explicit stack: each node is pushed once to enter it and once more to leave it and remove its prefix. O(n) expected |
| `differential.kara` | the four arms on 1,500 random trees, five properties |

Every arm prints the same 10 lines: the two LeetCode examples, seven
edge cases (the empty tree, one node equal to the target, four zeros
with target 0, a chain alternating 1 and -1, a chain of 10^9 values
summing past 32 bits, a chain of -10^9 values, and a perfect tree of
1 to 15), and for 300 random trees of up to 60 nodes with values in
[-5, 5] the total count and a checksum. `path_sum.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, sharing one
`TreeNode`, and runs them on 1,500 random trees of up to 50 nodes read
from a random level order, with values within 1, 3 or 10 of zero and a
target in [-5, 5].

| | property |
|---|---|
| P1 | the count is the reference's, which reads the level order into a table of parents and sums up the parent links, never building a tree |
| P2 | the mirror image of the tree gives the same count |
| P3 | negating every value and the target gives the same count |
| P4 | multiplying every value and the target by one factor up to 1,000,003 gives the same count |
| P5 | a chain of k zeros has k(k + 1)/2 paths summing to 0, a chain of k ones has k - s + 1 summing to s, a perfect tree of one value v that is not 0 has one per node summing to v, and the empty tree has none |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | prefix sums: a prefix is never removed on the way back | P1 855, P2 805, P5 1013 |
| M2 | prefix sums: the empty prefix above the root is not counted | P1 599, P5 1500 |
| M3 | every start: a path may not end at a leaf | P1 831, P5 1500 |
| M4 | every start: no path starts in a right subtree | P1 789, P2 677, P5 1490 |
| M5 | suffix sums: the sum back stops below the root | P1 599, P5 1500 |
| M6 | suffix sums: a node alone is never a path | P1 576, P5 1500 |
| M7 | stack: a right child gets the prefix above its parent | P1 790, P2 855, P5 1441 |
| M8 | stack: leaving removes the prefix twice | P1 855, P2 805, P5 1013 |

P3 and P4 change the values and the target alike, and none of these
mutants depends on what the values are, only on which paths it counts,
so neither property sees any of them; they guard against an arm that
compares sums wrongly or overflows. P2 sees the mutants that treat left
and right differently (M4, M7) and the ones that leak a prefix from one
subtree into its sibling (M1, M8), since mirroring changes which
sibling goes first. M2 and M5 are the same mistake in two arms, paths
from the root not counting, and fail alike, as do M1 and M8.

## Verification

All four arms print the same output as `path_sum.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and all four frozen legacy backends: `karac run --interp`, LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`. `karac check` passes
on every file. The differential prints `30000 checks, 0 failures`
under `karac __mir-run`, `karac __mir-llvm-run` and
`karac run --interp`. The four arms and the differential also run
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

The legacy code generator does not compile the differential: it
refuses `[1, 3, 10][next_random(seed) % 3]`, an index into an array
literal, as in katas 435 and 436. Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It builds one random tree of
100,000 nodes with values in [-1000, 1000], each node hung on a free
side of a random earlier node that still has one, then counts the
paths for 200 random targets in [-2000, 2000], each count a fresh walk
with a fresh map. Every implementation prints `200 targets on a tree
of 100000: 71159 paths, checksum 117505869`; a 3-target cut of the
Kāra program under `karac __mir-run` prints the same as the C program
cut the same way.

The mirrors keep the ★ arm's structure: Rust's nodes are
`Rc<RefCell<TreeNode>>`, as a Kāra `shared struct` is reference
counted, and its `HashMap` hashes with SipHash-1-3 under a random key,
as Kāra's `Map` does; Go uses pointers and a map. C keeps the nodes in
one array linked by index and the prefix counts in an open-addressing
table with a multiplicative hash, cleared for each target. Spot timings
on a shared 4-core container, three runs each (`bench.sh` timings need
a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.95 to 1.07 s |
| Go | 1.50 to 1.52 s |
| Rust (`rustc -O`) | 2.22 to 2.29 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.23 to 2.27 s |
| Kāra (legacy `karac build`) | 2.33 to 2.75 s |
| Python | 11.0 to 11.1 s |

Most of the time is in the map: each node does a lookup and two
updates. The Kāra program prints the same line under
`karac __mir-llvm-run` in 33 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings; one extension of an open row.

- **A bare `for` over a borrowed `Vec` types its items as values under
  `karac __mir-run`** (kara `B-2026-10-12-9`, extended by this kata).
  The differential's `mapped` helper first read
  `for v in vals { ... *v * factor ... }` over a borrowed
  `vals: Vec[i64]`. core-semantics.md §4.6 gives a bare `for` over a
  collection `ref T` items, so `*v` is right; `karac check` accepts it
  and `karac __mir-run` refuses it as `found 'i64'`. The helper writes
  `v`, which §5.10 allows for a `Copy` item, so nothing is routed
  around.
