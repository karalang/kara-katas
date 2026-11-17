# 1594. Maximum Non Negative Product in a Matrix

You are given a `m x n` matrix `grid`. Initially, you are located at the
top-left corner `(0, 0)`, and in each step, you can only move right or
down in the matrix.

Among all possible paths starting from the top-left corner `(0, 0)` and
ending in the bottom-right corner `(m - 1, n - 1)`, find the path with
the maximum non-negative product. The product of a path is the product
of all integers in the grid cells visited along the path.

Return the maximum non-negative product modulo `10^9 + 7`. If the
maximum product is negative, return `-1`.

Notice that the modulo is performed after getting the maximum product.

```
grid = [[-1,-2,-3],[-2,-3,-3],[-3,-3,-2]]  ->  -1
grid = [[1,-2,1],[1,-2,1],[3,-4,1]]        ->  8
grid = [[1,3],[0,-4]]                      ->  0
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`1 <= m, n <= 15`; `-4 <= grid[i][j] <= 4`.

## Approaches

A negative cell turns the smallest product reaching it into the largest,
so each cell needs both. A path has at most 29 cells, so a product is at
most `4^29` in size and fits in `i64`; the modulus is taken at the end.

| file | mechanism |
|---|---|
| `product.kara` ★ | the largest and the smallest product of a path reaching each cell, in two `Vec.filled` tables of `i64`, each cell from the one above and the one to the left. O(mn) |
| `product_memo.kara` | from the end: the largest and smallest product from each cell to the corner, by recursion that keeps each cell's pair in a `Map[(i64, i64), (i64, i64)]`. O(mn) |
| `product_sign.kara` | by sign: a `Reach` struct per cell holding the largest positive product and the negative product of largest size as `Option[i64]`s, and whether a path through a zero gets there. O(mn) |
| `product_solution.kara` | LeetCode's Rust template (two `vec![vec![0i64; n]; m]` tables, the first row and column filled first, `max`/`min` over four products), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (`[[-4]]`, `[[0]]`, and 15 by 15 grids of 4 and of -4), then the
count only negative and a checksum for 3000 random grids of up to 4 by 4
and 300 of up to 15 by 15, cells from -4 to 4. `product.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every path right and down from the corner to the corner, each
one's product, and the largest, `-1` when it is negative. It checks 3000
grids of 1 to 3 by 1 to 4 cells from -4 to 4, every random choice drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the grid transposed leaves the answer |
| P3 | the grid turned half way round leaves the answer |
| P4 | the top left cell doubled doubles the answer, or leaves `-1` |
| P5 | every cell negated leaves the answer when a path has an even number of cells (checked only then) |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 485040119, 65992 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the smallest from above ignores the smallest there | P1 19, P2 69, P3 39, P5 28, P6 19 |
| M2 | ★: the cell to the left read only in the first row | P1 708, P2 938, P3 938, P6 708 |
| M3 | ★: a largest product of 0 answered `-1` | P1 872, P6 872 |
| M4 | memo: the smallest product kept as the largest | P1 388, P3 450, P5 321, P6 388 |
| M5 | memo: the smallest from below left out | P1 177, P2 365, P3 266, P5 208, P6 177 |
| M6 | sign: a negative cell keeps the signs | P1 1026, P6 1026 |
| M7 | sign: a path through a zero not counted | P1 872, P6 872 |
| M8 | sign: two candidates merged to the smaller | P1 495, P6 495 |
| M9 | template: the smallest of four products from two | P1 76, P3 128, P5 59, P6 76 |
| M10 | template: the first row not multiplied | P1 1170, P2 1769, P3 1472, P5 642, P6 1170 |

## Benchmarks

The bench draws 40000 grids of 15 by 15 cells from -4 to 4 first, then
answers each by the ★ arm, in all five languages. Every implementation
prints `40000 grids of 15 by 15: 0 only negative, checksum 321315624`.
The C mirror keeps each grid and each table as a malloc'd array of
malloc'd rows, as Kāra's `Vec[Vec[i64]]` is.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.097 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.128 s |
| Rust (`rustc -O`) | 0.130 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.133 s |
| Kāra (`karac build`) | 0.136 s |
| Go | 0.249 s |
| Python | 7.1 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.120 s and 0.153 s on one run).

## Verification

All four arms print the same output as `product.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The ★ and memo arms were written in Kāra and checked as written. The
sign arm wrote `let end = reach[rows - 1][cols - 1]`, and `karac fix`
made it `ref`, as a struct is not copied out of a `Vec` by indexing.

The Rust template took one `karac fix`, of 16 edits: `struct Solution;`
to `struct Solution {}`, `Vec<Vec<i32>>` to `Vec[Vec[i32]]`, each
`vec![vec![0i64; n]; m]` to `Vec.filled(m, Vec.filled(n, 0))`, the
`as i64` dropped where an `i32` cell multiplies an `i64`, and
`Solution::` to `Solution.`. It then checks and agrees with no hand edit.

It first left a program that checked clean and overflowed: in one pass
`karac fix` dropped both the `0i64` suffix, since the stores' casts type
the table, and the stores' `as i64`, since the suffix does, which left
an `i32` table (B-2026-11-17-128). The cast fixes now wait for a pass
with no suffix fix, and the stores into `mx[0][0]` keep their cast.
