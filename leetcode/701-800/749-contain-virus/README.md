# 749. Contain Virus

A virus spreads on an m x n grid, where `isInfected[i][j]` is 1 for an
infected cell and 0 for a clean one. Each day one wall can be built
around one region (a group of infected cells joined by sides): the
region that threatens the most clean cells, a wall on every side it
shares with a clean cell. Then every other region infects all the clean
cells next to it. Return the number of walls used when no region
threatens a clean cell. LeetCode promises that no two regions ever tie
for the most threatened cells.

```
isInfected = [[0,1,0,0,0,0,0,1],
              [0,1,0,0,0,0,0,1],
              [0,0,0,0,0,0,0,1],
              [0,0,0,0,0,0,0,0]]               ->  10
isInfected = [[1,1,1],[1,0,1],[1,1,1]]         ->   4
isInfected = [[1,1,1,0,0,0,0,0,0],
              [1,0,1,0,1,1,1,1,1],
              [1,1,1,0,0,0,0,0,0]]             ->  13
```

**Constraints:** 1 <= m, n <= 50; every cell is 0 or 1; there is never a
tie.

## Approaches

Every arm simulates the days as stated; they differ in how they find the
regions and count what each threatens. On a tie, which random grids do
have, every arm walls the region whose first cell comes first in reading
order.

| file | mechanism |
|---|---|
| `contain_virus.kara` ★ | each day, flood-fill the regions with a stack over the grid flattened to one `Vec`, counting each region's walls and, with a mark per cell, its threatened cells once each; O(days x m x n) |
| `contain_virus_sets.kara` | the same day on the grid as rows, each region found breadth-first from a `VecDeque` and its threatened cells gathered in a `Set[(i64, i64)]` |
| `contain_virus_unionfind.kara` | join the infected cells in a disjoint-set forest, then count from each clean cell's side: a wall for each infected neighbour's set and a threatened cell for each distinct set among its neighbours |
| `contain_virus_recur.kara` | a recursive depth-first search for each region, collecting the clean cells it touches with repeats, one for each side, then sorting them and removing the repeats |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 15 lines: the three LeetCode examples; a
single clean cell, a single infected one, and the two side by side; a
grid with every cell infected; infected opposite corners, which tie on
the first day; a checkerboard; one infected cell in the middle; random
50 x 50 grids with 1%, 3%, 10% and 30% of their cells infected; and
300 random grids of up to 8 x 8, with the total of their walls and a
checksum. `contain_virus.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which runs the days with nothing shared with the arms: every infected
cell starts labelled with its place in reading order and labels fall to
the least among infected neighbours until none changes, each region's
threat is counted by asking every clean cell whether it touches the
region, and the cells to infect are found the same way. 3,000 random
grids are checked, each of 1 to 6 rows of 1 to 6 cells, every cell
infected with a chance of 5 to 50 in 100; their walls total 17,147. The
definition also notes whether any day had a tie, and 2,444 grids have
none. P2 to P4 change reading order, which breaks a tie, so they are
checked on those 2,444 only.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the grid transposed gives the same answer |
| P3 | every row reversed gives the same answer |
| P4 | the grid turned half round gives the same answer |

It prints `3000 grids (2444 with no tie, walls 17147 in all), 4 arms,
41328 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: walls counted once a cell, not once a side | P1 1323 |
| M2 | ★: a tie going to the later region | P1 295 |
| M3 | ★: the second row never looking up | P1 1110, P2 1058, P3 14, P4 1037 |
| M4 | sets: the walled region left clean, not walled off | P1 1124, P2 6, P3 1, P4 15 |
| M5 | sets: a diagonal in place of the right-hand neighbour | P1 1384, P2 1350, P3 1010, P4 1138 |
| M6 | sets: only the first day's walls | P1 1319 |
| M7 | unionfind: never joined to the cell below | P1 1244, P2 737, P3 24, P4 321 |
| M8 | unionfind: a cell threatened once for each side | P1 75, P2 13, P3 2, P4 25 |
| M9 | unionfind: a tie going to the later region | P1 295 |
| M10 | recur: repeats not removed from the threatened cells | P1 75, P2 13, P3 2, P4 25 |
| M11 | recur: the search never stepping left | P1 1768, P2 1363, P3 1248, P4 1238 |
| M12 | recur: every region infecting the walled region's cells | P1 1203, P2 81, P3 37, P4 180 |
| E1 | ★: a different mark for an unmarked cell | 0 |
| E2 | unionfind: union always under the first root | 0 |
| E3 | recur: the threatened cells in falling order | 0 |

P1 kills all twelve. M2 and M9 are one mistake in two arms, sending a
tie to the later region, and fail exactly the same checks, all under
P1: P2 to P4 are checked only on grids with no tie, where the tie rule
never acts. M8 and M10 are likewise one mistake, counting a threatened
cell once for each side it shares with a region, and fail the same
checks. M1 and M6 get the walls wrong in a way that does not depend on
direction, so the grid's symmetries cannot see them and only P1 does.
M3, M5, M7 and M11 each mishandle one direction, a row that never looks
up, a diagonal for a side, a join never made downwards, a search that
never steps left, so transposing, mirroring or turning the grid changes
their answer and P2 to P4 see them all. M4 and M12 spread the virus
wrongly; P2 to P4 see them only a little, presumably on grids where the
wrong spread makes a tie that reading order then breaks (inferred, not
traced). E1 marks unmarked cells with another value that is never a
region's number; E2 joins the sets the other way round, which leaves the
same sets; E3 infects the threatened cells in another order, all on the
same day.

## Verification

Every arm prints the same output as `contain_virus.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`1a5c083e3a`, whose last compiler change is `4655692faa`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking, at a `*` over a vector's `iter()`
(`*x` over a region's cells, and `*r`, `*c` over pairs), since legacy
gives those by value where v2 gives references. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes a 50 x
50 grid with each cell infected with a chance of 5 in 100 once, and in
each of 3,000 rounds draws 20 random cells afresh with the same chance
and contains the virus. Every implementation prints `3000 grids of 50 x
50: 2632174 walls in all, checksum 257958783`, the Kāra program under
`karac __mir-run` included (in 162 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.19 to 0.25 s |
| Rust (`rustc -O`) | 0.80 to 0.93 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.76 to 0.90 s |
| Go | 2.14 to 2.34 s |
| Python | 7.8 to 7.9 s |
| Kāra (`karac build --mir`) | 0.85 to 0.99 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 3.9 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.89 s,
level with Rust (0.86, or 0.79 under overflow checks), against C's
0.23 and Go's 2.25. The C program keeps each day's regions packed in
fixed arrays, where the Kāra, Rust and Go programs, like the arm, make
fresh vectors for each day and region: under valgrind's cachegrind
v2 runs 9.4 billion instructions, Rust 8.2 billion and C 2.5 billion.
The legacy backends refuse the program. To have a legacy time at all,
the bench was copied for legacy alone with `*x` written `x` in its
`iter()` loops: the legacy build of that copy ran 0.65 to 0.75 s, a
median of 0.67 s in the interleaved runs, so v2 takes about 1.3 times as
long as legacy, inside M2's limit of twice legacy. That copy is a
measurement only and is not in the kata, and new katas' benches are
outside M2's frozen set in any case. The comparison with C and Rust
waits until after M4.

## Compiler findings

None new.
