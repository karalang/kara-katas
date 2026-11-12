# 1139. Largest 1-Bordered Square

Given a 2D `grid` of `0`s and `1`s, return the number of elements in the
largest square subgrid that has all `1`s on its border, or `0` if such a
subgrid doesn't exist in the `grid`.

```
grid = [[1,1,1],[1,0,1],[1,1,1]]  ->  9
grid = [[1,1,0,0]]                ->  1
```

**Constraints:** `1 <= grid.length <= 100`; `1 <= grid[0].length <= 100`;
`grid[i][j]` is `0` or `1`.

The arms are `fn largest1_bordered_square(grid: Vec[Vec[i64]]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `largest1_bordered_square.kara` ★ | runs of 1s: for every cell, how many 1s end there going left along its row and going up its column. A square whose bottom-right corner is (i, j) and side is k has a border of 1s when the bottom and right runs there reach k, and the top run at (i - k + 1, j) and the left run at (i, j - k + 1) do too; each corner tries its sides from the longest down, only above the best so far. O(rows * cols * min(rows, cols)) |
| `largest1_bordered_square_brute.kara` | every square tried, its border read cell by cell: for each side from the longest down, each top-left corner where it fits, until one has 1s all round. O(rows * cols * min(rows, cols)^2) |
| `largest1_bordered_square_sums.kara` | prefix sums along every row and every column, so any stretch of a row or a column is counted in O(1): a square has a border of 1s when each of its four sides sums to its length. O(rows * cols * min(rows, cols)) |
| `largest1_bordered_square_corner.kara` | the ★ arm turned round: runs of 1s going right and going down from every cell, filled from the bottom-right corner in nested `Vec.filled` tables, and each square found from its top-left corner. O(rows * cols * min(rows, cols)) |
| `largest1_bordered_square_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `grid: Vec<Vec<i32>>`, `vec![vec![0; n + 1]; m + 1]` tables of runs indexed from 1, `as usize` lengths, `std::cmp::min` and a `for k in (1..=max_k).rev()` scan), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five properties |

Every arm prints the same 13 lines: LeetCode's two examples; one cell,
1 and 0; a grid of 0s; a column; a solid 3 by 4 block (9); a 3 by 3
block with a hole in its border (4); a frame of 4 drawn inside a frame
of 7 with one cell cleared (25: the outer frame's top and right sides
and the inner frame's bottom and left sides close a square of 5). Then
over 2000 random grids of 1 to 12 rows and columns, 1s at 50, 70 or 90
in 100 and every fourth with a frame drawn on it, the areas summed and a
checksum (`2000 random grids: areas total 22972, checksum 443688415`), and three
of the largest grids the constraints allow, 100 by 100: all 1s (10000),
1s at 90 in 100 (625), and 0s on the diagonal (2500).
`largest1_bordered_square.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: of every square of the grid, the largest area of one whose
border cells, walked round from its top-left corner, are all 1, or 0.
It checks 2000 grids of 1 to 8 rows and columns in four kinds of 500:
1s at 50, 75 or 90 in 100; a frame of 1s drawn on a sparse grid; the
same with one cell of the frame cleared; and every cell 1. Every random
choice, the cell P6 changes among them, is drawn before any arm answers.
53 of the 2000 answer 0.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the grid transposed gives the same answer |
| P3 | each row reversed gives the same answer |
| P4 | the rows in reverse order give the same answer |
| P5 | a ring of 0s round the grid gives the same answer |
| P6 | a drawn cell set to 1 gives no smaller answer, and set to 0 no larger |

All 60,000 checks pass on every arm: `2000 grids: checksum 640310728,
60000 checks over 5 arms: 0 failures`. A Python reading of the same
grids, by the same literal walk, gives the same checksum.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-six are caught; four are
equivalent. The ★ arm's area written `best * (best + 1) - best` is
`best * best`. The solution arm trying a side equal to the best again
(`k < res` for `k <= res`) only stores the best it already has. The
solution arm accepting a top side one short leaves its leftmost cell,
the top-left corner, unread, and the left side's run reads it. The
corner arm starting its rightward runs at 1 everywhere makes every run
one too long where it meets a 0 or the edge, so a top or bottom side may
claim one cell too many; that cell is an end of the right side, whose
own run, still exact, reads it. Fifteen are kept, no two failing the
same checks; one of them stops the run.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a side one longer than the best never tried | P1 1150, P2 14, P3 6, P4 21, P6 10 |
| M2 | ★: the left side not checked | P1 50, P2 77, P3 91 |
| M3 | ★: the top row's 1s start no column run | P1 668, P2 1032, P4 284, P5 668 |
| M4 | ★: each corner's longest side never tried | P1 1658, P3 301, P4 324 |
| M5 | brute: each side's last cell not read | P1 265, P3 233, P4 240 |
| M6 | brute: the rightmost place never tried | P1 715, P2 1032, P3 272, P5 715 |
| M7 | brute: no square answered 1 | P1 53 |
| M8 | sums: each corner's longest side never tried | P1 1233, P3 223, P4 197, P5 1233 |
| M9 | sums: each 1 counted twice down a column | P1 1946, P2 4, P6 1 |
| M10 | sums: only each corner's longest side tried | P1 187, P3 178, P4 179, P5 1927 |
| M11 | corner: rightward runs grow by 2 | stops: index out of bounds |
| M12 | corner: the right side not checked | P1 68, P2 104, P3 91 |
| M13 | corner: a shorter side found later overwrites the best | P1 351, P2 179, P3 93, P4 183, P6 11 |
| M14 | solution: upward runs never grow | P1 1947 |
| M15 | solution: the shortest side tried first | P1 1082 |

P1 catches all fourteen edits that let the run finish. The three
reflections each catch the edits that break the square's symmetry: one
side or one corner treated unlike the others. P3 catches nine, and P2
and P4 seven each; an edit to one side (M2, M12) is seen by the
reflections that move that side, and only P2 sees the column sums
counted twice (M9), since transposing turns them into the row sums the
edit leaves alone. P5 catches four, each an edit that reads the grid's
edge as something it is not: the top row (M3), the rightmost place
(M6), and a corner's longest side, which at the grid's edge is bounded by
the edge rather than by the runs (M8, M10). Padding moves every square
off the edge, so M8 answers rightly on the padded grid exactly where it
answers wrongly on the grid itself (1233 both), and M10, which tries
only that longest side, finds it crossing the ring of 0s nearly every
time. P6 catches the three edits whose answers fail to grow with the
grid: skipping only the side one past the best (M1), the column sums
doubled (M9), and a later, shorter side overwriting the best (M13).
Three edits only P1 sees, since they answer every reflection, padding
and change of a cell consistently: no square answering 1 (M7, wrong on
exactly the 53 grids that answer 0), upward runs that never grow (M14,
which answers 0 for every grid), and the shortest side tried first
(M15). The edit that stops the run makes the corner arm's rightward runs
longer than the row, so a side reads past the end of its table.

Of the eleven caught and not kept, seven fail exactly as a kept one: the
shortest side tried first in the brute arm, the row sums never summed in
the sums arm and the runs filled from the top in the corner arm as M15;
the right side not checked in the sums arm as M12; the shortest side
tried first in the corner arm as M13; the best side stored one short in
the solution arm as M14; and the longer run bounding the side in the
solution arm stops on an index out of bounds as M11 does. The other four
(the top side not checked in the ★ and brute arms, which fail alike, the
longest side never tried in the brute arm, and one 0 allowed in the top
side in the sums arm) each fail in a way of their own and were not
needed.

## Verification

Every arm prints the same output as `largest1_bordered_square.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, brute, sums and corner arms were written as Kāra and checked
clean as written. `karac fix` carried the solution arm in five rounds:
`Vec<Vec<i32>>` to `Vec[Vec[i32]]`, `std::cmp::min` to `min`, `&&` to
`and` and `Solution::` to `Solution.`; then `struct Solution {}`
declared; then the inner `vec![0; n + 1]` to `Vec.filled(n + 1, 0)`,
`res` declared `i32`, and the `as usize` and `as i64` casts that convert
nothing dropped; then `up`'s outer `vec!` to `Vec.filled` and `0i32` on
`left`'s literal; then `left`'s outer `vec!`. Once the gap below was
fixed, that is the whole of it.

The kata found two gaps:

- **B-2026-11-12-11** (fixed): `left` and `up` are fills of fills whose
  `0` an operator settles to `i64` (`left[i][j - 1] + 1`), and `res: i32`
  is given `k`, a loop variable over `(1..=max_k).rev()` with `max_k =
  min(left[i][j], up[i][j])`. `res = k` was refused with only "write an
  explicit `as i32`": the fill's literal was offered its `i32` suffix
  (B-2026-11-08-57) only where the fill itself is read, one index deep.
  A fill of fills is now read to its innermost literal, a binding that
  holds an element (`let k = g[i][j]`, through `min` or `max`, or a
  range's loop variable) is traced back to it, and an assignment's value
  is open for the place it is stored in, as a typed `let`'s is. The
  error names the fill and `karac fix` puts the suffix on its literal.
- **B-2026-11-12-12** (open): storing a literal into an element of an
  open fill (`t[1] = 4` after `let mut t = Vec.filled(3, 0)`) settles
  the fill's literal to `i64` where it is stored, so a later typed read
  (`let r: i32 = t[0]`) that would have fixed it is refused; the result
  depends on which use comes first.

## Benchmarks

The bench builds 20 grids of 100 by 100 once, LeetCode's largest, each
cell 1 with probability 95 in 100. Each of 300 rounds clears or sets one
drawn cell of every grid and answers it with the ★ arm: 6000 calls, each
filling two 100 by 100 tables of runs. Every implementation prints `300
rounds over 20 grids of 100 by 100: areas total 9571101, checksum
429512436`. Each makes the two tables row by row in every call:
`Vec.filled` rows in Kāra, `vec![0; cols]` in Rust, `calloc` in C,
`make` in Go and list repetition in Python.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `87bec305bc`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.246 to 0.354 s | 0.297 s |
| C (`clang -O3`) | 0.254 to 0.385 s | 0.301 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.236 to 0.400 s | 0.333 s |
| Kāra (`karac build`) | 0.241 to 0.432 s | 0.338 s |
| Rust (`rustc -O`) | 0.322 to 0.468 s | 0.349 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.345 to 0.534 s | 0.392 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.326 to 0.510 s | 0.399 s |
| Go | 0.985 to 1.107 s | 1.034 s |
| Python | 10.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra, C and Rust land within each other's spread, which
runs 0.11 to 0.19 s wide: C takes about 0.89x to 0.90x Kāra's median
time, Rust 1.05x, and Rust under overflow checks 1.18x to 1.20x. C's
user time, 0.22 to 0.24 s, is well under its real time: its 200 rows a
call come from `calloc`, whose fresh pages fault in. Go takes about
3.1x Kāra's time, its user time above its real time with the collector
running beside it; this README has not measured the rest. Python takes
about 32x.
