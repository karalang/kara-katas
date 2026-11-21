# 2503. Maximum Number of Points From Grid Queries

You are given an `m x n` integer matrix `grid` and an array `queries`
of size `k`.

Find an array `answer` of size `k` such that for each integer
`queries[i]` you start in the **top left** cell of the matrix and
repeat the following process:

- If `queries[i]` is **strictly** greater than the value of the current
  cell that you are in, then you get one point if it is your first time
  visiting this cell, and you can move to any **adjacent** cell in all
  `4` directions: up, down, left, and right.
- Otherwise, you do not get any points, and you end this process.

After the process, `answer[i]` is the **maximum** number of points you
can get. **Note** that for each query you are allowed to visit the same
cell **multiple** times.

Return *the resulting array* `answer`.

```
grid = [[1,2,3],[2,5,7],[3,5,1]], queries = [5,6,2]  ->  [5,8,1]
grid = [[5,2,1],[1,1,2]],         queries = [3]      ->  [0]
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`2 <= m, n <= 1000`; `4 <= m * n <= 10^5`; `k == queries.length`;
`1 <= k <= 10^4`; `1 <= grid[i][j], queries[i] <= 10^6`.

A query's points are the cells of the region joined to the top-left
cell through cells below the query, and the regions only grow as the
query rises. So the queries can be answered in increasing order by one
region that grows, or each cell can be given the least query that
reaches it, its bottleneck: the least, over the paths from the top-left
cell, of the greatest value on the path. The approaches differ in which
of the two they build, and how.

## Approaches

| file | mechanism |
|---|---|
| `points.kara` ★ | the queries in increasing order and one growing region, its border in a least-first `PriorityQueue` of (value, cell); a query takes in every border cell below it. O(m n log(m n) + k log k) |
| `points_minimax.kara` | every cell's bottleneck by a Dijkstra over (bottleneck, cell), sorted, then each query one `partition_point`. O(m n log(m n) + k log(m n)) |
| `points_union.kara` | a union-find: the cells switched on in increasing order of value while the queries rise, each joining its switched-on neighbours, the answer the size of the top-left cell's set; `find` halves the path, `union` by size, both through `mut ref Vec` parameters |
| `points_rec.kara` | the same switching on, with a recursive `find` that points the whole path at the root, and each new root hung under the other |
| `points_iter.kara` | iterators: the values in the order a growing region takes the cells, `scan`ned to the running greatest, the level each cell needs; each query `map`ped to the `partition_point` of that rising sequence |
| `points_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` and `Vec<i32>` in, `Vec<i32>` out; the queries' indices sorted by value, the border in a `BinaryHeap` of `Reverse((value, row, column))`, drained by `while let Some(&Reverse(..)) = heap.peek()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and six
more; then 1000 random grids of 2 to 8 rows and columns, values to 10
and to `10^6`, with 1 to 10 queries to one past the top, each as a
checksum; then the constraints' largest: 316 by 316 random with `10^4`
random queries; 100 by 1000 of walls a snake must wind through, with
`10^4` rising queries; and 2 by 50000 sevens. `points.py` mirrors the ★
arm and its output is byte-identical, and the mirror was checked on
3000 random grids of 2 to 6 rows and columns against a flood for each
query, and the two agreed on every query.

`check` first reports 18 errors on the template, all Rust's spellings:
the `use std::cmp::Reverse;` and `use std::collections::BinaryHeap;`
lines, `struct Solution;`, four `Vec<..>` in angle brackets,
`BinaryHeap::new`, the `&` patterns of `|&i|`, `for &i`, `Some(&Reverse(..))`
and `for &(dr, dc)`, the two `&` borrows, three `&&` and one `!`.
`karac fix` carries it in one call, reporting 36 edits: both `use`
lines go, since a `PriorityQueue` pops the smallest first and needs no
`Reverse`, and every `Reverse(..)` around a pushed tuple goes with them;
`BinaryHeap::new()` becomes `PriorityQueue.new()`; `struct Solution
{}` and the brackets; `vec![..]` becomes `Vec.filled(..)`; the `usize`
indices and the `as usize` casts become `i64`, and the `0usize`
literals plain `0`; `while let Some(&Reverse((v, r, c))) = heap.peek()`
becomes `while let Some((v, r, c)) = heap.peek().cloned()`; `for i in
ref idx` and `for (dr, dc) in ref dirs`; and `and` and `not`. The `i32`
offsets of the directions stand.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each query on its own, a flood from the top-left cell
through the cells below the query, counted, 0 when the top-left cell is
not below it. Nothing is sorted and no query sees another. It checks
300 random grids of 2 to 6 rows and columns, values to 5 or to 1000,
with 1 to 8 queries; then 20 of 2 by 2; and 40 of 10 by 10 with values
to 20 and 10 queries. All 360 are drawn before any arm answers; they
ask 1785 queries, of which the statement answers 912 with 0 and 203
with every cell.

| | property |
|---|---|
| P1 | every answer is the statement read literally |
| P2 | every answer from 0 to `m n`, and 0 exactly when the top-left cell is not below the query |
| P3 | the queries in the other order: the answers in the other order |
| P4 | the grid transposed: the same answers |
| P5 | every value `v` written `2 v` and every query `q` written `2 q - 1`: the same answers |
| P6 | each arm agrees with at least three of the other five |

P5 holds because for integers `v < q` exactly when `2 v < 2 q - 1`, so
each query lets in the same cells; it catches an arm that lets in a
cell equal to its query, which the odd queries never meet.

The differential prints `360 cases, 912 answers of 0: checksum
255296365, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and runs the same floods. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a query's own value let in | P1 179, P2 108, P5 179, P6 179 |
| M2 | ★: the queries unsorted | P1 240, P2 196, P3 255, P6 240 |
| M3 | ★: only rows walked | P1 273, P4 248, P6 273 |
| M7 | minimax: the start pushed at 1 | P1 266, P2 266, P6 266 |
| M9 | minimax: the bottlenecks unsorted | P1 201, P4 176, P6 201 |
| M10 | minimax: the levels summed | P1 281, P6 281 |
| M12 | union: sizes never added | P1 282, P6 282 |
| M14 | union: only down and right joined | P1 276, P6 276 |
| M16 | union: the size read at cell 0 | P1 266, P4 20, P6 266 |
| M17 | rec: a join counted twice | P1 282, P2 261, P4 166, P6 282 |
| M19 | rec: only up and left joined | P1 259, P6 259 |
| M21 | rec: the answer every cell on | P1 146, P6 146 |
| M22 | iter: the level the latest value | P1 297, P2 235, P4 88, P6 297 |
| M24 | iter: the border taken greatest first | P1 216, P4 9, P6 216 |
| M25 | iter: the level begun at 5 | P1 112, P2 112, P5 99, P6 112 |
| M28 | solution: the count begun at 1 | P1 360, P2 319, P6 360 |
| M29 | solution: three directions | P1 83, P4 110, P6 83 |

P1 and P6 kill all seventeen, P2 and P4 seven each, P5 two, and P3
one.

Two of the first thirty-one edits were replaced. The rec arm's set
joined to itself doubled a set's size at every join within it, until
the size overflowed and the run stopped with Kāra's overflow check,
which is a crash, so it became the root hung the other way (M18). The
iter arm's level the latest value was first written `Some((v, v))`,
and `check` refuses it with the bare E0200 that the 2501 kata records:
`v` is the `ref i64` the iteration gives, the state an `i64`, and the
message says neither; it became `Some((*v, *v))` (M22).

Fourteen are not kept, and none survives. Seven fail exactly as a kept
one: the ★ arm's count begun at 1 (M4) as the template's (M28); the
minimax, union, iter and template arms' query that reaches its own
value (M11, M13, M23, M27) as the ★ arm's (M1); the rec arm's root hung
the other way (M18) as the union arm's sizes never added (M12), each
leaving a set's size at a cell that is no longer its root; and the
template's queries unsorted (M31) as the ★ arm's (M2). Six fail as one
another, in three pairs: the ★ arm's start pushed at 0 and the union
arm's top-left asked even when off (M5, M15), each answering for a
top-left cell the query does not reach; the ★ and rec arms' every query
one lower (M6, M20); and the minimax arm's neighbour's own value
ignored and the template's neighbour pushed at the start's value (M8,
M30). The iter arm's start left unseen (M26) fails in a way of its own,
but its arm already holds its kept edits.

## Verification

Every arm prints the same output as `points.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 3.5 to 24.3 s and the differential 5.0 s; under `karac __mir-llvm-asan` the arms take 1.7 to 3.3 s and the differential 1.4 s; and under `karac run` the differential takes 1.0 s.

## Benchmarks

The bench builds 4 grids of 316 by 316 with values to `10^6` and `10^4`
queries to `10^6` once from its own generator, then makes 14 passes.
Each pass, for every grid, sets the cell at row `check % 316` and
column `check / 316 % 316` to `(check + p) % 10^6 + 1`, asks every
query, and puts the cell back, folding each answer plus the pass into
the checksum. The bench uses the ★ arm in all five languages: Kāra's
`PriorityQueue`, Rust's `BinaryHeap` of `Reverse`, Python's `heapq`,
and in C and Go a hand-written binary heap of (value, cell). Kāra,
Rust, Go and Python build their region's arrays afresh on every ask; C
allocates its heap, its marks and its order once and clears them. Every
implementation prints `14 passes over 4 grids of 316 by 316, 10^4
queries: checksum 358610374`.

BENCHTAB
