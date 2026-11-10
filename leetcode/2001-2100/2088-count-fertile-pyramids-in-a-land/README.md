# 2088. Count Fertile Pyramids in a Land

A farmer has a rectangular grid of land with `m` rows and `n` columns
that can be divided into unit cells. Each cell is either fertile
(represented by a `1`) or barren (represented by a `0`). All cells
outside the grid are considered barren.

A pyramidal plot of land can be defined as a set of cells with the
following criteria:

1. The number of cells in the set has to be greater than `1` and all
   cells must be fertile.
2. The apex of a pyramid is the topmost cell of the pyramid. The height
   of a pyramid is the number of rows it covers. Let `(r, c)` be the apex
   of the pyramid, and its height be `h`. Then, the plot comprises of
   cells `(i, j)` where `r <= i <= r + h - 1` and `c - (i - r) <= j <= c +
   (i - r)`.

An inverse pyramidal plot of land can be defined as a set of cells with
similar criteria:

1. The number of cells in the set has to be greater than `1` and all
   cells must be fertile.
2. The apex of an inverse pyramid is the bottommost cell of the inverse
   pyramid. The height of an inverse pyramid is the number of rows it
   covers. Let `(r, c)` be the apex of the pyramid, and its height be
   `h`. Then, the plot comprises of cells `(i, j)` where `r - h + 1 <= i
   <= r` and `c - (r - i) <= j <= c + (r - i)`.

Given a 0-indexed `m x n` binary matrix `grid` representing the
farmland, return the total number of pyramidal and inverse pyramidal
plots that can be found in `grid`.

```
grid = [[0,1,1,0],[1,1,1,1]]                              ->  2
grid = [[1,1,1],[1,1,1]]                                  ->  2
grid = [[1,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[0,1,0,0,1]]  ->  13
```

**Constraints:** `m == grid.length`; `n == grid[i].length`; `1 <= m, n
<= 1000`; `1 <= m * n <= 10^5`; `grid[i][j]` is either `0` or `1`.

A pyramid of height `h` apexed at a fertile cell holds the three
pyramids of height `h - 1` apexed at the cells below it, so the tallest
pyramid at a cell is one more than the least of the three below, and a
cell whose tallest is `t` apexes `t - 1` plots. One pass from the bottom
row up counts the pyramids and one from the top down the inverse ones:
O(m · n). The approaches differ in how they keep the heights, or whether
they grow each plot instead.

## Approaches

| file | mechanism |
|---|---|
| `pyramids.kara` ★ | the dynamic programming in rolling rows: one function given the order of the rows, `(0..m).rev()` for the pyramids and `0..m` for the inverse, each row's heights from the row before. O(m · n) |
| `pyramids_table.kara` | the same in two full tables, `Vec[Vec[i64]]` copies of the land filled in place, bottom up and top down |
| `pyramids_grow.kara` | each fertile cell as an apex, the plot widened a row at a time both ways while `all()` the next span, a slice `row[c - i..=c + i]`, is fertile. O(m · n · h²) |
| `pyramids_prefix.kara` | the same growth with row prefix sums, each span's test O(1). O(m · n · h) |
| `pyramids_memo.kara` | a `struct Land` with a memoised recursive `tallest(r, c)` in a `Map[(i64, i64), i64]`, the pyramids only; the inverse pyramids are the pyramids of the land with its rows reversed |
| `pyramids_solution.kara` | LeetCode's Rust template (`Vec<Vec<i32>>`, `let mut f = grid.clone()` filled in place, `(0..m - 1).rev()` and `1..n - 1`, `.min(..)` chained), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more, each land and its count; then the sum and a checksum of the counts
for 2000 random lands of 1 to 12 rows and columns, 5 to 9 cells in 10
fertile; then the counts for two of the constraints' largest, `10^5`
cells, 316 by 316 with 19 cells in 20 fertile and 100 by 1000 with 9 in
10. `pyramids.py` mirrors the ★ arm and its output is byte-identical; the
★ arm was also checked against every apex, height and way on 2000 random
lands of up to 7 by 7, in Python.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every cell as an apex, every height from 2, either way, kept
when every cell of the plot lies in the land and is fertile. It checks
300 random lands of 1 to 7 rows and columns, 5 to 9 cells in 10 fertile;
then 20 all fertile, and 20 all barren. All 340 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the land upside down counts the same |
| P3 | the land mirrored, east for west, counts the same |
| P4 | the land with a barren row and column round it counts the same |
| P5 | the first barren cell made fertile counts no fewer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 lands: checksum 91667723, 12240 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal counts was checked against a Python reading of the same
lands. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, five or six to each of its arms,
each run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen
are kept, three to each Kāra arm and two to the Rust-template arm. Each
kept one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an edge cell's plot of height 0 | P1 315, P4 315, P5 172, P6 315 |
| M2 | ★: half the plots counted | P1 30, P6 30 |
| M3 | ★: the cell below not looked at | P1 121, P6 121 |
| M4 | table: the pyramids' table filled top down | P1 25, P2 18, P6 25 |
| M5 | table: the inverse capped at height 2 | P1 103, P2 90, P6 103 |
| M6 | table: the inverse never apexed in the second column | P1 112, P2 61, P3 68, P4 112, P6 112 |
| M7 | grow: the last column never in a plot | P1 124, P3 90, P4 124, P6 124 |
| M8 | grow: a span with any fertile cell taken | P1 179, P4 267, P6 179 |
| M9 | grow: a span's last cell not looked at | P1 124, P3 117, P4 168, P6 124 |
| M10 | prefix: a span one cell short of fertile taken | P1 172, P4 200, P5 73, P6 172 |
| M11 | prefix: a barren apex grown | P1 127, P4 169, P6 127 |
| M12 | prefix: every cell summed as fertile | P1 181, P4 316, P6 181 |
| M13 | memo: the second column's plots of height 1 | P1 125, P3 90, P4 125, P6 125 |
| M14 | memo: a remembered height one too tall | P1 163, P3 19, P4 269, P6 163 |
| M15 | memo: the plots of height 2 missed | P1 159, P6 159 |
| M16 | solution: the adapter's land barren for fertile | P1 187, P4 256, P5 29, P6 187 |
| M17 | solution: the cell below not looked at | P1 105, P2 83, P6 105 |

P1 and P6 kill all seventeen, P4 eleven, P3 five, P2 four, and P5
three. P4, which puts a barren border round the land, sees every edit
that cares where the land ends or what is fertile: an edge cell's height
(M1), a column never used (M6, M7, M13), a span's cells (M8, M9, M10,
M12), a barren apex (M11), a height remembered wrong (M14), the land's
cells swapped (M16). P3, the land mirrored, sees an edit that treats east
and west differently (M6, M7, M9, M13, M14), and P2, the land upside
down, one that treats the pyramids and the inverse ones differently
(M4, M5, M6, M17). P5 sees only the edits that let a fertile cell lower
the count: an edge cell counting `-1` (M1), a span short of fertile
(M10), the land's cells swapped (M16). Three are seen by P1 and P6 alone,
since each errs alike on a land and on its upside-down, mirrored and
framed copies: half the plots (M2), the cell below never asked (M3), the
plots of height 2 missed (M15).

Of the thirty-two, fifteen were not kept, and none survives. Three fail
as a kept one: the memo arm's cell below not looked at as M3, and the ★
arm's row before never kept and the prefix arm's span summed one place
short as M15. Twelve are killed with checks of their own but were left
out because their arm keeps three, or the Rust arm two: the ★ arm's
pyramids counted twice for the inverse and its pyramids' rows walked top
down, the grow arm's pyramids counted twice, the prefix arm's pyramids
grown twice and the memo arm's land not flipped, which fail alike (P1
92, P2 92); the table arm's apex counted once whatever its height (P1
175, P2 128, P4 316) and its barren apex grown (P1 140, P2 105, P4 248);
the grow arm's growth starting at height 3 (P1 157); the Rust arm's
inverse never apexed in the second row and the prefix arm's first row
never a base, which fail alike (P1 90, P2 82, P4 90); the Rust arm's
inverse read from the pyramids' table (P1 26, P2 18, P4 26) and its
pyramids counted with their apex (P1 203, P2 109, P4 316).

## Verification

Every arm prints the same output as `pyramids.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 1.7 s to 2.3 s, but for the memo
arm's 6 s, which hashes every cell into its `Map`, and the grow arm's
11 s, which reads every span of every plot again, and the differential
1.5 s (timed while other work shared the machine).

No arm met a compiler gap. The Rust arm was written as LeetCode's Rust
template. `karac fix` carries it in three rounds of 13, 2 and 1 edits:
Rust's spellings (`Vec<Vec<i32>>` to brackets, the adapter's
`&Vec<Vec<i64>>` to `ref` and the `&` of `|&x|` dropped, `struct
Solution;` to `struct Solution {}`, `Solution::` to `.`); then `let mut
ans = 0` to `ans: i32`, as the literal kept the default `i64` against the
`i32` the method returns, and the adapter's `as i64`, which the `i32`
widens to anyway; then the adapter's `ref` parameter to a bare one,
which borrows already. The fixed arm reads as the template does.

## Benchmarks

The bench builds 20 lands of 316 by 316, the constraints' limit, from
15 to 19 cells in 20 fertile, and counts each 20 times with the ★ arm in
all five languages, the heights of each row in a fresh growable array (a
`Vec`, a `Vec`, a slice, a `list`, a `calloc`'d buffer): 400 counts of
`10^5` cells each way. Every implementation prints `400 counts: sum
88451860, checksum 711664593`.

BENCHTAB
