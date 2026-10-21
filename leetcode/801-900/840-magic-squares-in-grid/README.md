# 840. Magic Squares In Grid

A 3 x 3 magic square is a 3 x 3 grid filled with distinct numbers from 1
to 9 such that each row, each column and both diagonals all have the
same sum. Given a `row x col` grid of integers, return how many 3 x 3
contiguous subgrids of it are magic squares. (A magic square may hold
numbers above 9 in general; here it may not.)

```
grid = [[4,3,8,4],[9,5,1,9],[2,7,6,2]]  ->  1
grid = [[8]]                            ->  0
```

**Constraints:** `1 <= row, col <= 10` and `0 <= grid[i][j] <= 15`.

## Approaches

Every arm looks at each 3 x 3 window of the grid; they differ in how
they decide it is magic.

| file | mechanism |
|---|---|
| `magic_squares_in_grid.kara` ★ | the centre first: the numbers 1 to 9 add up to 45, so each row adds up to 15, and the four lines through the centre add up to 60 = 45 + 3 times the centre, which is therefore 5. A window is looked at only if its centre is 5; then its numbers must be 1 to 9 once each, kept as bits of a mask, its rows and columns must add up to 15 and each diagonal's corners to 10. O(rows cols) |
| `magic_squares_in_grid_ring.kara` | the ring around the centre: there are only eight magic squares of 1 to 9, the turns and mirror images of the Lo Shu, `4 9 2 / 3 5 7 / 8 1 6`. A window is magic when its centre is 5 and its ring, read clockwise from its top left corner, is the Lo Shu's ring `4 9 2 7 6 1 8 3` started at one of its corners, read forwards or backwards. O(rows cols) |
| `magic_squares_in_grid_lines.kara` | every line summed, with no shortcut: the window's nine numbers, sorted, must be 1 to 9, and its eight lines must all have its first row's sum. O(rows cols) |
| `magic_squares_in_grid_prefix.kara` | prefix sums: running sums along each row and down each column give a window's row and column sums by one subtraction each; its numbers are counted in a table and its diagonals added up directly. O(rows cols) |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 18 lines: LeetCode's two examples; eleven more
(the Lo Shu and one of its mirror images, a square of 5s, whose lines
all add up to 15, the Lo Shu with 1 added to every number, whose lines
all add up to 18, the numbers 1 to 9 in order, the Lo Shu with two
numbers swapped, two magic squares sharing a column, grids of two rows
and of one column, a magic square in the corner of a 4 x 4 grid, and all
eight magic squares side by side); three grids of LeetCode's largest
size, 10 x 10, with few and many squares stamped on them, shown by their
count and a checksum of the grid; and 300 random grids with their total
count and a checksum. The random grids are numbers 0 to 15 with up to 5
squares stamped on them: magic squares, magic squares moved off 1 to 9,
squares of 5s, magic squares with two cells swapped or another centre,
and turns of `1 5 9 / 6 7 2 / 8 3 4`, whose rows and columns add up to
15 but not its diagonals. `magic_squares_in_grid.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a window is magic when its nine numbers are distinct and each
from 1 to 9, and its three rows, three columns and two diagonals all
have the same sum, whatever that sum is. Its 1,600 cases come in four
kinds of 400: grids up to 5 x 5 with up to 3 squares stamped; single 3 x
3 grids with one; grids up to 10 x 10 with up to 12; and grids up to 6 x
6 with a magic square stamped and then one cell anywhere changed. 387 of
them hold a magic square.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the grid transposed gives the same answer |
| P3 | the grid turned a quarter gives the same answer |
| P4 | a border of zeros round the grid gives the same answer |
| P5 | the answers on each 3 x 3 window taken alone add up to the answer |

It prints `1600 cases, 32000 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the mask's check dropped | P1 153 |
| M2 | ★: the centre read one column right | P1 387 |
| M3 | ★: the last window of each row skipped | P1 223, P2 152, P3 146, P4 223, P5 166 |
| M4 | ring: the ring read from one corner only | P1 293, P3 185 |
| M5 | ring: the ring never read backwards | P1 192, P2 384 |
| M6 | ring: the centre not checked | P1 148 |
| M7 | lines: the diagonals left out | P1 151 |
| M8 | lines: the numbers not sorted | P1 387 |
| M9 | lines: the windows in the last rows skipped | P1 210, P2 152, P3 152, P4 210, P5 178 |
| M10 | prefix: a column's sum one row short | P1 387 |
| M11 | prefix: the counts kept from window to window | P1 180, P2 152, P3 160, P4 208, P5 180 |
| M12 | prefix: a row's sum one column short | P1 387 |

P1 kills all twelve, and seven of them only P1 sees: an edit that
misjudges a window misjudges it wherever it sits and however the grid is
turned. M2, M8, M10 and M12 reject every window, so they fail exactly
the 387 cases that hold a magic square. M4 and M5 split between the two
symmetries: from one corner, the ring arm accepts only the Lo Shu and
its mirror image across the falling diagonal, a pair that transposing
keeps and turning breaks, so only P3 sees it; read only forwards, it
accepts the four turns and no mirror image, which turning keeps and
transposing breaks, so only P2 sees it. M3, M9 and M11 depend on where a
window sits, so every property sees them, P5 most directly: each window
taken alone is judged right. M6 and M7 are the weakest kills, 148 and
151 checks; they need a magic square with another centre, or a square
whose rows and columns add up to 15 and diagonals do not, and the stamps
make both on purpose. Before they did, M6 and M7 failed 14 and 6 checks.
A first P5 set every number above 9 to 0 and killed none of the twelve:
every arm rejects such a number at once, and no edit touched that.

## Verification

Every arm prints the same output as `magic_squares_in_grid.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `4a744e1ec3`, and the runtime archives are
current with them. Under `karac __mir-run` each arm takes 0.2 s and the
differential 3.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends do not run this kata. `karac run --interp`,
`karac run` and `karac build` all refuse the four arms and the
differential at the harness's `*v`, a number read through `row.iter()`:
legacy types the loop variable as an `i64`, not a reference, though
`karac check` accepts it on v2. Legacy refuses the bench program as
moving a grid out of an index, which v2's borrowing parameters do not
do. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
grids once, each of LeetCode's largest size, 10 x 10, of numbers 0 to 15
with 12 squares stamped on it: the Lo Shu turned or mirrored, a square
of 5s, or the Lo Shu with 1 added to every number. Each of 14 million
rounds changes one cell of the next grid and counts its magic squares.
Every implementation prints `14000000 rounds of 64 grids: 219341 magic
squares, checksum 68055408`, the Kāra program under `karac __mir-run`
included, in 1019 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.99 to 1.12 s |
| Rust (`rustc -O`) | 1.46 to 1.69 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.56 to 1.80 s |
| Go | 3.92 to 4.21 s |
| Python | 236 to 241 s |
| Kāra (`karac build --mir`) | 1.60 to 1.75 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.65 s, against Rust's
1.54 (1.75 under overflow checks), C's 1.01 and Go's 4.08: 0.94 times
Rust's time under overflow checks, 1.6 times C's, and 0.40 times Go's.
Under valgrind's cachegrind C runs 10.1 billion instructions and 3.0
billion branches, Rust 22.7 and 4.9 billion and v2 25.0 and 5.5 billion;
the three mispredict about alike, 528, 558 and 553 million branches. The
C program keeps each grid as a fixed 10 x 10 array, where the others
keep a vector of row vectors and check each index: most likely that is
the gap to C (not traced). Built for `x86-64-v3`, the target `karac
build` uses, C takes 1.06 to 1.20 s and Rust with overflow checks 1.51
to 1.62 s, against v2's 1.76 to 1.79 s in the same five interleaved
runs. Python takes 238 s, about 235 times C's time; a round takes C
about 70 ns. The comparison with C and Rust waits until after M4.

## Compiler findings

None on v2: every arm, the differential and the bench program pass
`karac check` and run on both v2 backends as written.
