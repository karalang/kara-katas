# 1337. The K Weakest Rows in a Matrix

You are given an `m x n` binary matrix `mat` of `1`'s (representing
soldiers) and `0`'s (representing civilians). The soldiers are
positioned in front of the civilians. That is, all the `1`'s will appear
to the left of all the `0`'s in each row. A row `i` is weaker than a row
`j` if the number of soldiers in row `i` is less than the number of
soldiers in row `j`, or both rows have the same number of soldiers and
`i < j`. Return the indices of the `k` weakest rows in the matrix ordered
from weakest to strongest.

```
mat = [[1,1,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,1,0,0,0],[1,1,1,1,1]], k = 3  ->  [2,0,3]
mat = [[1,0,0,0],[1,1,1,1],[1,0,0,0],[1,0,0,0]], k = 2                      ->  [0,2]
```

**Constraints:** `2 <= m, n <= 100`, `1 <= k <= m`, `mat[i][j]` is
either 0 or 1.

The arms are `fn k_weakest_rows(mat: Vec[Vec[i32]], k: i32) ->
Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `k_weakest_rows.kara` ★ | each row's soldiers counted by a binary search for its first civilian; the (soldiers, row) pairs sorted, which puts ties in row order, and the first k rows kept. O(m log n + m log m) |
| `k_weakest_rows_sum.kara` | each row's soldiers by `sum`, and the row numbers sorted by that count with `sort_by_key`, which is stable, so ties stay in row order; then `truncate(k)`. O(m n + m log m) |
| `k_weakest_rows_heap.kara` | a `PriorityQueue.max_first()` of (soldiers, row) holding the k weakest rows met so far, a weaker row pushing the strongest out; emptied strongest first and read backwards. O(m n + m log k) |
| `k_weakest_rows_columns.kara` | no counting and no sort: the columns walked left to right, a row joining the answer at the column of its first civilian, the rows of one column taken top to bottom, and the rows of nothing but soldiers last. O(m n) |
| `k_weakest_rows_solution.kara` | a Rust solution as LeetCode's Rust users write it (`(r.iter().sum::<i32>(), i)` pairs from `enumerate`, `sort()`, then `take(k as usize)` with the pattern `\|&(_, i)\|`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples, a matrix with
no soldiers, and one of nothing but soldiers (`[2, 0, 3] [0, 2] [0, 1]
[0]`); 100 rows of 100, the constraints' largest, the 5 weakest and the
strongest of all (`100 by 100: weakest [28, 74, 94, 12, 27], strongest
14, checksum 728778677`); and 300 random matrices of 2 to 100 rows and
columns, most of them small, with 0 to n soldiers a row or 0 to 2, and k
from 1 to m (`300 random matrices: checksum 767489937`).
`k_weakest_rows.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run` and
`karac __mir-llvm-run`.

The Mend loop: the sum, heap and columns arms check clean. The ★ arm
draws a warning for `take(k as i64)`, a cast an `i32` does not need on
its way to an `i64`, and `karac fix` drops it. The Rust arm takes one
round of 19 fixes by `karac fix`'s count, from 9 errors: `struct
Solution;` to `struct Solution {}`, each `Vec<..>` to `Vec[..]`, the
pair's `usize` to `i64`, the turbofish in `sum::<i32>()` removed (the
binding's annotation `Vec[(i32, i64)]` already says what the sum is),
`take(k as usize)` to `take(k)`, `|&(_, i)|` to `|(_, i)|`, and
`Solution::` to `Solution.`. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each row's soldiers counted one by one, a row's place the
number of rows weaker than it, by fewer soldiers or as many and a smaller
index, and the rows of the first k places in order. 2000 matrices of 2 to
6 rows and 2 to 6 columns in four kinds, 500 each: 0 to n soldiers a
row; 0 or 1; every row alike; and the rows' counts stepping by 7, taken
modulo n + 1. k runs from 1 to m. Every matrix is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | a civilian added at the end of every row: the same answer |
| P3 | a soldier added at the front of every row: the same answer |
| P4 | every row asked for: m rows, whose first k are the answer |
| P5 | a row of nothing but soldiers added below: the same answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 matrices: checksum 346717623,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, sorting by soldiers and row,
gives the same checksum.

## Mutation testing

Eleven edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. One is left out: the heap arm
counting civilians instead of soldiers fails exactly the checks of the
sum arm sorting strongest first (M3), since with every row the same
length, fewer civilians is more soldiers and both keep ties in row
order. The ten kept, two to each arm, are each killed, fail the same way
under both backends and not by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the search stopped one step early | P1 631, P2 74, P3 673, P6 2524 |
| M2 | ★: ties broken by the later row | P1 1423, P5 336, P6 5692 |
| M3 | sum: the rows sorted strongest first | P1 1299, P5 1634, P6 1299 |
| M4 | sum: one row too many kept | P1 1434, P4 1434, P5 566, P6 1434 |
| M5 | heap: the rows left strongest first | P1 1415, P4 1434, P6 1415 |
| M6 | heap: a smallest-first queue, which keeps the strongest | P1 2000, P5 2000, P6 2000 |
| M7 | columns: the rows of nothing but soldiers never added | P1 336, P2 336, P4 766, P6 336 |
| M8 | columns: a row joining at every civilian after its first | P1 911, P2 431, P3 467, P4 291, P5 198, P6 911 |
| M9 | solution: the rows never sorted | P1 972, P6 972 |
| M10 | solution: one row too few kept | P1 2000, P4 2000, P6 2000 |

P1 and P6 kill all ten, P4 five, P5 five, P2 three and P3 two. Asking
for every row (P4) catches the edits that keep the wrong number of rows
(M4, M10), lose rows (M7, M8), or order the whole answer backwards
(M5). A strong row below (P5) catches the edits that would let it in:
those that favour strong rows or later rows (M2, M3, M6), keep one row
too many (M4), or count a row more than once (M8). A civilian after
every row (P2) makes no row all soldiers, which catches the column walk
that forgets such rows (M7), and with the soldier before (P3) moves
where the binary search stops (M1).

## Benchmarks

The bench builds 50 matrices of 100 by 100, the constraints' largest,
once; then makes 2000 passes, each rewriting one row of every matrix with
a soldier count, and choosing k, from the checksum so far, so no answer
carries over, answering every matrix with the ★ arm and folding the
answer's first and last rows plus the pass into the checksum. Every
language reads the matrix in place. C sorts with `qsort` and Go with
`slices.SortFunc`, the kata convention. Every implementation prints
`2000 passes over 50 matrices of 100 by 100: checksum 33765082`.

BENCHTAB
