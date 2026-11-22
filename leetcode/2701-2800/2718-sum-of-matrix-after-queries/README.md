# 2718. Sum of Matrix After Queries

You are given an integer `n` and a **0-indexed** **2D array** `queries`
where `queries[i] = [type_i, index_i, val_i]`.

Initially, there is a **0-indexed** `n x n` matrix filled with `0`'s.
For each query, you must apply one of the following changes:

- if `type_i == 0`, set the values in the row with `index_i` to `val_i`,
  overwriting any previous values.
- if `type_i == 1`, set the values in the column with `index_i` to
  `val_i`, overwriting any previous values.

Return *the sum of integers in the matrix after all queries are
applied*.

```
n = 3, queries = [[0,0,1],[1,2,2],[0,2,3],[1,0,4]]           ->  23
n = 3, queries = [[0,0,4],[0,1,2],[1,0,1],[0,2,3],[1,2,1]]   ->  17
```

**Constraints:** `1 <= n <= 10^4`, `1 <= queries.length <= 5 * 10^4`,
`queries[i].length == 3`, `0 <= type_i <= 1`, `0 <= index_i < n`,
`0 <= val_i <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `matrix.kara` ★ | a cell keeps the value of the last query that set its row or its column, so the queries are read from the last back: a row not set by a later query fills every column not yet taken by a later one, and is taken itself; a column likewise. A line met again earlier is overwritten later and adds nothing. O(n + q) |
| `matrix_times.kara` | forward, each row and column remembers the time and value of the last query that set it. A row then holds its own value in each column set before it and the column's value in each set after: the columns sorted by time, with suffix sums of their values, answer each row by a binary search for its time. O(q + n log n) |
| `matrix_set.kara` | the walk from the last query back, with the lines already set later kept as `(kind, index)` pairs in one `Set` whose `insert` says whether the pair is new; each kind's count of lines left is n less the pairs of that kind seen. O(n + q) with the hashing |
| `matrix_fold.kara` | the same walk back written as one `fold` over `queries.iter().rev()`, its state a struct of the lines taken and the sum so far. O(n + q) |
| `matrix_solution.kara` | a Rust solution as LeetCode's Rust users write it, two `HashSet<i32>`s of the rows and columns seen, `queries.iter().rev()`, and an `i64` sum from `i32` values, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one cell;
`10^4` by `10^4`, LeetCode's largest, one row set to `10^5`; every row
and then every column of `10^4` set, the columns last; then the sums
summed and a checksum for 2000 random cases of 1 to 8 rows and up to 20
queries of values up to 10, and 40 of up to `10^4` rows and `5 * 10^4`
queries of values up to `10^5`. `matrix.py` mirrors the ★ arm and its
output is byte-identical.

```
23
17
7
1000000000
9500050000000
2000 small cases: sums sum to 187025, checksum 615836027
40 large cases: sums sum to 56194685520247, checksum 940588687
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: an n by n matrix of zeros, each query written into every cell
of its row or column in turn, and the cells summed at the end, with no
reading backwards. It checks 1000 random cases of 1 to 6 rows and up to
15 queries of values up to 5, then 30 of up to 300 rows and 2000
queries of values up to `10^5`. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | up to 6 rows, the answer is the literal reading's |
| P2 | every query's kind flipped, rows for columns: the same answer |
| P3 | each query written twice in a row: the same answer |
| P4 | every value doubled: the answer doubled |
| P5 | every row set to v by n queries appended: n * n * v |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1030 cases: checksum 538958475, 30900 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same 1000 small cases, cell by cell, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. Two first choices for the times arm were
equivalent and were replaced: the rows' times counted from 0 rather than
1, and the first column set at the row's time or after rather than
strictly after. No row and column query share a time, so neither
changes a comparison that matters.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a row set later added again | P1 432, P2 658, P3 787, P5 787, P6 462 |
| M2 | ★: a column fills the rows taken, not those left | P1 762, P2 946, P5 858, P6 792 |
| M3 | times: the row's own value counted in every column | P1 615, P2 809, P6 645 |
| M4 | times: the search never finds no column set after the row | P1 421, P2 846, P5 873, P6 433 |
| M5 | set: a line taken counted for its own kind | P1 805, P5 946, P6 835 |
| M6 | set: the queries read first to last | P1 799, P5 904, P6 829 |
| M7 | fold: a column fills the columns left | P1 654, P2 911, P5 724, P6 684 |
| M8 | fold: a row never marked taken | P1 432, P2 658, P3 787, P5 787, P6 462 |
| M9 | solution: the rows seen kept with the columns | P1 758, P2 909, P5 863, P6 788 |
| M10 | solution: a value counted once per line, not per cell | P1 709, P2 920, P5 858, P6 739 |

## Benchmarks

The bench draws 40 cases of `5 * 10^4` queries on `10^4` rows, values
up to `10^5`, LeetCode's largest, all of them first, then answers each
20 times by the ★ arm in all five languages. The queries are a vector of
three-element vectors in Kāra, Rust, Go and Python, LeetCode's shape,
and a flat array of triples in C. Every implementation prints `40 cases
of 50000 queries on 10000 rows, 20 rounds: sums mod p sum to
423318253800, checksum 896320205`.

BENCHTAB

## Verification

All five arms print the same output as `matrix.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four arms of our own checked clean as first written.

LeetCode's Rust template took one `karac fix` of 26 edits, the wrapper
included: the `use std::collections::HashSet;` became `struct Solution
{}`, `Vec<Vec<i32>>` became `Vec[Vec[i32]]`, `HashSet<i32>` and
`HashSet::new()` became `Set[i32]` and `Set.new()`, the `&v` closure
pattern dropped its `&`, and `Solution::` became `Solution.`. Its
`v as i64 * (n as i64 - cols.len() as i64)` became `v * (n -
cols.len())`: the `i32` value and row count widen to `i64` by
themselves against the `i64` length.
