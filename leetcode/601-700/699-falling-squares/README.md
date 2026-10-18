# 699. Falling Squares

Squares are dropped one at a time onto the X axis. `positions[i] =
[left, side]` is a square of side length `side` whose left edge is at
`left`; it falls straight down until it lands on the axis or on top of
an earlier square. A square only brushing another at an edge does not
land on it, and once landed it stays. Return an array whose i-th entry
is the height of the tallest stack after the i-th square lands.

```
positions = [[1, 2], [2, 3], [6, 1]]      ->  [2, 5, 5]
positions = [[100, 100], [200, 100]]      ->  [100, 100]
```

**Constraints:** 1 <= `positions.length` <= 1,000; 1 <= `left` <=
10^8; 1 <= `side` <= 10^6.

## Approaches

Every arm is `fn falling_squares(positions: Vec[(i64, i64)]) ->
Vec[i64]`. A square covers [left, left + side), so two squares meet when
each starts before the other ends; touching at an edge is not meeting.

| file | mechanism |
|---|---|
| `falling_squares.kara` ★ | each square against every earlier one: its top is its side plus the highest top among those it overlaps; O(n^2) time, O(n) space |
| `falling_squares_cells.kara` | the distinct edges sorted, each gap between neighbours a cell with a height; a square takes the highest of its cells and raises them all; O(n^2) |
| `falling_squares_tree.kara` | the same cells in a segment tree with range highest and range set, a setting left on the highest node that covers it and pushed down when needed; O(n log n) |
| `falling_squares_intervals.kara` | the ground as a `SortedMap` from where each flat stretch starts to its height; a square cuts the stretches at its two edges, lands on the highest between them and replaces them with one; O(n log n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: the two LeetCode examples; one
square; four squares that only touch; four on one spot; a wide square
over two towers with narrow ones on it and beside it; a stair of
1,000 squares of 100,000, each overlapping the last by one, and a row of
1,000 squares of 1,000,000 side by side down from 100,000,000; and
40 random problems of up to 1,000 squares, on a stretch of ground from
1 to nearly 10^8 wide and with sides up to 1 to 1,000, with a checksum
of every answer. `falling_squares.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: the ground is a row
of columns of width one, a square covers the columns from its left edge
to one short of its right, lands on the highest of them and raises them
all, and the answer is the highest column. 3,000 random problems of 1 to
12 squares are checked, sides 1 to 6, left edges from 1 to a random 1 to
30, so some pile up on a narrow stretch and some spread out.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | every square moved 1,000 to the right, the same answer |
| P3 | the picture mirrored, a square on [l, l + s) moved to [60 - l - s, 60 - l), the same answer |
| P4 | every coordinate and side times three, every answer times three |

It prints `3000 problems, 4 arms, 48000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. One more edit, E1, changes
nothing that can be seen, and the differential rightly reports no
failure for it.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: squares that touch at an edge counted as overlapping | P1 768, P3 1257 |
| M2 | ★: the answer is the latest top, not the highest so far | P1 2037 |
| M3 | ★: a square lands on the latest square it overlaps | P1 423 |
| M4 | cells: the cell right of a square counted as under it | P1 790, P3 1257 |
| M5 | cells: only a square's first cell raised | P1 1868, P3 2243 |
| M6 | cells: a square's top is the higher of its base and its side | P1 2483 |
| M7 | tree: a pending setting never cleared once pushed down | P1 587, P3 614 |
| M8 | tree: a node's highest not updated after its children are set | P1 3000 |
| M9 | tree: a node outside the range answers its own highest | P1 2351 |
| M10 | intervals: no cut at a square's right edge | P1 1768, P3 2351 |
| M11 | intervals: a cut starts at height 0 | P1 2247, P3 2240 |
| M12 | intervals: the stretches under a square left in place | P1 1129, P3 1532 |
| E1 | cells: repeated edges kept | none (equivalent) |

P1 kills all twelve. P3 sees the mutants that treat the two sides of a
square unlike: counting an edge contact as overlap on one side (M1) or
the cell to the right as under the square (M4), raising only the first
cell (M5), a pending setting reapplied (M7), and the interval arm's
slips at its edges (M10 to M12). P2 and P4 see none: every arm uses only
the order of the edges and the sums of sides, so moving or scaling the
picture moves or scales a mutant's mistake with it. E1 keeps repeated
edges: `binary_search` finds the same copy of an edge every time, so a
square's right edge and the next square's left edge still meet at one
place, and the empty cells between copies are never under a square.

## Verification

Every arm prints the same output as `falling_squares.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`ec489d962f` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking, at `*` on an item of `.iter()` (`*h`
in the harness, `*left` and `*side` in the other three arms): legacy
gives the item by value, while on v2 it is a reference. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the segment-tree arm, the same in all five
languages; C has no sorted map, and the tree is what a C program would
write. It builds 100 problems of 1,000 squares once, problem p on a
stretch of ground 1,000 + 999,990 p wide with its own largest side up to
1,000,000; then it answers every problem in each of 5 rounds, putting
the tallest stack at the end into a checksum. Every implementation
prints `5 rounds of 100 problems of 1000 squares: tallest stacks sum to
43322825, checksum 715600227`, the Kāra program under `karac __mir-run`
included (in 153 s).

For the legacy row a copy of the bench program drops the `*` on `left`
and `side`, the only change, and prints the same line.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.25 to 0.29 s |
| Rust (`rustc -O`) | 0.18 to 0.22 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.18 to 0.25 s |
| Go | 0.29 to 0.30 s |
| Python | 4.3 to 4.5 s |
| Kāra (`karac build --mir`) | 0.58 to 0.75 s |
| Kāra, legacy (`karac build`, the copy) | 0.22 to 0.28 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 24 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is more than twice as slow as legacy here, and behind
the other four, because of the O(n) binary search below. The comparison
with C and Rust waits until after M4.

## Compiler findings

kara B-2026-10-18-9 (open): `Vec.binary_search` on the v2 compiled
backend builds a fresh vector of the indices 0 to n - 1 on every call
and searches that, so each call costs O(n) instead of O(log n). The
bench program makes two searches per square over 2,000 edges, and
callgrind puts 64% of the `--mir` binary's instructions in that index
vector; it is why the v2 build is more than twice as slow as legacy
here. The kata keeps `binary_search` as written; the row records the
measurements.

Otherwise none. `karac check` passed all four arms, the harness, the
differential and the bench program, once the interval arm's calls
carried the call-site `mut` marker it asked for, `cut(mut ground,
right)`.
