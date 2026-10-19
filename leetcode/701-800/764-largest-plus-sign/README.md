# 764. Largest Plus Sign

An `n` x `n` grid holds 1 everywhere except at the cells listed in
`mines`, which hold 0. A plus sign of order k is a cell with k ones
running from it up, down, left and right, the cell itself included in
each. Return the order of the largest plus sign in the grid, or 0 if
there is none.

```
n = 5, mines = [[4, 2]]  ->  2
n = 1, mines = [[0, 0]]  ->  0
```

**Constraints:** 1 <= `n` <= 500; 1 <= `mines.length` <= 5000; the mines
are distinct cells of the grid.

## Approaches

| file | mechanism |
|---|---|
| `largest_plus_sign.kara` ★ | sweep each row and column both ways in one pass, counting the run of ones up to each cell, and keep each cell's smallest run, which is the order centred there; O(n^2) |
| `largest_plus_sign_grow.kara` | from each cell that is not a mine, grow the plus a step at a time while all four new ends are ones, skipping cells whose distance to the walls cannot beat the best so far; O(n^3) at worst |
| `largest_plus_sign_search.kara` | binary search on the order, since a plus holds one of every smaller order, testing whether an order fits anywhere with running counts of the mines along rows and columns; O(n^2 log n) |
| `largest_plus_sign_nearest.kara` | each row's and column's mines in sorted lists with the walls as mines; a cell's order is the distance to its nearest mine in any direction, found by binary search; O(n^2 log n) |
| `differential.kara` | the four arms against the definition, four properties |

Mines arrive as `Vec[Vec[i64]]`, as LeetCode gives them. Every arm
prints the same 9 lines: the two LeetCode examples; a 2 x 2 and two 3 x
3 grids, one with a corner mine and one with the centre mined; a 10 x
10 grid with one mine; a 4 x 4 grid whose four mines leave only plus
signs of order 1; a 500 x 500 grid with three mines; then 300 random
grids of up to 60 x 60 with up to a quarter of their cells mined, with
the orders' total and a checksum. `largest_plus_sign.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every cell and every order, checking each cell of the plus
against the list of mines. 1,500 random grids of up to 8 x 8 are checked
against it, and 300 of up to 40 x 40 against the other properties, each
with up to a third of its cells mined.

| | property |
|---|---|
| P1 | the answer is the definition's (the 1,500 small grids) |
| P2 | the grid turned a quarter turn has the same answer |
| P3 | one more mine, on a random free cell, never makes the answer larger |
| P4 | the grid inside a frame of mines, two cells wider, has the same answer |

It prints `1800 grids (orders adding up to 4476), 4 arms, 27600 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error; the total is the ★
arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the runs from below never applied | P1 394, P2 390 |
| M2 | ★: runs from the left carried through mines | P1 159, P2 374, P4 209 |
| M3 | ★: runs down a column reset at the row's mines | P1 177, P2 407 |
| M4 | growing: the right arm never checked | P1 151, P2 380, P4 204 |
| M5 | growing: the latest order kept, not the largest | P1 117, P2 269, P4 597 |
| M6 | growing: a cell skipped when it could beat the best by one | P1 623, P2 288, P3 18, P4 694 |
| M7 | search: an order above n / 2 never tried | P1 83, P4 98 |
| M8 | search: each row's stretch one short on the left | P1 94, P2 205, P4 186 |
| M9 | search: the last row of centres never tried | P1 218, P2 220, P4 256 |
| M10 | nearest: the distance to the mine on the left one too long | P1 254, P2 315 |
| M11 | nearest: the left wall taken as column 0 | P1 224, P2 256, P4 270 |
| M12 | nearest: the distance to the mine below one short | P1 359, P2 357 |
| E1 | ★: every cell started at 2n | 0 |
| E2 | growing: a cell tried when it could only tie the best | 0 |
| E3 | nearest: the search finding the first mine at or after the cell | 0 |

P1 kills all twelve. P3 sees only M6, 18 times: once cells that could
beat the best by one are skipped, the answer depends on what was found
first, so a mine that lowers an early cell's order can let a larger plus
through later. P2 misses M7 alone, which never tries an order above n /
2 and so errs the same way in the turned grid. P4 misses the edits that
err the same way at a mine as at a wall, M1, M3, M10 and M12; it sees
M11, which takes the left wall for column 0, because in the framed grid
column 0 holds a mine anyway. E1 starts every cell at 2n, but any start
no smaller than the longest run will do; E2 also tries cells that could
only tie the best, which costs time and changes nothing; E3's search
finds a mine on the cell itself as the nearest on its right, at distance
0, so a mined cell gets order 0 rather than being skipped.

## Verification

Every arm prints the same output as `largest_plus_sign.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a62eacd307`, whose last compiler change is `7d736aae75`. This paragraph
said the runtime archives were built after the last runtime change,
`b09cd37112`; in fact they predated a later one, `176f59738b`, which
changed only the order in which the runtime's merge sort makes its
merges, so it could not change any result here. Every arm and the
differential were checked again at kara `8a2af7d554`, whose last
compiler change is `60d9973e03`, with the archives rebuilt after
`176f59738b`: each prints the same under `karac __mir-llvm-run` and
`karac __mir-llvm-asan` with no error, and the bench program built by
`karac build --mir` prints the same line. The timings below are from the
earlier build.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the growing, search and nearest-mine
arms: each prints the same output under `karac run`, `karac build` and
an auto-par build, and the first two under the legacy interpreter too;
the nearest-mine arm ran past the check's 60 s limit under the legacy
interpreter of the debug build. They refuse the ★ arm, the differential
and the bench at a `*` over an element of `iter()` (`best.max(*order)`),
which legacy gives by value where v2 gives references. The legacy
timings below are of a copy of the bench that writes `order` for
`*order`, and that also reads each cell into a local before calling
`min` on it, since legacy's code generator defers a method call on a
doubly indexed receiver (`grid[i][j].min(left)`); the copy prints the
same line. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages, on 300 random
grids of 500 x 500 with 5,000 mines each, the most LeetCode allows,
adding up the orders and a checksum. Every implementation prints
`300 grids of 500 x 500 with 5000 mines: orders adding up to
41446, checksum 81897763`, the Kāra program under `karac __mir-run`
included (in 329 s). The mines are drawn afresh for each grid, rejecting
cells already taken, as part of the timed work; C keeps the grid in a
static array, where the others allocate a vector of rows for each grid.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.68 to 0.79 s |
| Rust (`rustc -O`) | 0.59 to 0.74 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.67 to 0.82 s |
| Go | 1.37 to 1.50 s |
| Python | 44.3 to 46.0 s |
| Kāra (`karac build --mir`) | 0.74 to 0.87 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
4.3 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.77 s,
against C's 0.78, Rust's 0.65 (0.74 under overflow checks) and Go's
1.41. Under valgrind's cachegrind v2 runs 8.6 billion instructions, Rust
5.4 billion and C 3.2 billion, but C mispredicts 45 million branches to
Rust's 0.7 million and v2's 11 million; C's `if` on each minimum
presumably compiles to a branch where `min` compiles to a conditional
move (inferred, not profiled). The legacy build of the copy ran 0.45 to
0.51 s, a median of 0.47 s in the interleaved runs, so v2 takes
1.6 times as long as legacy, inside M2's limit of twice legacy; new
katas' benches are outside M2's frozen set in any case. The comparison
with C and Rust waits until after M4.

## Compiler findings

None new.
