# 2713. Maximum Strictly Increasing Cells in a Matrix

Given a **1-indexed** `m x n` integer matrix `mat`, you can select any
cell in the matrix as your **starting cell**.

From the starting cell, you can move to any other cell **in the same
row or column**, but only if the value of the destination cell is
**strictly greater** than the value of the current cell. You can repeat
this process as many times as possible, moving from cell to cell until
you can no longer make any moves.

Your task is to find the **maximum number of cells** that you can visit
in the matrix by starting from some cell.

Return *an integer denoting the maximum number of cells that can be
visited.*

```
mat = [[3,1],[3,4]]         ->  2
mat = [[1,1],[1,1]]         ->  1
mat = [[3,1,6],[-9,5,7]]    ->  4
```

**Constraints:** `1 <= m, n <= 10^5`, `1 <= m * n <= 10^5`,
`-10^5 <= mat[i][j] <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `increasing.kara` ★ | a path only climbs, so the longest one ending at a cell is one more than the longest ending anywhere in its row or column at a smaller value. The cells sorted by value as `(value, row, column)` tuples are taken one value at a time: each row's and column's best so far answers every cell of the value, and only then are the answers recorded, so that equal values never extend each other. O(m n log(m n)) |
| `increasing_descending.kara` | the same idea run backwards: the longest path starting at a cell is one more than the longest starting anywhere in its row or column at a larger value, so the cells are taken from the largest value down, sorted by `sort_by` on the value reversed. O(m n log(m n)) |
| `increasing_map.kara` | the cells grouped by value in a `SortedMap[i64, Vec[(i64, i64)]]`, whose walk visits the values in order; each group's lengths are worked out in full before the rows' and columns' bests take them. O(m n log(m n)) |
| `increasing_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `BTreeMap<i32, Vec<(usize, usize)>>` of the cells by value, `vec![0; m]` bests, a scratch `Vec` of lengths per value, and `*row.iter().max().unwrap()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; one cell;
300 by 300 rising along rows and down columns; a row of `10^5` equal
values, LeetCode's most cells; a column of `10^5` falling values; then
the cells summed and a checksum for 1000 random matrices up to 8 by 8
with values from -10 over a random spread up to 20, and 20 up to 200 by
200 with values from `-10^5` to `10^5`. `increasing.py` mirrors the ★
arm and its output is byte-identical.

```
2
1
4
1
599
1
100000
1000 small matrices: cells sum to 5833, checksum 591379995
20 matrices up to 200 by 200: cells sum to 7720, checksum 684524081
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: from every cell, every move the statement allows tried, to
any cell of the same row or column with a strictly greater value, the
most cells a path visits remembered per cell, with no sorting. It checks
800 random matrices of up to 6 by 6 with values over a spread of 1 to
12 about zero, then 10 of up to 100 by 100 with values from `-10^5` to
`10^5`. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 6 by 6, the answer is the literal reading's |
| P2 | the matrix transposed: the same answer |
| P3 | every value v made 2 v + 7: the same answer |
| P4 | every value negated: the same answer, each path walked backwards |
| P5 | the answer is at least the distinct values of any one row and at most the distinct values of the matrix |
| P6 | each arm agrees with at least two of the other three |

The differential prints `810 cases: checksum 591642250, 19440 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the same 800 small cases, path by path, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. P3 kills none of them: no edit here
looks at a value other than to order it. One first choice was
equivalent and was replaced: the descending arm's cells sorted smallest
first turns it into the ★ arm's reading, the longest path ending at each
cell rather than starting there, and the largest of those is the same
answer.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each answer recorded as soon as it is found | P1 637, P4 333, P5 543, P6 637 |
| M2 | ★: a cell's column never read | P1 444, P2 532, P6 454 |
| M3 | descending: the cells ordered by row, not value | P1 512, P2 63, P5 352, P6 522 |
| M4 | descending: the column's best never raised | P1 444, P2 532, P6 454 |
| M5 | map: a value's group joined with the next value's | P1 800, P5 790, P6 810 |
| M6 | map: the answer the largest column | P1 487, P2 543, P4 267, P5 282, P6 497 |
| M7 | solution: a cell's row never read | P1 423, P2 532, P5 254, P6 433 |
| M8 | solution: each length kept for its row only | P1 444, P2 532, P6 454 |
| M9 | ★: equal values grouped one cell at a time | P1 637, P4 333, P5 543, P6 637 |
| M10 | descending: the length starts at 0 | P1 800, P5 810, P6 810 |

## Benchmarks

The bench draws 10 matrices of 300 by 300, values below a random spread
of 10 to `10^4`, so values repeat, all of them first, then answers each
10 times by the ★ arm in all five languages; each answer sorts 90000
cells. The sort is each language's own: Kāra's `Vec.sort` and Rust's
`sort` on tuples, Go's `sort.Slice` and C's `qsort` with a comparator
on the three fields, Python's `list.sort`. Every implementation prints
`10 matrices of 300 by 300, 10 rounds: cells sum to 84710, checksum
829254502`.

BENCHTAB

## Verification

All four arms print the same output as `increasing.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The harness's row of `10^5` equal values, written
`max_increasing_cells([(0..100000).map(|_| 7).collect()].to_vec())`,
passed `karac check` but failed to lower in every arm: the bare
`collect()` inside the array literal never took the element type the
argument's `Vec[Vec[i64]]` gave it. That was kara `B-2026-11-20-138`, fixed in the
compiler at `0d28296389`; the harness keeps the natural spelling.

The ★, descending and map arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 22 edits: the `use
std::collections::BTreeMap;` became `struct Solution {}`,
`BTreeMap<i32, Vec<(usize, usize)>>` became `SortedMap[i32, Vec[(i64,
i64)]]`, `.or_default()` became `.or_insert(Vec.new())`, `vec![0; m]`
became `Vec.filled(m, 0i32)`, `Vec::with_capacity` became
`Vec.with_capacity`, and the `&(i, j)` patterns dropped their `&`. The
wrapper's `as i64` on the `i32` answer was dropped, since it widens by
itself.
