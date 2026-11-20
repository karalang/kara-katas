# 1219. Path with Maximum Gold

In a gold mine `grid` of size `m x n`, each cell holds an integer, the
amount of gold in it, or `0` if it is empty. Return the most gold you can
collect under these conditions:

- Every time you are in a cell you collect all the gold in it.
- From your position you can walk one step left, right, up or down.
- You cannot visit the same cell more than once.
- Never visit a cell with `0` gold.
- You can start and stop collecting gold from any position in the grid
  that has some gold.

```
grid = [[0,6,0],[5,8,7],[0,9,0]]                       ->  24   9 -> 8 -> 7
grid = [[1,0,7],[2,0,6],[3,4,5],[0,3,0],[9,0,20]]      ->  28   1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7
```

**Constraints:** `1 <= m, n <= 15`; `0 <= grid[i][j] <= 100`; at most 25
cells hold gold.

The arms are `fn get_maximum_gold(grid: Vec[Vec[i64]]) -> i64`. The two
Rust arms keep the method LeetCode gives Rust users, on `i32`, inside
`impl Solution`, and a one-line `get_maximum_gold` narrows the cells and
calls it.

## Approaches

| file | mechanism |
|---|---|
| `path_with_maximum_gold.kara` ★ | a depth-first search from every cell with gold, through a `mut ref` grid: a step takes the cell's gold and sets it to 0 while the search goes on from it, so the path never comes back, and puts it back on the way out. At most 25 cells hold gold, so the search is small however large the grid |
| `path_with_maximum_gold_mask.kara` | the gold cells numbered in reading order, each with the list of its neighbours with gold; a path grows cell by cell with the cells it holds as the bits of an `i64`, so the grid is never written |
| `path_with_maximum_gold_stack.kara` | no recursion: a stack of partial paths, each a struct of its last cell, the cells it holds as a `Set` of positions, and the gold it has; every path popped is a candidate, and pushes one longer path for each neighbour with gold it does not hold yet |
| `path_with_maximum_gold_corners.kara` | the ★ arm's search, started only at gold cells with at most two neighbours with gold (see below) |
| `path_with_maximum_gold_grid.kara` | a Rust solution as LeetCode's Rust users write it (the grid taken as `mut grid`, a `dfs(grid: &mut Vec<Vec<i32>>, i: usize, j: usize)` that zeroes and restores the cell, and the four bounds written out as `i > 0` and `i + 1 < grid.len()`), carried to Kāra by `karac fix` |
| `path_with_maximum_gold_visited.kara` | another Rust solution (the grid only read, the path held in a `HashSet<(usize, usize)>`, each neighbour found by `checked_add_signed` in a `let ... else`, and `grid.get(ni).and_then(\|row\| row.get(nj))` for the bounds), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

The corners arm rests on a claim: some best path always starts at a gold
cell with at most two neighbours with gold. A best path never starts
beside gold it does not visit, since that gold in front of it would make
it richer, but that alone does not settle a start whose three or four
neighbours are all visited later. The claim is checked here, not proven:
against the search from every cell, over every shape of a 4×4, 3×5 and
2×7 grid with one gold in each cell it holds, 20,000 random grids up to
5×5 with gold from 1 to 100, and 5,000 dense ones from 3×3 to 4×5 with
gold of 1 or 100, it never differs; the differential checks it again on
every case. Such a start always exists: the first gold cell in reading
order has no gold above it or to its left.

Every arm prints the same 13 lines: LeetCode's two examples (`24`,
`28`); `[[0]]` (`0`); `[[5]]` (`5`); a 2×2 grid with no gold (`0`) and
one all ones (`4`); four cells of 100 none of which touch (`100`); one
row, 1 to 5 (`15`); 1000 random grids up to 4×4, each cell empty one time
in three, else holding 1 to 100 (`1000 grids up to 4 by 4: gold total
181211, checksum 451035536`); and four grids of 15×15 with 25 cells of
gold, the constraints' most: scattered at random (`104`), a full 5×5
block, the search's worst case at about three million paths (`1329`),
one bent line (`1231`), and none next to another (`25`).
`path_with_maximum_gold.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, mask, stack and corners arms check clean as
written. The grid arm takes one round of 28 fixes (among them `mut grid:
Vec<Vec<i32>>` to `grid: own Vec[Vec[i32]]` with `let mut grid = grid;`
as the body's first line, `&mut Vec<Vec<i32>>` to `mut ref
Vec[Vec[i32]]`, `i: usize` to `i: i64`, `Self::dfs(&mut grid, i, j)` to
`Solution.dfs(mut grid, i, j)`, `let mut best = 0` to `let mut best: i32
= 0`, and `&&` to `and`). The visited arm takes one round of 39
fixes: the same kinds, `HashSet::new()` to `Set.new()`, `[(isize, isize);
4]` to `Array[(i64, i64), 4]`, `Some(&g)` to `Some(g)` with `.cloned()`,
and `i.checked_add_signed(di)` to `i.checked_add(di).filter(|v| v >= 0)`,
which keeps what the Rust meant once `i` is an `i64`: a step off the top
or left edge is `None`.

## Gaps

The visited arm found one, fixed in kara B-2026-11-18-59 at 2e40b2fffa. `karac
fix` turns a `usize` index into an `i64`, and a call that leans on
`usize` stopping at zero changed with it. `i.checked_add_signed(di)` was
left as written and had no method on `i64`, so the arm could not be
fixed; worse, `i.checked_sub(1)` and `i.saturating_sub(1)` kept
compiling and quietly stopped catching the step below zero. The fix now
rewrites each of these four calls on a retyped index to keep the floor:
`.filter(|v| v >= 0)` after a checked call, `.max(0)` after a
saturating one.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of gold cells that one walk visits each exactly
once, as a mask over the gold cells, built up from the one-cell sets by
adding a neighbour of a cell the walk can end at, and the richest such
set. 2000 random cases of at most 10 cells, 1 to 3 rows and as many
columns as keep it to 10, each cell empty one time in three, else holding
1 to 20; in 1570 of them the best path holds more than one cell, and in
67 there is no gold.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the grid transposed gives the same |
| P3 | every row reversed gives the same |
| P4 | every cell's gold doubled doubles the answer |
| P5 | a cell's gold taken away never raises the answer |
| P6 | between the richest cell and all the gold |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 870032653,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, every walk of every set of gold cells, gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a cell's gold never put back | P1 267, P2 224, P3 310, P5 9, P7 1335 |
| S2 | ★: the search goes only down and right | P1 584, P3 717, P7 2920 |
| M1 | mask: a vertical pair recorded on one side only | P1 101, P2 133, P7 101 |
| M2 | mask: the start not held | P1 1595, P6 1230, P7 1595 |
| K1 | stack: a path's last cell left out of its gold | P1 1933, P6 408, P7 1933 |
| K2 | stack: paths started in the first row only | P1 277, P2 760, P6 199, P7 277 |
| C1 | corners: a start needs at most one neighbour with gold | P1 127, P5 92, P6 119, P7 127 |
| C2 | corners: a start needs three or more | P1 1834, P6 1578, P7 1834 |
| G1 | grid: the neighbour below never tried | P1 101, P2 133, P7 101 |
| G2 | grid: the right-hand bound read off the row count | stops: index out of bounds |
| V1 | visited: a step into row 0 or column 0 refused | P1 1444, P3 668, P7 1444 |
| V2 | visited: the cell left held after the search comes back | P1 267, P2 224, P3 310, P5 9, P7 267 |

G2 is caught before any property: on a grid with more rows than columns
its bound lets the search index past the end of a row, and both
backends stop with `runtime error: index out of bounds` at the same
place. A mutation of the ★ arm fails P7 on all six arms, the ★ arm
against the other five. P4 catches none: doubling every cell's gold
doubles every mutant's answer too. P2, the grid transposed, catches the
five that treat rows and columns differently (M1, K2, G1) or that
depend on the order the search tries cells in (S1 and V2, both leaving
a cell spent after the walk that spent it, the same fault in two arms
with the same counts). P3, every row reversed, catches S2 and V1, which
treat the two ends of a row differently, and S1 and V2 again. P6
catches the five that change which walks are searched, from where (C1,
C2, K2) or with what counted (M2, K1). P5 catches S1, V2 and C1, where
taking gold away gives a richer answer.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a depth-first search from every cell with gold that zeroes a cell
while the search goes on from it and puts its gold back on the way out)
on 160 grids of 15 by 15, the constraints' most, each holding one blob
of 25 cells with gold, the most they allow, grown at random and drawn
once; every answer folded into a checksum. Every program prints `160
grids of 15 by 15, one blob of 25 cells with gold each: gold total
192106, checksum 735331015`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.569 to 0.669 s | 0.603 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.575 to 0.733 s | 0.623 s |
| Rust (`rustc -O`) | 0.608 to 0.750 s | 0.651 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.645 to 0.852 s | 0.686 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.638 to 0.754 s | 0.670 s |
| C (`clang -O3`) | 0.558 to 0.678 s | 0.580 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.554 to 0.633 s | 0.583 s |
| Go | 0.809 to 1.096 s | 0.890 s |
| Python | 35.02 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 9% ahead of Rust with overflow checks on (0.623 s
against 0.686 s), and the two ranges overlap. C is about 7% ahead of
Kāra (0.580 s against 0.623 s); Kāra is about 30% ahead of Go (0.623 s
against 0.890 s). Python takes about 56x Kāra's time. No profile was
taken.
