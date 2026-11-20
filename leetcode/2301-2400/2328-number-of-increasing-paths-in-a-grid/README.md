# 2328. Number of Increasing Paths in a Grid

You are given an `m x n` integer matrix `grid`, where you can move from
a cell to any adjacent cell in all `4` directions.

Return *the number of **strictly** **increasing** paths in the grid
such that you can start from **any** cell and end at **any** cell.*
Since the answer may be very large, return it **modulo** `10^9 + 7`.

Two paths are considered different if they do not have exactly the
same sequence of visited cells.

```
grid = [[1,1],[3,4]]  ->  8
grid = [[1],[2]]      ->  3
```

**Constraints:** `1 <= m, n <= 1000`; `1 <= m * n <= 10^5`;
`1 <= grid[i][j] <= 10^5`.

The paths starting at a cell are the one of that cell alone and, for
each neighbour holding more, every path starting at that neighbour.
Larger values come first along any path, so counting the cells from the
largest value down finds every neighbour's count already made. O(m n
log(m n)) with the sort, O(m n) by memoized search.

## Approaches

| file | mechanism |
|---|---|
| `paths.kara` ★ | the cells as `(value, row, column)` sorted and reversed, largest first; each cell's count one plus its larger neighbours', and every count added up |
| `paths_memo.kara` | top down: a recursive `from` counts the paths starting at a cell, memoized in a table passed by `mut ref`, 0 for not yet counted |
| `paths_topo.kara` | Kahn's order: each cell waits on its smaller neighbours, the cells with none start in a `VecDeque`, and each cell leaving hands its count of paths ending there to its larger neighbours |
| `paths_naive.kara` | every path walked: a depth-first walk from each cell counts one for every cell it reaches, with nothing remembered. O(the number of paths) |
| `paths_iter.kara` | iterators: flat cell indices `sort_by_key` on the negated value, then a `fold` keeping the counts in a flat `Vec`, each cell's one plus the `sum` of the neighbours `filter` keeps |
| `paths_solution.kara` | LeetCode's Rust template: a memoized `dfs` nested in the method over `&Vec<Vec<i32>>` and a `&mut` table of `i64`, `usize` indices checked through `as i32`, and an `i32` answer; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one cell; a
3 by 3 of equal values; a row of 1 to 10; 300 by 300 with values from
1 to 100; then 1000 random grids of 1 to 6 by 1 to 6 with values from
1 to 5, with a checksum and the counts in all. `paths.py` mirrors the ★
arm and its output is byte-identical.

The harness's row of 1 to 10 was first written
`count_paths([(1..=10).collect()].to_vec())`. `karac check` refuses it
with the MIR builder's own words, `an expression whose type does not
lower (Type(UnknownParam("C"))) is not lowered yet`: the parameter's
type does not reach the `collect` inside the array, though the same
expression after `let g: Vec[Vec[i64]] =` builds and runs. Ledger row
B-2026-11-18-93 records it; the harness names the row first, `let row: Vec[i64]
= (1..=10).collect();`.

`karac fix` carries the template in one call, reporting 44 edits.
`check` first reports seventeen errors and offers 20 edits for them:
the brackets of every `Vec<..>`; `&Vec` to `ref Vec` and `&mut Vec`
to `mut ref Vec` in `dfs`; the four `&&` to `and`; the nested `fn dfs`,
which captures nothing, moved above `impl Solution`; the `&` and
`&mut` at the outer call to `dfs` dropped and marked `mut`; `struct
Solution;` to `struct Solution {}`; and, in the harness's wrapper, the
pattern `|&v|` to `|v|` and `Solution::` to `Solution.`. The rest follow
from those: `dfs`'s indentation taken off; its `i: usize` and `j:
usize` to `i64`, the type of an index, and the six `as usize` on its
indices dropped; the `ref` on `grid` dropped, since a bare parameter
already borrows; `memo` marked `mut` at the call inside `dfs`;
`vec![vec![0i64; n]; m]` to `Vec.filled`, and the suffixes of its
`0i64`, `res`'s `1i64` and `ans`'s `0i64` dropped; and the wrapper's
`as i64` on the `i32` answer. Two `as usize` inside parentheses leave
`(ni) < grid.len()` and `(nj) < grid[0].len()`, which stand.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every path is kept as its list of cells, the single cells
first and then each path grown by every neighbour of its last cell that
holds more, level by level until none grows, all of them put in a
`Set` of lists; the answer is how many different lists it holds. No
counts carried from cell to cell. It runs up to 25 cells. It checks 300
random grids of 1 to 5 by 1 to 5 with values from 1 to 6; then 30 of 1
to 6 by 1 to 6 with values from 1 to 3, where neighbours tie often;
then 30 of up to 30 by 30 with values from 1 to 1000. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | up to 25 cells, the answer is the literal reading's |
| P2 | the answer is at least `m n`, and is `m n` exactly when no two neighbouring cells differ |
| P3 | the grid turned a quarter clockwise: the same answer |
| P4 | every value `v` replaced by `1001 - v`: the same answer, each path walked backwards |
| P5 | every value doubled: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 548294618, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and walks every path by recursion into a `set` of
tuples. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cells taken smallest first | P1 218, P6 243 |
| M2 | ★: an equal neighbour counted as larger | P1 224, P2 9, P3 168, P4 220, P6 235 |
| M5 | ★: the paths of one cell not added | P1 335, P2 143, P6 360 |
| M7 | memo: each cell counted twice alone | P1 335, P2 19, P6 360 |
| M8 | memo: the last row never a neighbour | P1 280, P2 53, P3 299, P4 257, P6 305 |
| M10 | memo: the memo one more than the count | P1 316, P3 183, P4 209, P6 341 |
| M12 | topo: an equal neighbour waited on | P1 224, P2 189, P4 208, P6 235 |
| M13 | topo: only the first larger neighbour handed paths | P1 245, P2 221, P3 191, P4 266, P6 270 |
| M14 | topo: each hand-over counted twice | P1 295, P2 173, P3 37, P4 249, P6 320 |
| M17 | naive: the walk only right and down | P1 290, P2 25, P3 244, P4 284, P6 315 |
| M18 | naive: each longer path counted twice | P1 316, P6 341 |
| M21 | naive: no step up to 1000 or more | P4 244, P5 30, P6 2 |
| M22 | iter: the cells taken smallest first | P1 316, P2 341, P6 341 |
| M24 | iter: an equal neighbour counted as larger | P1 224, P2 9, P3 168, P4 207, P6 235 |
| M26 | iter: every value taken modulo 7 | P1 6, P4 28, P5 217, P6 30 |
| M29 | solution: the first row never a neighbour | P1 283, P2 50, P3 300, P4 255, P6 308 |
| M31 | solution: no path started in the first column | P1 335, P2 122, P3 324, P4 245, P6 360 |

P6 kills all seventeen, P1 sixteen, P2 and P4 twelve, P3 nine and P5
two. P1 misses the naive arm's step up to 1000 or more: values reach
1000 only in the 30 by 30 grids, past the literal reading's 25 cells,
and there seldom; P4's `1001 - v` turns every 1 into 1000 and P5's
doubling passes 1000 often. P5 fails only for the two edits that do
arithmetic on the values, that bound and the values taken modulo 7.
P3, the grid turned, catches the edits that favour a direction or a
side: a row or column never a neighbour or never a start, one step left
out, an equal neighbour counted, and the handing on that stops at the
first neighbour in the table's order; it misses those that treat every
direction alike. P4, the values turned round so each path runs
backwards, fails nearly as widely, and passes where an edit is the same
both ways: the cells taken smallest first, the single cells left out
or counted twice, every longer path counted twice. P2
misses the edits whose counts stay at least `m n` and still `m n` on a
flat grid: the cells smallest first in the ★ arm, the memo one more,
every longer path counted twice, and the two that do arithmetic on the
values.

Of the thirty-one, fourteen were not kept. Four groups fail alike, and
none of them is kept: no path of one cell in the ★ (M3) and template
(M27) arms; the step up never taken in the ★ (M4), iter (M23) and
template (M28) arms; the last column never a neighbour in the ★ (M6)
and naive (M19) arms; and a step up by 1 not taken in the memo (M9) and
template (M30) arms. The memo arm's no path started on the last row
(M11), the topo arm's equal neighbour handed paths (M15) and left
neighbour never waited on (M16), the naive arm's no walk begun on the
first row (M20) and the iter arm's first cell not counted (M25) fail
apart from every kept one, and were left out to keep three to an arm.

## Verification

Every arm prints the same output as `paths.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, memo, topo and template arms take 1.1 to
1.3 s, the iter arm 2.2 s and the naive arm, which walks each of the
300 by 300 grid's 680205 paths one by one, 4.1 s. The differential
takes 4.7 s there and 1.1 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 grids of 250 by 400 with values from 1 to 1000
once, then makes 3 passes counting the paths of every grid, with the ★
arm in all five languages. Every implementation prints `3 passes over
10 grids of 10^5 cells: checksum 640244643`. Each sorts the cells as
triples of 64-bit integers, largest first: Kāra's `sort` and Rust's
`sort` then a reverse, Go's `sort.Slice` and C's `qsort` with the order
turned round in the comparison, and Python's `sort`; and keeps the
counts in a fresh grid for every call.

BENCHTAB
