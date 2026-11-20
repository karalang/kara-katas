# 1260. Shift 2D Grid

Given a 2D `grid` of size `m x n` and an integer `k`. You need to shift
the `grid` `k` times.

In one shift operation:

- Element at `grid[i][j]` moves to `grid[i][j + 1]`.
- Element at `grid[i][n - 1]` moves to `grid[i + 1][0]`.
- Element at `grid[m - 1][n - 1]` moves to `grid[0][0]`.

Return the *2D grid* after applying shift operation `k` times.

```
grid = [[1,2,3],[4,5,6],[7,8,9]], k = 1                          ->  [[9,1,2],[3,4,5],[6,7,8]]
grid = [[3,8,1,9],[19,7,2,5],[4,6,11,10],[12,0,21,13]], k = 4    ->  [[12,0,21,13],[3,8,1,9],[19,7,2,5],[4,6,11,10]]
grid = [[1,2,3],[4,5,6],[7,8,9]], k = 9                          ->  [[1,2,3],[4,5,6],[7,8,9]]
```

**Constraints:** `1 <= m, n <= 50`; `-1000 <= grid[i][j] <= 1000`;
`0 <= k <= 100`.

The arms are `fn shift_grid(grid: Vec[Vec[i64]], k: i64) -> Vec[Vec[i64]]`,
the grid taken by value (`own`) where the arm changes it.

## Approaches

Read in row order, the grid is one list of `m * n` values, and a shift
moves every value one place on, the last to the front: `k` shifts
rotate that list right by `k` modulo its length.

| file | mechanism |
|---|---|
| `shift_2d_grid.kara` ★ | by flat index: the value at flat place `p` written to place `(p + k) % (m * n)` of a new grid, row `to / n`, column `to % n` |
| `shift_2d_grid_rotate.kara` | by rotation: the rows flattened with `flat_map`, `rotate_right(k % len)`, and cut back into rows with `chunks(n)` |
| `shift_2d_grid_steps.kara` | step by step, as the statement does it: `k` modulo `m * n` single shifts in place, a `carry` taking each value to the next place |
| `shift_2d_grid_reverse.kara` | by three reversals of the flattened list (all of it, then its first `k` and the rest), with a `fn reverse_range` on `swap`, and the rows rebuilt by slicing |
| `shift_2d_grid_solution.kara` | a Rust solution as LeetCode's Rust users write it (`k as usize % total`, `vec![vec![0; n]; m]`, `Vec<Vec<i32>>`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's three examples; the sum
of the top-left values and a checksum of the grids for 1000 random grids
of 1 to 50 by 1 to 50, shifted by 0 to 100 (`corners 3585, checksum
390588424`); and three grids at the constraints' top, 50 by 50 shifted
by 100 and a column and a row of 50 shifted by 99. `shift_2d_grid.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the ★ and reversal arms checked clean as first written.
The rotation arm was first written with Rust's `grid.iter().flatten()`
and `flat.chunks(n).map(..)`: `flatten` takes items that are iterators,
which a `ref Vec[i64]` is not, and `chunks` gives a `Vec`; `karac fix`
writes `.flat_map(|v| v.iter())` and adds the `.into_iter()`. The step
arm takes its grid `own`, and the harness's first call gave away the
grid the third call shows again (E0500); the fix passes `g.clone()`.
The solution arm takes one round of fixes, 17 by `karac fix`'s count:
`struct Solution;` to `struct Solution {}`, `Vec<..>` to brackets, `k as
usize % total` to `k % total`, `vec![vec![0; n]; m]` to
`Vec.filled(m, Vec.filled(n, 0))`, the `|&x|` patterns to `|x|` and
`Solution::` to `Solution.`. All five check clean.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: `k` times, a new grid made by the three moves as written, with
no modulus. 2000 random grids of 1 to 6 by 1 to 6 with values 0 to 9 (so
many repeat), shifted by 0 to 100.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | shifted on by the rest of `m * n`, the grid back |
| P3 | shifted by `k + m * n`, the same grid |
| P4 | the same values |
| P5 | shifted by `a` and then by `k - a`, the same grid |
| P6 | the ★ arm's grid |

All 60,000 checks pass on every arm: `2000 grids: checksum 12299116,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the
same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the shift taken modulo the row length | P1 1218, P2 984, P5 476, P6 4872 |
| S2 | ★: each place reads the value `k` on, a shift left | P1 1458, P6 5832 |
| R1 | rotation: `rotate_left` for `rotate_right` | P1 1458, P6 1458 |
| R2 | rotation: rows cut at `m` values, not `n` | P1 1688, P5 1688, P6 1688 |
| T1 | step by step: `k` taken modulo `m * n + 1` | P1 1514, P2 1514, P3 1687, P5 713, P6 1514 |
| T2 | step by step: the carry starts from the top left | P1 1617, P2 1641, P4 1617, P5 661, P6 1617 |
| V1 | reversals: the first `m * n - k` and the rest reversed, a shift left | P1 1458, P6 1458 |
| V2 | reversals: the middle pair of a range left unswapped | P1 1528, P2 1205, P5 1276, P6 1528 |
| L1 | solution: each row read from its end | P1 1650, P2 1108, P5 1646, P6 1650 |
| L2 | solution: every value one place too far | P1 1929, P2 1847, P5 1929, P6 1929 |

All ten are caught, every one by P1, the statement read literally, and
by P6. The three that shift left (S2, R1, V1) are caught by nothing
else: a shift left is as consistent as a shift right, so shifting on by
the rest of `m * n` still gives the grid back (P2), `k + m * n` still
gives the same grid (P3), and two shifts still add up (P5); only the
direction the statement names tells them apart. R2's rows of the wrong
length survive P2 too, since a second wrong cut puts the rows back. P4,
the same values, catches only T2, the one mutation that copies a value
over another: its carry starts from the top-left value and the bottom
right one is lost.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (each value at flat place p written to (p + k) % (m * n) of a new
grid) on 200 random grids of 50 by 50 built once, each shifted by a
random 0 to 100, 150 rounds; a corner and the middle of each result
folded into a checksum. Every program prints `150 rounds of 200 grids of
50 by 50: checksum 127468808`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.379 to 0.429 s | 0.399 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.379 to 0.432 s | 0.389 s |
| Rust (`rustc -O`) | 0.383 to 0.434 s | 0.393 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.378 to 0.439 s | 0.388 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.381 to 0.424 s | 0.389 s |
| C (`clang -O3`) | 0.192 to 0.261 s | 0.221 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.190 to 0.230 s | 0.198 s |
| Go | 0.722 to 0.778 s | 0.738 s |
| Python | 10.35 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.388 s
against 0.389 s), and the two ranges overlap. Kāra takes about 1.8x C's
time (0.389 s against 0.221 s); Go takes about 1.9x Kāra's time. Python
takes about 27x Kāra's time. No profile was taken.
