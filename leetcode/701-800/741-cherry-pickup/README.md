# 741. Cherry Pickup

An `n x n` grid holds in each cell 0 (empty), 1 (a cherry) or -1 (a
thorn that blocks the way). Start at `(0, 0)`, walk to `(n - 1, n -
1)` moving only right or down through cells that are not thorns, then
walk back to `(0, 0)` moving only left or up. Passing a cell with a
cherry picks it, and the cell becomes empty. Return the most cherries
that can be picked, or 0 when there is no way through.

```
grid = [[0, 1, -1], [1, 0, -1], [1, 1, 1]]   ->  5
grid = [[1, 1, -1], [1, -1, 1], [-1, 1, 1]]  ->  0
```

**Constraints:** 1 <= `n` <= 50; each cell is -1, 0 or 1; `grid[0][0] !=
-1` and `grid[n - 1][n - 1] != -1`.

## Approaches

Picking the best way there and then the best way back fails, since the
first walk can take the cherries the second needed. Instead, the way
back walked backwards is a second way there, so the trip is two walkers
going from the near corner to the far one at once, one step each at a
time, a cherry on a cell they both reach counted once. Since they move
in step, after `k` steps both are on the diagonal of cells whose row and
column sum to `k`, and a state is just the pair of rows.

| file | mechanism |
|---|---|
| `cherry_pickup.kara` ★ | keep the best cherries for every pair of rows after `k` steps in an `n x n` table of `Vec`s, and build each next layer from the four ways the walkers can have stepped; O(n^3) time, two layers of space |
| `cherry_pickup_memo.kara` | the same states solved from the start, recursively: the best from a pair of cells to the far corner is what they hold plus the best of the four ways on, each answer remembered by step and rows in a flat `Vec` |
| `cherry_pickup_ordered.kara` | the walkers are interchangeable, so keep only pairs with the first walker's row no greater than the second's in a flat table, folding a predecessor pair into that order; about half the states |
| `cherry_pickup_twice.kara` | no step count: a plain four-dimensional table over both walkers' coordinates, filled in order of the coordinate sum and kept only where the sums agree; n^4 entries, 6.25 million for n = 50 |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the two LeetCode examples; one cell
with a cherry and one without; a 3 x 3 grid of cherries, of which two
ways can pick 8; a grid with only one way through; a 4 x 4 grid with
thorns on the diagonal; a 2 x 2 grid with no way through; a 50 x
50 random grid with a thorn in about one cell in 10; a 50 x 50 grid of
cherries; and 300 random grids up to 6 x 6, with the cherries in all and
a checksum. `cherry_pickup.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which lists every way from the near corner to the far one by steps right
and down that avoids the thorns, tries every pair of them as the way
there and the way back reversed, and counts the cherries on either once.
3,000 random grids are checked, from 1 x 1 to 5 x 5, with a thorn in
about one cell in 2 to 6 and a cherry in about half the rest, the
corners never thorns; 589 of them have no way through, and the best
trips pick 7,830 cherries in all.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the grid turned about its main diagonal gives the same answer |
| P3 | the grid turned half way round, so that the way there is the way back, gives the same answer |
| P4 | one cell that is not a thorn changed from cherry to empty costs at most one cherry, and from empty to cherry gains at most one |

It prints `3000 grids (589 with no way through, 7830 cherries in all),
4 arms, 48000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a shared cell's cherry counted twice | P1 1586, P3 907, P4 746 |
| M2 | ★: the walkers always stepping the same way | P1 874 |
| M3 | ★: an unreachable pair treated as reachable | P1 271, P3 424 |
| M4 | memo: done when the first walker reaches the last row | P1 380, P2 590, P3 701 |
| M5 | memo: a dead end counted as a way through | P1 259, P3 424 |
| M6 | memo: answers remembered without the step count | P1 686, P2 727, P3 716 |
| M7 | ordered: a shared cell's cherry counted twice | P1 1586, P3 907, P4 746 |
| M8 | ordered: the second walker's cherry read from the first's row | P1 732, P2 605, P3 848, P4 224 |
| M9 | ordered: the walkers never on one cell | P1 1742 |
| M10 | twice: the first cell's cherry lost | P1 1179, P3 907 |
| M11 | twice: the second walker's coordinates swapped | P1 505 |
| M12 | twice: the first walker only stepping right | P1 1742 |
| E1 | twice: a shared cell told by its column, not its row | 0 |
| E2 | memo: a table one step longer | 0 |
| E3 | ordered: a move that crosses the walkers not folded back | 0 |

P1 kills all twelve. M1 and M7 are one mistake in two arms, a shared
cell's cherry counted twice, and fail the same checks. M9 and M12 lose
the far corner itself, since the walkers can then never meet there, so
every answer is 0 and both fail the 1742 checks with a cherry on some
way through. P3 sees the edits that treat the two walkers or the two
ends unalike: a shared cherry counted twice is counted at a different
place when the grid turns round, M3 and M5 count a blocked way, which
the turned grid blocks at the other end, M4 stops when the first walker
reaches the last row, M10 loses the first cell's cherry, which turning
moves to the last cell, and M6 and M8 go wrong in ways that depend on
where in the grid a cell lies. P2 sees M4, M6 and M8, which treat rows
and columns unalike. P4 sees M1, M7 and M8, under which one cherry can
be counted twice, so that one cherry more or less moves the answer by
two. E1 tells a shared cell by its column rather than its row, which on
one diagonal is the same test; E2 makes the memo table one step longer,
an entry never used; E3 drops the fold that puts a predecessor pair in
order, and changes nothing, because the only pair a move can cross comes
from walkers on one cell, and the other walker's move reaches the same
ordered pair.

## Verification

Every arm prints the same output as `cherry_pickup.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`1d96cab833`, whose last compiler change is `afe886a96d`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms and the bench program.
Every arm prints the same output under the legacy `karac run` and `karac
build`, and under `KARAC_AUTO_PAR=1`; under the legacy interpreter the ★
and ordered arms do too, while the memo and twice arms print the right
lines but are still on the 50 x 50 grids when the 60 s limit stops them.
The legacy backends refuse the differential at type checking, at a `*`
over a vector's `iter()` (`*cell` over a path's cells), since legacy
gives those by value where v2 gives references. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes a 50 x
50 grid once, with a thorn in about one cell in 10 and a cherry in about
half the rest, and in each of 300 rounds changes 5 random cells other
than the corners to a thorn, a cherry or nothing and finds the most
cherries again. Each call builds every layer afresh as a table of rows,
as the ★ arm does, which in C is an array of row pointers allocated row
by row. Every implementation prints `300 rounds of a 50 by 50 grid:
47867 cherries in all`, the Kāra program under `karac __mir-run`
included (in 56 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.09 to 0.11 s |
| Rust (`rustc -O`) | 0.40 to 0.52 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.41 to 0.57 s |
| Go | 1.11 to 1.24 s |
| Python | 10.8 to 11.8 s |
| Kāra (`karac build --mir`) | 0.41 to 0.45 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
2.8 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is level with Rust at the medians of the interleaved
runs (0.44 s against 0.44), a seventh ahead of Rust under overflow
checks (0.51) and well ahead of Go (1.19), but four times as slow as C
(0.10). Under valgrind's cachegrind it runs 4.9 billion instructions
against C's 1.6 and Rust's 6.7, and 1.08 billion branches against
0.24 and 1.18. The legacy build of the same program ran 0.22 to 0.28 s
in the interleaved runs, a median of 0.25 s, so v2 takes 1.8 times as
long as legacy here, inside M2's limit of twice legacy; new katas'
benches are outside M2's frozen set in any case. Legacy runs 2.8 billion
instructions and 0.66 billion branches. Where v2's extra instructions
over legacy go was not traced. The comparison with C and Rust waits
until after M4.

## Compiler findings

None new.
