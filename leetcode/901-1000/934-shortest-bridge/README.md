# 934. Shortest Bridge

You are given an `n x n` binary matrix `grid` where `1` represents land
and `0` represents water.

An **island** is a 4-directionally connected group of `1`'s not
connected to any other `1`'s. There are **exactly two islands** in
`grid`.

You may change `0`'s to `1`'s to connect the two islands to form **one
island**.

Return the smallest number of `0`'s you must flip to connect the two
islands.

```
grid = [[0,1],[1,0]]                                  ->  1
grid = [[0,1,0],[0,0,0],[0,0,1]]                      ->  2
grid = [[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],
        [1,0,0,0,1],[1,1,1,1,1]]                      ->  1
```

**Constraints:** `n == grid.length == grid[i].length`;
`2 <= n <= 100`; `grid[i][j]` is either `0` or `1`; there are exactly
two islands in `grid`.

## Approaches

| file | mechanism |
|---|---|
| `shortest_bridge.kara` ★ | the first island walked depth first with a stack, every cell at distance 0, then a breadth-first search outward from all of them at once; the first cell of the other island reached ends it, and the distance of the cell it was reached from is the answer. O(n²) |
| `shortest_bridge_pairs.kara` | the least Manhattan distance between a cell of each island, less one, since a staircase path between the closest pair crosses only water; only shore cells, with water beside them, are paired. O(n² + ab) for shores of `a` and `b` cells |
| `shortest_bridge_zero_one.kara` | a 0-1 breadth-first search with a `VecDeque` from one cell of the first island, entering land costing 0 and water 1; the least cost of a land cell above 0 is the answer. O(n²) |
| `shortest_bridge_grow.kara` | the first island painted 2, then the whole grid scanned once a ring: water beside a cell painted `k` is painted `k + 1`, until a cell painted `k` touches the other island, `k - 2` rings out. O(n²) a ring |
| `shortest_bridge_both.kara` | both islands spread at once from every land cell, each water cell taking the label and distance of the cell that reached it first; the least sum of distances across two neighbouring cells with different labels is the answer. O(n²) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (two strips three rows apart, opposite corners, and a ring with
one cell at its centre); for 300 random grids of 2 to 60 rows, each with
two islands grown at random, the answers' sum and a checksum; and three
of LeetCode's largest, 100 x 100: single cells in opposite corners
(197), two halves split by one column of water (1), and two random
islands of up to 2,000 cells. A random grid grows each island from a
random cell, one random neighbour of a random cell at a time, the second
never beside the first. `shortest_bridge.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of `k` water cells, for `k` from 0 up, flipped in
turn until the grid holds one island. It checks 3,200 random grids:
3,000 of 2 to 5 rows against the statement, and 200 of 2 to 32 rows
against the other properties; 111,317 cells in all.

| | property |
|---|---|
| P1 | the statement's answer, on the small grids |
| P2 | from 1 to the gap between the islands' first cells in reading order, and 1 exactly when some water cell touches both islands |
| P3 | the same answer a quarter turn round |
| P4 | the same answer with a ring of water around the grid |
| P5 | when no water cell touches both islands, the first island grown by the water cells beside it takes one 0 fewer; when one does, the answer is 1 |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 grids, 111317 cells, answers summing to 4315, 95000
checks over 5 arms: 0 failures` under `karac __mir-run` (33 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

P5 first chose between its two halves by the arm's own answer, growing
the island whenever the arm answered more than 1. A mutant answering 2
for a grid whose answer is 1 then handed every arm a grid of one island,
and the grow arm, which stops only on reaching the other island, never
returned. P5 now chooses by whether a water cell touches both islands,
which the differential finds for itself, so every grid an arm sees has
two islands.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: water marked with the first island | P1 3000, P2 3200, P5 3200, P6 3200 |
| M2 | ★: each ring of water counted twice | P1 3000, P2 3072, P5 3200, P6 3200 |
| M3 | ★: the starting cell at distance 1 | P1 1814, P2 1788, P3 926, P5 1747, P6 1829 |
| M4 | pairs: the least distance itself | P1 3000, P2 3009, P5 2695, P6 3200 |
| M5 | pairs: the shore taken as cells beside land | P1 1869, P2 1895, P4 1895, P5 1895, P6 1895 |
| M6 | pairs: the column difference not made positive | P1 1748, P2 1871, P3 3188, P4 42, P5 1653, P6 1880 |
| M7 | zero_one: land cells cost 1 too | P1 1579, P2 1653, P3 458, P5 1683, P6 1683 |
| M8 | zero_one: the starting cell at cost 1 | P1 407, P2 505, P5 505, P6 505 |
| M9 | zero_one: the last row never searched | P1 1468, P2 1472, P3 909, P4 1476, P5 1472, P6 1476 |
| M10 | grow: one ring too many | P1 3000, P2 2880, P5 2695, P6 3200 |
| M11 | grow: only the starting cell painted 2 | P1 1667, P2 1856, P3 458, P5 2022, P6 1856 |
| M12 | grow: cells painted later in the same scan grown at once | P1 2909, P2 3076, P3 411, P5 3001, P6 3100 |
| M13 | both: one more on each bridge | P1 382, P2 375, P3 793, P5 369, P6 403 |
| M14 | both: the last two rows never compared | P1 207, P2 207, P3 392, P4 207, P5 223, P6 207 |
| M15 | both: neighbours to the right never compared | P1 445, P2 453, P3 962, P4 178, P5 471, P6 484 |

P1, P2, P5 and P6 kill all fifteen, P3 nine and P4 five. P3 misses the
six whose mistakes do not depend on which way the grid faces: an answer
off by a fixed amount or doubled (M2, M4, M10), every cell of water
joined to the first island (M1), M8, which answers 1 for every grid
since the first island's own cells then cost 1, and M5, whose shores
come out empty for single-cell islands in any orientation. P4 kills the
five tied to the grid's edge or size: the last row or rows (M9, M14),
right-hand neighbours (M15), M5, whose answer when it finds no shore
at all is `2n - 1`, which the extra ring changes, and M6, for which the
ring makes the cells along the old edge shore cells, some of which pair
closer once the sign of the column difference is lost. M13 adds 1 only
across neighbours one above the other, so it is wrong only when every
shortest bridge changes label vertically.

Eight other edits were tried and set aside. Two failed exactly the same
checks as a kept mutant: ★ answering one more than the distance reached,
as M10, and zero_one counting the first island as the other, as M1.
Three were sound but beyond three an arm (pairs leaving shore cells in
the first row out, both giving the other island the first label, and
both counting each step of water twice). Three, all in grow, ran past
the 200 s limit: painting new cells with the ring being grown, which
leaves the next ring empty so the scan never ends; and never growing
from the first row or into the last column, which ran under the first
version of P5 and can stall the same way when the cells left to grow
from all sit in the skipped row or column.

## Verification

Every arm prints the same output as `shortest_bridge.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 1.7 to 3.1 s each and the
differential 33 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The ★, zero_one, grow and both arms print the same output under the
frozen legacy interpreter, the legacy JIT and both legacy builds, with
and without auto-par. Legacy refuses the pairs arm and the differential
at the first `*` on an element of a `Vec[i64]`'s `.iter()` ("unary '*'
requires 'ref T', ... found 'i64'"), legacy's older rule; under v2 the
element is a reference and the `*` is required. It refuses the bench
program at `shortest_bridge(grids[(r + i) % count])`, a move out of an
index ("cannot move ... out of an index"), which v2's borrowing
parameters make a borrow. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program builds 100 grids of 100 x 100 once, LeetCode's
largest, each with two islands of up to 2,500 cells grown at random as
in the harness, and in each of 50 rounds runs the ★ arm on every grid,
each round starting from a different one. Every implementation prints
`50 rounds over 100 grids of 100 x 100: answers summing to 153500,
checksum 606801423`. C keeps each grid in one block read row by row and
its stack and queue in arrays of `n * n`; the others keep a grid as rows
and grow their stacks and queues.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.23 to 0.27 s | 0.24 s |
| Rust (`rustc -O`) | 0.22 to 0.26 s | 0.24 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.23 to 0.28 s | 0.24 s |
| Go | 0.48 to 0.53 s | 0.50 s |
| Python | 16.5 s | |
| Kāra (`karac build --mir`) | 0.36 to 0.40 s | 0.39 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 68 times C's.

v2 takes 1.61 times Rust's median time under overflow checks and 1.61
times C's. Under valgrind's cachegrind v2 runs 4.93 billion
instructions and 1.46 billion branches with 34.1 million mispredicted,
Rust with overflow checks 2.82 billion, 1.02 billion and 9.30 million,
and C 1.65 billion, 0.70 billion and 8.14 million. v2 mispredicts 3.7
times as often as Rust; that its bounds checks on the four-way
neighbour tests are compiled as separate branches where Rust's fold
into fewer, and that this is most of the gap, is inferred, not
profiled.
