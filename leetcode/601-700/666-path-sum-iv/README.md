# 666. Path Sum IV

A binary tree at most four levels deep is given as a sorted list of
three-digit numbers, one per node: the hundreds digit is the node's
depth, from 1, the tens digit its position in that level, from 1, as in
a full tree, and the units digit its value. Return the sum of the path
sums from the root to every leaf.

```
nums = [113,215,221]  ->  12   (3 + 5 and 3 + 1)
nums = [113,221]      ->  4    (3 + 1)
```

**Constraints:** 1 to 15 numbers, each a valid node of a connected tree,
listed in ascending order.

## Approaches

Every arm is `fn path_sum(nums: Vec[i64]) -> i64`. The children of
position `p` are at `2p - 1` and `2p` one level down, and its parent at
`(p + 1) / 2` one level up.

| file | mechanism |
|---|---|
| `path_sum_iv.kara` ★ | a `Map` from each node's depth and position to its value, walked down from the root carrying the sum so far, which is added in at each node with no children; O(n) |
| `path_sum_iv_leaves.kara` | each value times the number of leaves below it, the list walked backwards so that children hand their leaf counts up to their parents first; O(n) |
| `path_sum_iv_grid.kara` | a fixed 5 by 9 grid of the places, and from each leaf a walk up through its parents adding their values; O(n * depth) |
| `path_sum_iv_levels.kara` | each node's path sum, its parent's plus its own value, worked out in list order, which puts parents first, then the sums at nodes no child names as parent added up; O(n) |
| `differential.kara` | the four arms against a definition that builds the tree as linked nodes, five properties |

Every arm prints the same 8 lines: the two LeetCode examples; one node;
a chain down the left and one down the right; a full tree of four levels
of 9s and the same of 0s; and the largest sum of 2,000 random trees of
1 to 4 levels, with a checksum. `path_sum_iv.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which builds the tree as linked nodes, each hung under the node one
level up at half its position rounded up, and lists every root-to-leaf
path with its sum and its length. Each of 1,500 random trees is 1 to
4 levels deep, each child there with chance 30 to 100 in 100, with
values from 0 to 8 so that each can be raised by 1.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the mirrored tree, each position `p` at depth `d` moved to `2^(d - 1) + 1 - p`, sums the same |
| P3 | every value raised by 1 adds the length of every path |
| P4 | two children of 0 under each leaf above the fourth level count its path twice |
| P5 | the root raised by 1 adds one for each leaf |

It prints `1500 trees (5568 nodes), 4 arms, 30000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node with one child taken as a leaf too | P1 611, P3 643, P4 447, P5 162 |
| M2 | ★: the children looked for at `2p` and `2p + 1` | P1 837, P2 886, P3 853, P4 1223, P5 645 |
| M3 | leaves: every node counted as a single leaf | P1 607, P3 645, P4 1223, P5 645 |
| M4 | leaves: the parent taken at half the position, rounded down | P1 605, P2 260, P3 640, P4 1216, P5 645 |
| M5 | grid: a node with one child taken as a leaf too | P1 609, P3 643, P5 643 |
| M6 | grid: the walk up stopping below the root | P1 1313, P3 1500, P4 1130, P5 1500 |
| M7 | levels: only a leaf's own value added | P1 903, P3 960, P4 1223, P5 960 |
| M8 | levels: each node marked as having children, not its parent | P1 936, P3 960, P4 1223, P5 645 |
| E1 | ★: the right child's key worked out afresh | 0 |
| E2 | leaves: a leaf known by fewer than 1 leaf below | 0 |
| E3 | grid: a 6 by 10 grid | 0 |
| E4 | levels: a parent marked with `false` | 0 |

P1 and P3 each kill all eight, and P4 all but M5. P2, the mirror, sees
only M2 and M4, the two that get the arithmetic of positions wrong,
which a mirror changes; the rest go wrong the same way in a tree and its
mirror image. P5 sees all but M1, which takes a node with one child for
a leaf too: the root is on that wrong path just as it is on the right
ones, so raising it adds one for each of them either way. M5, the same
mistake in the grid arm, slips past P4 because the extra children of
0 make the same mistake count the same twice. The four survivors cannot
change an answer: `left + 1` is the right child's key by any route; the
leaf counts are never negative, so below 1 means 0; a bigger grid only
has more empty places; and the levels arm asks only whether a parent was
marked, not with what.

## Verification

Every arm prints the same output as `path_sum_iv.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `72739d54d6` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: they read through `*` the numbers that `iter()` and `get` hand
them, which legacy types as plain `i64`s, and the harness hands `seed`,
already a `mut ref` parameter, on with the `mut` marker design.md asks
for. Legacy rejects both. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 256 random trees of the
problem's deepest, four levels, once, each child there with chance 50 to
100 in 100; then each of 1,000,000 rounds sums one, picked by the round,
into a checksum. Every implementation prints `256 trees, 1000000 rounds:
checksum 659065943`, the Kāra program under `karac __mir-run` included
(in 41 s).

Each implementation is the same walk over a fresh map for each tree:
Kāra's `Map` and Rust's `HashMap` both hash with SipHash, Go's map with
its own hash, and Python's dict. C has no map, so a table indexed by the
key, `10 * depth + position`, stands in for it, which needs no hashing
at all. Spot timings on a shared 4-core container, three runs each (two
for Python; `bench.sh` timings need a quiet machine), each including
making the trees:

| | time |
|---|---|
| C (`clang -O3`) | 0.04 to 0.06 s |
| Rust (`rustc -O`) | 0.63 to 0.78 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.68 to 0.77 s |
| Go | 0.65 to 0.71 s |
| Python | 3.3 to 3.7 s |
| Kāra (`karac build --mir`) | 0.82 to 1.12 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking, for the same `*` reads and `mut` markers as
the arms and for `trees[r % 256]` handed to `path_sum` without a copy,
which design.md allows, since a parameter borrows, and which legacy
rejects as a move out of an index. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata without those
builds under legacy and takes 0.91 to 0.99 s, a copy of each tree's list
included. Under `karac __mir-llvm-run` the program prints the same line
in 10 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is about level with legacy and within about a third of
Rust and Go, all three hashing every key of every tree. C's table needs
no hashing at all, which is why it is more than ten times faster; it is
not the same work. The comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
