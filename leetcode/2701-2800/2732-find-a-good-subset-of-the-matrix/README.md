# 2732. Find a Good Subset of the Matrix

You are given a **0-indexed** `m x n` binary matrix `grid`.

Let us call a **non-empty** subset of rows **good** if the sum of each
column of the subset is at most half of the length of the subset.

More formally, if the length of the chosen subset of rows is `k`, then
the sum of each column should be at most `floor(k / 2)`.

Return *an integer array that contains row indices of a good subset
sorted in **ascending** order.*

If there are multiple good subsets, you can return any of them. If there
are no good subsets, return an empty array.

```
grid = [[0,1,1,0],[0,0,0,1],[1,1,1,1]]  ->  [0, 1]
grid = [[0]]                            ->  [0]
grid = [[1,1,1],[1,1,1]]                ->  []
```

**Constraints:** `1 <= m <= 10^4`, `1 <= n <= 5`, `grid[i][j]` is 0 or 1.

## Approaches

With at most 5 columns, whenever any subset is good, one of one or two
rows is: a row of zeros alone, or two rows with no 1 in the same column.
Every arm looks only for those; the differential checks the claim
against every subset of up to 10 rows.

| file | mechanism |
|---|---|
| `subset.kara` ★ | each row a mask of 5 bits; the first row of each of the 32 masks kept in an `Array[i64, 32]`, a zero mask named at once, then every two disjoint masks tried. O(m n + 32^2) |
| `subset_pairs.kara` | no masks: every row tried alone for all zeros by `all`, then beside every later row, cell by cell, for no column where both hold a 1. O(m^2 n) |
| `subset_scan.kara` | one pass: each row's mask, built by `enumerate` and `fold`, tried against the first row of every mask seen so far, so the pair names the earliest row that completes one. O(m (n + 32)) |
| `subset_complement.kara` | the first row of each mask in a `Map`; a row's partner lies inside the complement of its mask, so each row walks the complement's submasks, `sub = (sub - 1) & rest`, asking the map for each. O(m (n + 2^n)) |
| `subset_solution.kara` | a Rust solution as LeetCode's Rust users write it, each row's mask into a `HashMap` from mask to row, a zero mask returned at once, then every two entries of the map tried, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

The arms may name different good subsets, and the solution arm's walk
over its `Map` is in the per-process hash order, so it may name a
different one on each run. The output therefore says only whether a
subset was named, and checks each one named: it holds rows in ascending
order, in range, and each column of them sums to at most half their
number.

Every arm prints the same 5 lines: LeetCode's three examples, each with
one answer only; 3000 random grids of 1 to 10 rows and 1 to 5 columns;
and 30 grids of 1000 rows and 5 columns, each batch with how many had a
good subset, how many named were not good, and a checksum of which had
one. In one grid of three, one column is set in every row, so no subset
is good; in another, in every row but one.
`subset.py` mirrors the ★ arm and its output is byte-identical.

```
[0, 1]
[0]
[]
3000 small grids: 1197 with a good subset, 0 named not good, checksum 564060142
30 grids of 1000 rows: 18 with a good subset, 0 named not good, checksum 854122031
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every non-empty subset of the rows, as the bits of a number,
with each column's sum over it held to half its size; no masks of rows
and no pairs. It draws 1000 random grids of 1 to 10 rows and 1 to 5
columns, then 200 of up to 300 rows, all before any arm answers; the
literal reading is asked only of the first 1000.

| | property |
|---|---|
| P1 | up to 10 rows, a subset is named exactly when the literal reading finds one good |
| P2 | the subset named is good: ascending, in range, each column at most half its size |
| P3 | the rows listed in reverse order: a subset named or not, the same |
| P4 | the columns rotated by one: a subset named or not, the same |
| P5 | a row of all ones added at the end: a subset named or not, the same |
| P6 | each arm agrees with at least three of the other four on whether a subset is named |

The differential prints `1200 cases: checksum 779790341, 36000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by `itertools.combinations` over every subset
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed. Nine fail the
same checks under both backends; M9, in the solution arm, fails P2 345
times under one and 340 under the other, since which two masks it pairs
first follows its `Map`'s walk, a fresh hash order in every process, so
a wrong pair is named in some runs and a right one in others. The other
counts of M9 do not depend on which pair is named.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the mask of column 0 alone never paired | P1 42, P4 52, P6 49 |
| M2 | ★: a row of zeros not named alone | P1 177, P6 192 |
| M3 | pairs: any two rows taken as apart | P1 507, P2 757, P5 91, P6 608 |
| M4 | pairs: neighbouring rows never paired | P1 22, P6 22 |
| M5 | scan: the pair named with the later row first | P2 246 |
| M6 | scan: partners with the last column never tried | P1 10, P3 20, P4 11, P6 10 |
| M7 | complement: the submask 1 never asked | P1 11, P3 25, P4 22, P6 11 |
| M8 | complement: each column's bit one place up | P1 34, P3 65, P4 50, P6 34 |
| M9 | solution: two masks sharing column 0 taken as apart | P1 232, P2 340 to 345, P4 318, P6 276 |
| M10 | solution: columns 2j and 2j + 1 share a bit | P1 80, P4 78, P6 93 |

## Benchmarks

The bench draws 100 grids of `10^4` rows by 5 columns, LeetCode's
largest, of the same three kinds as the harness, so that about half of
them have no good subset and are read to the end, all of them
first, then answers each 10 times by the ★ arm in all five languages.
C keeps each grid as one flat array; the others keep a vector of rows.
Every implementation prints `100 grids of 10000 rows, 10 rounds: 480
good subsets found, checksum 948815936`.

BENCHTAB

## Verification

All five arms print the same output as `subset.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, pairs and scan arms checked clean as first written. The
complement arm wrote Rust's `full & !mask`; `karac check` refuses `!`
with "use `not` for a bool, `~` for an integer's bitwise complement",
and `karac fix` made it `~mask`.

LeetCode's Rust template took one `karac fix` of 27 edits, the wrapper
included: the `use std::collections::HashMap` became `struct Solution
{}`, `HashMap<i32, i32>` and `HashMap::new()` became `Map[i32, i32]` and
`Map.new()`, `Vec<..>` became `Vec[..]`, the `&x`, `&a`, `&i` patterns
dropped their `&`, `vec![..]` became an array literal and `vec![]`
became `Vec.new()`, `let mut mask = 0` gained `: i32`, since a mask
built from `i32` cells is one, and `Solution::` became `Solution.`.
