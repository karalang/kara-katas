# 2428. Maximum Sum of an Hourglass

You are given an `m x n` integer matrix `grid`.

We define an **hourglass** as a part of the matrix with the following
form:

```
a b c
  d
e f g
```

Return *the **maximum** sum of the elements of an hourglass*.

**Note** that an hourglass cannot be rotated and must be entirely
contained within the matrix.

```
grid = [[6,2,1,3],[4,2,1,5],[9,2,8,7],[4,1,2,9]]  ->  30
grid = [[1,2,3],[4,5,6],[7,8,9]]                  ->  35
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`3 <= m, n <= 150`; `0 <= grid[i][j] <= 10^6`.

An hourglass is fixed by its centre, which may be any cell off the
border, so there are `(m - 2) (n - 2)` of them, each seven cells. Adding
the seven for every centre is O(m n) and already as fast as any reading
of the grid; the other ways of writing it share work between
neighbouring hourglasses or follow the statement's shape more literally.

## Approaches

| file | mechanism |
|---|---|
| `hourglass.kara` ★ | every centre off the border, its seven cells added directly, the largest kept by `max`. O(m n) |
| `hourglass_naive.kara` | the statement read directly: every 3 by 3 box tried by its top-left cell and its nine cells walked, the middle row's two outer cells skipped. O(9 m n) |
| `hourglass_prefix.kara` | 2D prefix sums: each 3 by 3 box summed in four lookups, less the middle row's two outer cells. O(m n) |
| `hourglass_rows.kara` | row triples: the sum of three consecutive cells for every row and column, so an hourglass is the triple above, the centre and the triple below, each triple shared by the hourglasses above and below it. O(m n) |
| `hourglass_iter.kara` | iterators: every centre by `flat_map` over the rows and `map` over the columns, the top and bottom as slices summed by `sum`, then `max`. O(m n) |
| `hourglass_solution.kara` | LeetCode's Rust template: `let (m, n) = (..)` over the lengths, and each hourglass's top and bottom summed over an inclusive slice by `iter().sum::<i32>()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; a 3 by 3
grid of zeros; the constraints' largest, 150 by 150 all `10^6`; then
random grids of 150 by 150, 3 by 150 and 150 by 3, values up to `10^6`;
and 3000 random grids of 3 to 6 by 3 to 6, values up to 9, as a checksum
and the total. `hourglass.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 20000 random grids of up
to 7 by 7 against every box summed cell by cell.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 7 edits: the brackets of `Vec<Vec<i32>>`; each
turbofish `::<i32>` on `sum` dropped, since Kāra has no call-site type
arguments; `struct Solution;` given its braces; and, once the template
parses, `ans` declared `ans: i32`, its literal `0` otherwise keeping the
default `i64` against the `i32` sums. The tuple `let (m, n) = (..)`, the
inclusive slices `j - 1..=j + 1` and the bare `sum()`, whose type comes
from the `i32` it is added to, stand as Kāra. The values fit an `i32`,
as LeetCode's signature has them; the other arms take `i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every placement of the 3 by 3 box, its hourglass the seven
cells listed by their offsets, `(0, 0) (0, 1) (0, 2) (1, 1) (2, 0)
(2, 1) (2, 2)`, and each placement's sum kept when it is the largest
yet. It checks 300 random grids of 3 to 6 by 3 to 6, values up to 1 to
9; then 30 of up to 40 by 40, values up to `10^6`; then 30 of 3 rows or
3 columns and up to 40 the other way, values 0 and 1. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the grid turned half round: the same answer |
| P3 | each row reversed: the same answer |
| P4 | every cell raised by one constant below 1000: the answer plus 7 times it |
| P5 | one cell raised by `10^6`: an answer no smaller, and at most `10^6` larger |
| P6 | each arm agrees with at least three of the other five |

P2 and P3 hold because the hourglass is its own image turned half round
and mirrored left to right, so each takes hourglasses to hourglasses.
P4 holds because every hourglass has seven cells. P5 holds because the
raised cell lies in each hourglass at most once.

The differential prints `360 cases: checksum 808814678, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and sums the seven offsets. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cell left of the centre for the centre | P1 246, P2 271, P3 271, P6 246 |
| M4 | ★: the last hourglass kept | P1 261, P2 316, P3 260, P6 261 |
| M6 | ★: the top middle counted twice | P1 346, P2 251, P4 359, P5 94, P6 346 |
| M8 | naive: every cell of the box counted | P1 349, P4 359, P6 349 |
| M9 | naive: the first row of boxes skipped | P1 145, P2 154, P4 75, P6 145 |
| M11 | naive: only the middle row's left cell left out | P1 303, P2 267, P3 267, P4 359, P6 303 |
| M14 | prefix: the corner not added back | P1 87, P2 133, P3 106, P4 24, P6 87 |
| M15 | prefix: the centre taken out instead | P1 307, P4 359, P6 307 |
| M16 | prefix: the first column of boxes skipped | P1 154, P2 148, P3 148, P4 82, P6 154 |
| M17 | rows: the triples' middle left out | P1 353, P4 359, P6 353 |
| M18 | rows: the middle row's triple for the bottom | P1 297, P2 272, P5 96, P6 297 |
| M21 | rows: the least kept | P1 360, P4 359, P6 360 |
| M24 | iter: the least hourglass | P1 344, P6 344 |
| M25 | iter: only the last row of centres | P1 168, P2 257, P6 168 |
| M26 | iter: the top read twice | P1 319, P2 320, P5 180, P6 319 |
| M30 | solution: the answer started at 100 | P1 330, P4 329, P6 330 |
| M31 | solution: the centre counted twice | P1 343, P4 359, P5 95, P6 343 |


P1 and P6 kill all seventeen, P4 eleven, P2 ten, P3 five and P5 four.

Fourteen are not kept. Five fail exactly as a kept one: the naive arm's
centre left out instead (M7) as the prefix arm's centre taken out
instead (M15); the prefix arm's only the left cell taken out (M13) as
the naive arm's only the middle row's left cell left out (M11); the rows
arm's centre one to the left (M19) as the ★ arm's cell left of the
centre for the centre (M1); the rows arm's best started at `10^6` (M20)
as the template's answer started at 100 (M30), both a floor that only
the small grids sit below; and the template's first column of centres
skipped (M28) as the prefix arm's first column of boxes skipped (M16).
Eight fail apart from every kept one and were left out because those
arms keep their share already: the ★ arm's centre left out, last row of
centres skipped and bottom-left cell left out (M2, M3, M5); the naive
arm's box two wide (M10); the iter arm's top two wide and centre left
out (M22, M23); and the template's centre left out and bottom two wide
(M27, M29), its centre left out failing exactly as the ★ and iter arms'
do.

One ends in an integer overflow, not a wrong answer, under both
backends: the prefix arm's overlap added (M12) adds `pre[r][c]` where it
should subtract it, so each prefix sum is about three times the one
before it on the diagonal, and well inside the 40 by 40 grids they pass
`2^63`.

## Verification

Every arm prints the same output as `hourglass.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.4 to 1.0 s, and the
differential 2.4 s; under `karac __mir-llvm-asan` the differential
takes 1.1 s and under `karac run` 0.7 s.

## Benchmarks

The bench builds 10 grids of 150 by 150, the constraints' largest, once
from its own generator, values up to `10^6`. It then makes 600 passes;
each sets one cell of every grid, so no answer can be carried from one
pass to the next, then answers every grid, folding the answer plus the
pass into the checksum. The bench uses the ★ arm, the seven cells added
for every centre, in all five languages. Every implementation prints
`600 passes over 10 grids of 150 by 150: checksum 539646059`. Each grid
is a list of rows in every language, and in C an array of row pointers.

BENCHTAB
