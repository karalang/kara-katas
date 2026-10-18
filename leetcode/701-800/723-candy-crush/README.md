# 723. Candy Crush

Given an m x n integer array `board` where `board[i][j]` is the type of
candy in a cell and 0 an empty cell, restore the board to a stable
state. If three or more candies of the same type are adjacent in a row
or a column, crush them all at the same time, leaving their cells empty.
Then every candy above an empty cell drops until it lands on a candy or
the bottom, all at the same time, and no new candies enter from the top.
Repeat while any candies can be crushed, and return the stable board.

```
board = [[1, 3, 5, 5, 2], [3, 4, 3, 3, 1], [3, 2, 4, 5, 2], [2, 4, 4, 5, 5], [1, 4, 4, 1, 1]]
     ->  [[1, 3, 0, 0, 0], [3, 4, 0, 5, 2], [3, 2, 0, 3, 1], [2, 4, 0, 5, 2], [1, 4, 3, 1, 1]]
```

**Constraints:** 3 <= m, n <= 50; 1 <= `board[i][j]` <= 2000.

## Approaches

Each arm runs the same rounds, finding every run, crushing them all and
dropping the columns, and differs in how it marks the crushed cells and
how it drops.

| file | mechanism |
|---|---|
| `candy_crush.kara` ★ | each cell and the two after it, across and down, tested on absolute values, a run's cells marked by turning them negative so overlapping runs still see them; each column then copied down from the bottom, keeping only the positive cells; O((m * n)^2) at worst, since every round crushes at least three candies |
| `candy_crush_mask.kara` | the same windows marked in a separate grid of flags, and each column dropped in one pass from the bottom, moving each survivor down by the number of crushed and empty cells below it |
| `candy_crush_runs.kara` | each row and column cut into maximal runs of one candy and every run of three or more marked whole; each column's survivors gathered into a list and written back at the bottom |
| `candy_crush_columns.kara` | the board kept as columns, each a list of its candies from the bottom up with no empty cells, so a drop is only removing entries; a candy's neighbours across sit at the same height in the columns beside it; the board rebuilt at the end |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: the two LeetCode examples; a board
with no run and a board of one kind; a run across and a run down sharing
a corner; runs of five and four across; a chain reaction, where a candy
dropped by one crush completes a run on the bottom row; three runs down
side by side; three random boards of 50 x 50, the problem's largest, of
3, 4 and 5 kinds, each with its empty cells and a checksum; and
300 random boards of 3 to 8 rows and columns with a checksum.
`candy_crush.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which marks no runs: each round it asks of every cell whether any window
of three across or down that holds it has three equal candies, empties
those cells together, then swaps any candy above an empty cell down one
step at a time until none is. 3,000 random boards are checked, each of
3 to 7 rows and columns of 1 to 4 kinds, so overlapping runs and chain
reactions are common; 2,709 of them crush something.

| | property |
|---|---|
| P1 | the board is the definition's |
| P2 | the board mirrored left to right gives the result mirrored |
| P3 | every candy renamed, v to 10 * v + 3, gives the result renamed |
| P4 | the result is settled, with no candy above an empty cell, and crushing it again changes nothing |

It prints `3000 boards (2709 with a crush), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run of four across losing its last candy | P1 608, P2 661 |
| M2 | ★: the third candy of a run across left standing | P1 1525, P2 1628 |
| M3 | ★: a run down ending on the bottom row missed | P1 1107 |
| M4 | mask: a run across in the last three columns missed | P1 1076, P2 1238 |
| M5 | mask: the third candy of a run down left standing | P1 1470 |
| M6 | mask: the survivors not moved down, the top cells emptied anyway | P1 1631 |
| M7 | runs: only runs of four or more across crushed | P1 1504 |
| M8 | runs: a run down cut off at the bottom row | P1 1107 |
| M9 | runs: the survivors stacked from the top | P1 2165, P4 2236 |
| M10 | columns: a run down at the top of a column missed | P1 1072 |
| M11 | columns: two candies across taken for three | P1 2041, P2 2167 |
| M12 | columns: the board rebuilt upside down | P1 2236, P4 2236 |
| E1 | mask: an empty cell told by <= 0 | 0 |
| E2 | runs: a run's candy tested > 0 instead of != 0 | 0 |
| E3 | mask: the window across tested as c < n - 2 | 0 |

P1 kills all twelve, and six of them only P1 sees. P2 sees only the four
that treat a run across unevenly from left to right, M1, M2, M4 and
M11; a mistake about runs down, or one even from left to right like M7's
runs of four, mirrors with the board. P3 sees none: every arm compares
candies only for equality, so renaming them cannot change what an edit
does, and P3 is there to show that the arms do not depend on the values
themselves. P4 sees M9 and M12, which leave candies above empty cells.
M6 leaves the survivors where they are but empties the top cells all the
same, and the board it leaves passes P4. M3 and M8 fail the same boards,
both missing a run down that ends on the bottom row. Three earlier
choices for M3, M6 and M12 each left a crushed candy on the board, and
none of them finished: the interpreter's step limit ended two and the
600 s timeout the third. A crushed candy that stays put can be found in
the same run every round, which is the likely cause; they were replaced
by edits that finish. E1 tells an empty cell by <= 0 and E2 a candy by >
0, the same tests since candies are positive; E3 writes the window test
across as c < n - 2.

## Verification

Every arm prints the same output as `candy_crush.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a73d3c10ad`, whose last compiler change is `3c8e763161`. The runtime
archives were built after that change.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms and the differential at
type checking: at `next_random(mut seed)` in the harness's
`random_board`, whose argument is already a `mut ref`, where legacy
wants the marker dropped and design.md § Call-site `mut` markers now
requires it (kara B-2026-10-14-25), and at `*v` over a row's `iter()`,
since legacy gives those by value where v2 gives references. Legacy
refuses the bench program at `candy_crush(boards[d])`, which it reads as
moving a board out of the vector of boards (E_INDEX_MOVE_NON_COPY);
v2 borrows bare parameters. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
40 random boards of 50 x 50 candies of 5 kinds once, and in each of
100 rounds changes one candy of every board to another kind before
crushing every board, on a copy as the function makes one, summing the
empty cells of the results. Every implementation prints `100 rounds of
40 boards of 50 x 50: 4008123 empty cells`, the Kāra program under
`karac __mir-run` included (in 2.6 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.56 to 0.62 s |
| Rust (`rustc -O`) | 0.57 to 0.85 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.86 to 1.01 s |
| Go | 0.87 to 1.06 s |
| Python | 17.4 to 17.5 s |
| Kāra (`karac build --mir`) | 0.91 to 0.98 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 3.3 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is behind C and Rust, by about two thirds and a third at
the medians of the interleaved runs (0.96 s against 0.58 and 0.74), and
level with Go (0.91) and with Rust under overflow checks (0.97). Under
valgrind's cachegrind it runs 8.3 billion instructions against Rust's
6.3 and C's 3.4, and 2.3 billion branches against 1.5 and 0.8, with
about the same 57 to 58 million mispredicted in all three, so the extra
branches are well predicted; where they come from was not traced. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new.
