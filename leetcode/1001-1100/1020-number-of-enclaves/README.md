# 1020. Number of Enclaves

Given an `m x n` binary grid, where 0 is sea and 1 is land, a move walks
from a land cell to a land cell next to it up, down, left or right, or
off the grid from a land cell on its border. Return the number of land
cells from which no number of moves can walk off the grid.

```
grid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]  ->  3
grid = [[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]]  ->  0
```

**Constraints:** `1 <= m, n <= 500`, each `grid[i][j]` is 0 or 1.

## Approaches

A land cell can walk off exactly when its island, the land joined to it,
touches the border. The arms differ in how they find that land.

| file | mechanism |
|---|---|
| `enclaves.kara` ★ | sinking the coast: turn every border land cell to sea and flood on from them over land with a stack, sinking what it reaches; the land left is the enclaves. O(mn) |
| `enclaves_bfs.kara` | from the border inwards: count the land, then search breadth first from all border land cells at once over a queue, marking what it reaches; the enclaves are the land less the cells reached. O(mn) |
| `enclaves_union.kara` | union-find with the outside: a set for each cell and one for the outside of the grid, each land cell joined to its land neighbours below and to the right and each border land cell to the outside, with path compression and union by size; the enclaves are the land cells whose set is not the outside's. O(mn α(mn)) |
| `enclaves_islands.kara` | island by island: visit each island once from its first cell with a stack, counting its cells and noting whether any is on the border, and add the size of each island that is not. O(mn) |
| `enclaves_recursive.kara` | recursive sinking: the ★ arm's flood as a recursive search, sinking each border land cell and recursing into its four neighbours. O(mn), recursion as deep as the search's longest path through an island |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers for seven grids,
LeetCode's two examples among them; for six groups of random grids (4x4
to 60x80, with land at each cell with probability 3/8 to 6/8), the
enclaves in all, the most in one grid and a checksum; and a 61x61 grid
of nested rings, each joined to the next by one cell, inside a border
of sea, so one winding island of 1,814 cells, all enclaves.
`enclaves.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: from each land cell, a search of the land it can walk to for
a border cell. It checks 4,315 grids: every grid of at most 9 cells
(3,210), 500 random grids of 4x4 to 5x5, 600 of 1x1 to 15x15 and 5 of
40x40, with land at each cell with probability 2/8 to 6/8. Each grid is
also asked turned on its side, upside down, inside a ring of sea and
inside a ring of land.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the same answer for the grid turned on its side and upside down |
| P3 | no more than the land off the border, and none when every cell is on the border |
| P4 | inside a ring of sea every land cell is an enclave |
| P5 | inside a ring of land the answer does not change: the old border land joins the new border |
| P6 | each arm agrees with at least two of the other four |

The differential prints `4315 grids: checksum 428452622, 129450 checks
over 5 arms: 0 failures` under `karac __mir-run` (15 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last column not on the border | P1 422, P2 609, P3 188, P5 422, P6 422 |
| M2 | ★: border land pushed but not sunk itself | P1 2875, P3 2322, P5 2875, P6 2875 |
| M3 | ★: every cell counted, sea too | P1 4315, P3 4315, P4 4315, P5 4315, P6 4315 |
| M4 | bfs: a step down queued without marking it | P1 675, P2 859, P3 577, P5 3396, P6 675 |
| M5 | bfs: only the top and bottom rows as sources | P1 1538, P2 2640, P3 1271, P5 1538, P6 1538 |
| M6 | bfs: the first source never expanded | P1 75, P2 160, P5 75, P6 75 |
| M7 | union: the cell, not its root, attached | P1 234, P2 330, P5 191, P6 234 |
| M8 | union: compared with the outside node, not its set's root | P1 4283, P3 4283, P5 4315, P6 4283 |
| M9 | union: sea cells joined too | P1 379, P2 173, P4 4233, P5 165, P6 379 |
| M10 | islands: the coastal islands counted instead | P1 4264, P3 4183, P4 4286, P5 4315, P6 4264 |
| M11 | islands: the first column not coast | P1 435, P2 610, P3 195, P5 435, P6 435 |
| M12 | islands: an island's first cell not marked, so counted twice | P1 201, P3 41, P4 3597, P6 201 |
| M13 | recursive: one column past the edge | index out of bounds panic, exit 101 |
| M14 | recursive: the row above the last sunk instead of the last | P1 379, P2 757, P3 116, P4 3530, P5 379, P6 379 |
| M15 | recursive: the top row never sunk | P1 3515, P2 4107, P3 2796, P5 4313, P6 3515 |

P1 and P6 kill the fourteen that finish, P5 thirteen, P3 eleven, P2
nine and P4 five; M13 is killed by its bounds check. P2 catches the
edits that treat one side of the grid apart from the others, since
turning the grid moves that side. M8 is right only when no land touches
the border, which leaves the outside node its own root; so P4, whose
ring of sea keeps all land off the border, never sees it, and P5, whose
ring of land always touches it, fails on every grid. The checks draw no
random number that depends on an answer, so every mutant sees the same
grids and their counts can be compared.

Fifteen other edits were tried and set aside, none of them equivalent.
Four failed exactly the same checks as a kept one: bfs, union and
recursive leaving the last column off the border (as M1), and recursive
counting every cell (as M3). The other eleven were killed too, beyond
three per arm: ★ with no step to the left, a diagonal step in its
place, and no spreading into the row above the last; bfs and recursive
with no step up, which fail alike; bfs queueing the wrong cell on a
step left, which panics out of bounds; union never joining downwards,
and counting sea; islands with no step to the left; and islands
counting each island as one cell, or counting islands instead of cells,
which fail alike and as M12 does on P1 and P4, without its P3.

## Verification

Every arm prints the same output as `enclaves.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error; the differential prints its line under all three. `karac
check --output=json` reports no diagnostic for the five arms, the
differential and the bench program, so `karac fix` had nothing to do.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. The release build is kara `56c60bdf7c`, with
runtime archives rebuilt at `ce706dd131`, the last commit before it to
change the runtime. Under `karac __mir-run` the arms take 1.4 s (bfs) to 2.9 s (recursive).
No compiler gap turned up.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench builds 100 random grids of 1 to 500 rows and columns
(LeetCode's sizes, 6,129,943 cells in all), with land at each cell with
probability 2/8 to 6/8, once in all five languages, and runs the ★ arm
on each grid 20 times, folding the answers into a sum and a checksum:
each run copies the grid, floods it from the border with a stack and
sums what is left. C keeps each grid as an array of row pointers, the
others as a vector of row vectors. Every implementation prints `100
grids, 6129943 cells, 20 rounds: 27147360 enclaves, checksum
777835003`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.829 to 0.898 s | 0.859 s |
| Rust (`rustc -O`) | 0.860 to 1.138 s | 0.984 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.919 to 1.124 s | 1.027 s |
| Go | 1.661 to 1.811 s | 1.707 s |
| Python | 33.3 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.860 to 1.091 s | 0.946 s |
| Kāra (`karac build`) | 0.890 to 1.127 s | 0.921 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 0.92 times Rust's median time under overflow checks and 1.10
times C's. The times include building the grids, about 6 million
random numbers, once. C spends about a fifth of its time in the
system (user 0.67 s of 0.86 s real); we did not measure where that
time or the gaps between the languages go.
