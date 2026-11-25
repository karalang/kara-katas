# 1329. Sort the Matrix Diagonally

A matrix diagonal is a diagonal line of cells starting from some cell in
either the topmost row or leftmost column and going in the bottom-right
direction until reaching the matrix's end. For example, the matrix
diagonal starting from `mat[2][0]`, where `mat` is a `6 x 3` matrix,
includes cells `mat[2][0]`, `mat[3][1]`, and `mat[4][2]`. Given an
`m x n` matrix `mat` of integers, sort each matrix diagonal in ascending
order and return the resulting matrix.

```
mat = [[3,3,1,1],[2,2,1,2],[1,1,1,2]]  ->  [[1,1,1,1],[1,2,2,2],[1,2,3,3]]
mat = [[11,25,66,1,69,7],[23,55,17,45,15,52],[75,31,36,44,58,8],[22,27,33,25,68,4],[84,28,14,11,5,50]]
    ->  [[5,17,4,1,52,7],[11,11,25,45,8,69],[14,23,25,44,58,15],[22,27,31,36,50,66],[84,28,75,33,55,68]]
```

**Constraints:** `1 <= m, n <= 100`, `1 <= mat[i][j] <= 100`.

The arms are `fn diagonal_sort(mat: Vec[Vec[i32]]) -> Vec[Vec[i32]]`;
the two carried from Rust take `mat: own Vec[Vec[i32]]`, as `karac fix`
writes Rust's `mut mat` parameter.

## Approaches

| file | mechanism |
|---|---|
| `diagonal_sort.kara` ★ | each diagonal, from its start on the top row or the left column, read into a `Vec`, sorted, and written back along the same cells. O(m n log min(m, n)) |
| `diagonal_sort_count.kara` | the values run from 1 to 100, so each diagonal is sorted by counting how many of each value it holds, then refilled from 1 up. O(m n + 100 (m + n)) |
| `diagonal_sort_insertion.kara` | each diagonal sorted where it lies, by insertion: every cell's value carried up its diagonal past the larger values above it, with no list of its own. O(m n min(m, n)) |
| `diagonal_sort_heap.kara` | every value pushed into a `PriorityQueue` kept for its diagonal in a `Map` keyed by `i - j`; then the cells visited row by row, which meets each diagonal from its top, each taking the smallest value its queue has left. O(m n log min(m, n)) |
| `diagonal_sort_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<i32, Vec<i32>>` keyed by `i as i32 - j as i32`, each list sorted largest first with `sort_unstable_by(\|a, b\| b.cmp(a))`, then every cell given its list's `pop()`), carried to Kāra by `karac fix` |
| `diagonal_sort_walk.kara` | a second Rust solution as LeetCode's Rust users write it (each diagonal's start walked with `let (mut r, mut c) = (i, j)`, its values gathered into a `Vec`, `sort()`ed, and written back by a second walk), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's two examples; one cell, one
row and one column, which no sort changes (`[7] [5,4,3] [3][2][1]`); a
100 by 100, the constraints' largest, each row counting down (`100 by
100: corners 4 1 7 100, checksum 178186121`); and 300 random matrices of
1 to 100 rows and columns, most of them small, with values from 1 to 100,
1 to 3, or all 1 (`300 random matrices: 91136 cells, checksum
981068579`). `diagonal_sort.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms check clean. The first Rust arm takes
one round of 23 fixes by `karac fix`'s count, from 10 errors: the `use
std::collections::HashMap;` line deleted, `struct Solution;` to `struct
Solution {}`, `mut mat: Vec<Vec<i32>>` to `mat: own Vec[Vec[i32]]` with
`let mut mat = mat;` in the body, `HashMap<i32, Vec<i32>>` to `Map[i32,
Vec[i32]]`, each `::` path to `.`, `sort_unstable_by` to `sort_by`, and
`get_mut(&(..))` to `get_mut(..)`. The second takes one round of 23 fixes
from 12 errors: the same `struct`, `Vec` and `::` rewrites, `usize` to
`i64`, `for &(i, j)` to `for (i, j)`, each `let (mut r, mut c)` to `let
mut (r, c)`, `&&` to `and`, and the parameter to `own`. Both outputs
match on the first run.

The harness was first written with Rust's habit for test data, `let ex1:
Vec[Vec[i32]] = [[3, 3, 1, 1].to_vec(), ...].to_vec();`, and `check`
refused each such line with "expected 'Vec[Vec[i32]]', found
'Vec[Vec[i64]]'" and the advice to annotate the binding, which already
was annotated (kara B-2026-11-24-43). A list literal is already a `Vec`
where a `Vec` is wanted, so the harness writes `[[3, 3, 1, 1], ...]`.
Since kara bfee4ce6ba the `.to_vec()` form checks too: the literals
behind it take the wanted `i32`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a cell's diagonal is every cell with the same row less column,
and sorted ascending, the cell holds the value whose place in that order
is the number of its diagonal's cells above it. 2000 matrices of 1 to 6
rows and columns in four kinds, 500 each: values from 1 to 100; from 1 to
3; all one value; and every row counting down from a random start. Every
matrix is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the matrix turned over its main diagonal: the answer turned |
| P3 | every diagonal ascending, with the values it held, by count and by sum of squares |
| P4 | sorted again: no change |
| P5 | a border of 1 above and to the left and of 100 below and to the right: the answer in the same border |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 matrices: checksum 444620509,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python, sorting each diagonal, gives the same
checksum.

## Mutation testing

Fourteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Two are left out: the count arm
refilling each diagonal from its second row runs past the matrix and
stops with an index out of bounds, and the first Rust arm sorting each
list smallest first fails exactly the checks of the heap arm visiting the
rows from the bottom (M7), since both give every diagonal in descending
order. The twelve kept, two to each arm, are each killed, fail the same
way under both backends and not by a crash, and no two fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each diagonal read short of the last column | P1 852, P2 845, P3 852, P5 852, P6 4260 |
| M2 | ★: the diagonal from the second column never sorted | P1 569, P2 748, P3 569, P6 2845 |
| M3 | count: the 100s never written back | P1 45, P3 45, P4 16, P6 45 |
| M4 | count: each value counted once however often it comes | P1 233, P3 233, P5 929, P6 233 |
| M5 | insertion: the second column never inserted | P1 798, P2 835, P3 798, P4 208, P5 798, P6 798 |
| M6 | insertion: a value never carried to the diagonal's top | P1 917, P3 917, P5 917, P6 917 |
| M7 | heap: the rows visited from the bottom | P1 1022, P3 1022, P5 2000, P6 1022 |
| M8 | heap: the first column left as it was | P1 1012, P2 979, P3 1012, P4 391, P5 2000, P6 1012 |
| M9 | solution: a diagonal of two cells or fewer left unsorted | P1 727, P3 727, P4 998, P5 2000, P6 727 |
| M10 | solution: each value kept one more | P1 2000, P3 2000, P4 2000, P5 2000, P6 2000 |
| M11 | walk: the main diagonal never walked | P1 724, P3 724, P6 724 |
| M12 | walk: a diagonal read no further than its fourth cell | P1 130, P3 130, P5 333, P6 130 |

P1, P3 and P6 kill all twelve, P5 nine, P4 five and P2 four. The border
(P5) lengthens every diagonal by a 1 at its start and a 100 at its end,
so it catches the edits that lose track of a diagonal's ends or order:
read short of the last column (M1), a value never carried to the top
(M6), the rows met from the bottom (M7), and a diagonal cut at its fourth
cell (M12), which the border makes longer. Sorting again (P4) catches only
the edits whose answer a second pass changes: the 100s dropped (M3), a
column or a short diagonal left unsorted (M5, M8, M9), and a value grown
by one (M10). Turning the matrix over (P2) catches the edits that treat
the top row and the left column differently (M1, M2, M5, M8) and misses
those that go wrong on both alike.

## Benchmarks

The bench builds 8 matrices of 300 by 300 with values from 1 to 100 once,
then makes 100 passes, each setting one cell of every matrix from the
checksum so far, so no answer carries over, answering it with the ★ arm
and folding two of the answer's cells plus the pass into the checksum.
Each call copies the matrix into fresh rows and takes a fresh list for
each diagonal in every language. C sorts with `qsort` and Go with
`slices.Sort`, the kata convention, and both trail: on a shared Linux
container with two compiler gates running, C took 5.0 s, Go 4.4 s, Rust
1.4 s and Kāra 0.9 s. `qsort` calls its comparator through a pointer for
every comparison, where Rust's and Kāra's sorts compare `i32`s inline.
Every implementation prints `100 passes over 8 matrices of
300 by 300: checksum 484357434`.

BENCHTAB
