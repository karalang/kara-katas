# 1240. Tiling a Rectangle with the Fewest Squares

Given a rectangle of size `n` x `m`, return *the minimum number of
integer-sided squares that tile the rectangle*.

```
n = 2,  m = 3   ->  3    (two 1x1 squares and one 2x2)
n = 5,  m = 8   ->  5
n = 11, m = 13  ->  6
```

**Constraints:** `1 <= n, m <= 13`.

The arms are `fn tiling_rectangle(n: i64, m: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `tiling_a_rectangle_with_the_fewest_squares.kara` ★ | backtracking on the skyline, the heights of the `m` columns filled so far (a `Vec.filled(m, 0)` passed `mut ref`): the lowest column, the leftmost of them, takes a square of every size that fits, the largest first, as wide as the run of columns at that height and no taller than the room above. A branch stops once it has used as many squares as the best tiling found so far |
| `tiling_a_rectangle_with_the_fewest_squares_grid.kara` | on the board itself, a `Vec[Vec[bool]]` of filled cells: the first empty cell in reading order (an `Option[(i64, i64)]`) takes every square that fits on empty cells, the largest first, with the same cut |
| `tiling_a_rectangle_with_the_fewest_squares_bfs.kara` | breadth first over skylines: each level grows every skyline by one square at its lowest column, of every size that fits, a skyline seen before (a `Set[Vec[i64]]`) not queued again; the level at which every column is full is the answer |
| `tiling_a_rectangle_with_the_fewest_squares_cuts.kara` | the guillotine cuts, memoised: a square is one, any other rectangle the best of every straight cut across it into two. A tiling with no straight cut through it is missed, and up to 13 x 13 only 11 x 13 needs one (6 squares, against 8 by cuts), so that one is taken as known, as LeetCode solutions of this kind do |
| `tiling_a_rectangle_with_the_fewest_squares_memo.kara` | memoised over skylines, with no cut: the fewest squares that finish a skyline is one more than the fewest that finish it after a square at its lowest column, of any size; each skyline is a `Map[i64, i64]` key, its heights read as base-14 digits with `fold` |
| `tiling_a_rectangle_with_the_fewest_squares_solution.kara` | a Rust solution as LeetCode's Rust users write it (the skyline search over a `vec![0; m as usize]`, the lowest column found against `i32::MAX`, the run of columns measured in `usize` with `as i32` casts, `Self::dfs(&mut h, ..)`, and the sizes tried by `(1..=(end - pos)).rev()`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 7 lines: LeetCode's three examples (`3`, `5`,
`6`); `1 x 1`, `13 x 13`, `1 x 13` and `13 x 1` (`1 1 13 13`); the rows
`11 x 1..13` (`11 7 6 6 6 6 6 6 7 6 1 7 6`) and `13 x 1..13` (`13 8 7 7
6 6 6 6 7 7 6 7 1`); and a checksum and the total of the answers for all
169 rectangles up to 13 x 13 (`981666112`, `867`).
`tiling_a_rectangle_with_the_fewest_squares.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the five Kāra arms check clean as written. The solution
arm takes one round of 17 fixes (`struct Solution;` to `struct Solution
{}`, `Self::dfs` to `Solution.dfs` twice, the four arguments `dfs` writes
marked `mut` (two of them written `&mut`, two bare), the two `&mut T` parameters to `mut ref T`, `Vec<i32>` to
`Vec[i32]`, `i32::MAX` to `i32.MAX`, the two `&&` to `and`, `vec![0; m
as usize]` to `Vec.filled(m, 0)`, and the wrapper's `as i64` on an `i32`
dropped) and checks clean.

## Gaps

None found: every arm, as written, checks, runs and builds alike.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every tiling of the rectangle by integer-sided squares, each
counted once (the first empty cell in reading order is a square's top-left
corner, of every size that fits), and the fewest squares among them, with
no branch cut. Every rectangle from 1 x 1 to 13 x 13.

| | property |
|---|---|
| P1 | the statement read literally (up to 6 x 6) |
| P2 | the sides swapped give the same answer |
| P3 | at least the area over the largest square that fits, at most the best of straight cuts alone (no rectangle taken as known) |
| P4 | the rectangle scaled up, `k n` x `k m`, needs no more squares |
| P5 | `n` x `m` and `n` x `k` side by side, `n` x `(m + k)`, need no more than both |
| P6 | the ★ arm's answer |

All 6,084 checks pass on every arm: `169 rectangles: checksum 981666112,
6084 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, with the
skyline search and breadth-first search, gives the same table.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the rightmost of the lowest columns taken | P1 25, P3 144, P4 216, P5 660, P6 720 |
| S2 | ★: a square one taller than the room above | P1 9, P2 116, P3 27, P4 7, P6 400 |
| G1 | grid: a square's last column not checked for room | P1 3, P2 50, P4 3, P5 10, P6 46 |
| G2 | grid: no square of side 1 | P1 10, P3 68, P6 68 |
| B1 | bfs: the largest square that fits never placed | never finishes: step limit under `__mir-run`, still running at 1500 s under `run` |
| B2 | bfs: the search ended a row short of the top | P1 24, P2 124, P3 48, P4 24, P5 58, P6 120 |
| C1 | cuts: 11 x 13 not taken as known | P6 2 |
| C2 | cuts: the middle cut missed | P1 10, P2 100, P3 81, P6 81 |
| M1 | memo: the heights read in base 13, so a column of 13 carries | NOT CAUGHT |
| M2 | memo: an answer kept under the next skyline's key | P1 25, P2 114, P3 144, P6 144 under `run`; step limit under `__mir-run` |
| R1 | solution: no square reaching the top | never finishes: step limit under `__mir-run`, still running at 1500 s under `run` |
| R2 | solution: the widest square never tried | P1 25, P3 144, P6 144 |

Eleven of the twelve are caught: nine fail properties, and two never
finish. When the ★ arm itself is mutated (S1, S2), P6 fails on the other
five arms too, which is why its counts there run to 720. Searches that
miss tilings answer too high: the ★ arm starting from the rightmost of
the lowest columns (S1), whose square there may need to reach left, the
grid arm with no square of side 1 (G2), and the solution arm never
trying the widest square (R2). P3 catches all three where they go past the best of straight cuts, and P1 on the small
rectangles. Searches that accept a non-tiling answer too low: a square
taller than the room above (S2), squares allowed to overlap in their last
column (G1), and the breadth-first search stopping a row short (B2); P2
catches these, since the overcount differs with the sides swapped. Two
make the search unable to finish a tiling, and never end: the
breadth-first search that never places the largest square that fits (B1)
queues nothing once only a one-column run is left and loops on an empty
level, and the solution arm that lets no square reach the top (R1) never
completes a tiling, so its cut never tightens. The interpreter stops both
at its step limit; compiled, both were still running at 1500 s.

C1, the cuts arm without 11 x 13 taken as known, fails only P6, on 11 x 13
and 13 x 11: 8 is the best of straight cuts, so P3 holds, and the
statement read literally stops at 6 x 6. It is the one rectangle the cuts
arm cannot find, and only another arm's answer shows it. M2, the memo
keeping each answer under the next skyline's key, answers wrongly when
compiled; under the interpreter the memo saves nothing, the search is
exponential, and the step limit stops it first. M1, the memo reading
heights in base 13, is not caught and is equivalent on these inputs: base
13 runs together only a column of 13 and its left neighbour, and a Python
run of the memo over all 169 rectangles finds no two skylines met in one
search that read the same, so no answer changes.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (backtracking on the skyline) on every rectangle up to 13 x 13, 200
passes; prints the total of the answers and a checksum. Every program
prints `169 rectangles, 200 passes: total 173400, checksum 695938994`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.290 to 1.560 s | 1.344 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.319 to 1.429 s | 1.347 s |
| Rust (`rustc -O`) | 1.156 to 1.283 s | 1.200 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.216 to 1.325 s | 1.274 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.181 to 1.413 s | 1.258 s |
| C (`clang -O3`) | 1.107 to 1.314 s | 1.140 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.105 to 1.375 s | 1.165 s |
| Go | 1.235 to 1.457 s | 1.322 s |
| Python | 33.63 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 5% ahead of Kāra (1.274 s
against 1.347 s), and the two ranges overlap. C is about 15% ahead of
Kāra (1.140 s against 1.347 s); Go runs level with Kāra (1.322 s against
1.347 s). Python takes about 25x Kāra's time. No profile was taken.
