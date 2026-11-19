# 1632. Rank Transform of a Matrix

Given an `m x n` `matrix`, return *a new matrix* `answer` *where*
`answer[row][col]` *is the* ***rank*** *of* `matrix[row][col]`.

The **rank** is an **integer** that represents how large an element is
compared to other elements. It is calculated using the following rules:

- The rank is an integer starting from `1`.
- If two elements `p` and `q` are in the **same row or column**, then:
  - If `p < q` then `rank(p) < rank(q)`
  - If `p == q` then `rank(p) == rank(q)`
  - If `p > q` then `rank(p) > rank(q)`
- The **rank** should be as **small** as possible.

The test cases are generated so that `answer` is unique under the given
rules.

```
matrix = [[1,2],[3,4]]                                      ->  [[1,2],[2,3]]
matrix = [[7,7],[7,7]]                                      ->  [[1,1],[1,1]]
matrix = [[20,-21,14],[-19,4,19],[22,-47,24],[-19,4,19]]    ->  [[4,2,3],[1,3,4],[5,1,6],[1,3,4]]
matrix = [[7,3,6],[1,4,5],[9,8,2]]                          ->  [[5,1,4],[1,2,3],[6,3,1]]
```

**Constraints:** `m == matrix.length`; `n == matrix[i].length`;
`1 <= m, n <= 500`; `-10^9 <= matrix[row][col] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `rank.kara` ★ | the cells sorted and taken one value at a time; a union-find joins each cell to the first cell of that value seen in its row and in its column, each group's rank is one more than the largest rank so far in any of its rows and columns, and those row and column maxima then take it. O(rc log rc) |
| `rank_bfs.kara` | the cells grouped by value in a `SortedMap`; per value, each row and each column is a node and each cell an edge between them, and a breadth-first search gathers each group, with no union-find. O(rc log rc) |
| `rank_topo.kara` | equal cells of one row or column joined into one node, each row's and column's sorted values pointing at the next larger one, and a cell's rank the length of the longest path ending at its node, found in topological order by Kahn's algorithm over a `VecDeque`. O(rc log rc) |
| `rank_solution.kara` | LeetCode's Rust template: a `BTreeMap` from value to cells and, per value, a `UnionFind` struct over rows and columns. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's four examples, one cell,
and a column of one value; then every rank summed and a checksum for
2000 random matrices of up to 4 x 4 with values -3 to 3, 200 of up to
30 x 30 with values -1000 to 1000, and 5 of up to 200 x 200 with values
-5 to 5. `rank.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every rank starts at 1, and any two cells of one row or column
that break a rule are mended, the larger value's rank pushed above the
smaller's and equal values taking the larger of their two ranks, until
nothing changes. Ranks only grow and each step is forced, so what is
left is the smallest ranking that keeps every rule. It checks 3000
random matrices of at most five rows and five columns, every other one
with values -2 to 2, so ties are common, and the rest -50 to 50. Every
matrix is drawn before any arm answers.

| | property |
|---|---|
| P1 | the ranks are the statement read literally |
| P2 | the matrix transposed transposes the ranks |
| P3 | the matrix turned half round turns the ranks the same way |
| P4 | every value mapped by `v -> 3v + 7`, which keeps their order, leaves the ranks |
| P5 | the ranks keep every row's and column's order, equal values equal, the smallest value ranked 1, and none above the number of distinct values |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 663857234, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property. P5 first bounded
a rank by rows + columns - 1, and every arm broke it on
`[[-15, 8], [42, 32]]`, whose ranks run 1, 2, 3, 4 around the square: a
chain of values can wind through the matrix, so the bound is the number
of distinct values.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The first M8 tried, the topological
arm taking a node's rank from its last predecessor rather than the
largest, survived, and is equivalent: Kahn's queue is first-in
first-out, so nodes leave it in order of rank and the last predecessor
taken is always one of the highest. It was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a group's rank from its rows alone | P1 2129, P2 2749, P5 2129, P6 2129 |
| M2 | ★: a group's rank the last cell's, not the largest | P1 441, P2 124, P3 666, P5 441, P6 441 |
| M3 | ★: every cell its own group | P1 1496, P3 1496, P5 1496, P6 1496 |
| M4 | bfs: edges only from rows to columns | panics on both backends: `key not found` |
| M5 | bfs: a group's rank from the smallest of its rows and columns | P1 2796, P5 2796, P6 2796 |
| M6 | bfs: the rows and columns keep one less than the rank | P1 3000, P5 3000, P6 3000 |
| M7 | topo: the lines left unsorted | P1 2612, P3 2825, P5 2612, P6 2612 |
| M8 | topo: every edge reversed | P1 2832, P5 2832, P6 2832 |
| M9 | template: a cell's row joined to the row numbered as its column | P1 215, P3 176, P6 215 |
| M10 | template: a group's best the last cell's, not the largest | P1 441, P2 124, P3 666, P5 441, P6 441 |

## Benchmarks

The bench draws 12 random 300 x 300 matrices of values 0 to 9999, all of
them first, then ranks each by the ★ arm in all five languages, each with
its own hash map for the per-value maps: Kāra's `Map`, Rust's `HashMap`,
Go's `map`, Python's `dict`, and an open-addressing table written out in
C. Every implementation prints `12 matrices of 300 x 300: ranks sum to
589176866, checksum 766437404`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `rank.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `SHA`.

## Writing it

The ★ arm first ended each `match` on a map with
`None => first_in_row.insert(r, id),` beside a block arm. `Map.insert`
returns the `Option` it replaced, so the check refused it, as rustc does
the same code: "match arms have incompatible types: '()' and
'Option[i64]'". The match is the last thing in a `for` body, where its
value is thrown away, so the arm's value can be discarded with braces and
`;`, but `karac fix` had nothing for it and the error points at the
`match` rather than the arm; that is ROWID. The arm writes
`None => { first_in_row.insert(r, id); }`.

The breadth-first arm's `let mut group = vec![r];` drew the deprecation
warning for `vec!`, and `karac fix` wrote the list literal `[r]`. The
topological arm checked clean as first written, a `map` closure over a
row's columns that calls `find(mut parent, ..)` on a captured `parent`
included.

LeetCode's Rust template takes one `karac fix` of 48 edits, among them
`BTreeMap` to `SortedMap` and `HashMap` to `Map` with the `use` line
dropped, `&mut self` to `mut ref self`, the `usize` indices to `i64`,
`for &(i, j) in cells` to `for (i, j) in cells`, `best[&root]` to
`best[root]`, and `vec![0; m + n]` to `Vec.filled(m + n, 0i32)`: the
literal's `i32` comes from `max_rank[i]` passed to `max`, a method,
which does not fix a literal's type (design.md § Literals), so the fix
writes the suffix. The arm then checks and agrees with no hand edit.
