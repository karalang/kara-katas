# 2500. Delete Greatest Value in Each Row

You are given an `m x n` matrix `grid` consisting of positive integers.

Perform the following operation until `grid` becomes empty:

- Delete the element with the greatest value from each row. If multiple
  such elements exist, delete any of them.
- Add the maximum of deleted elements to the answer.

**Note** that the number of columns decreases by one after each
operation.

Return *the answer after performing the operations described above*.

```
grid = [[1,2,4],[3,3,1]]  ->  8
grid = [[10]]             ->  10
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`1 <= m, n <= 50`; `1 <= grid[i][j] <= 100`.

The `k`-th round deletes the `k`-th largest value of every row, so with
each row sorted the rounds are the columns, and each round adds the
greatest value of its column. The order a row's values leave in is all
that matters: which of equal values goes first changes nothing. The
approaches differ in how they put each row's values in order.

## Approaches

| file | mechanism |
|---|---|
| `greatest.kara` ★ | every row of a copy sorted, then each column's greatest summed. O(m n log n) |
| `greatest_remove.kara` | the statement as written: each round finds every row's greatest, takes it out with `swap_remove`, and adds the round's greatest. O(m n^2) |
| `greatest_heap.kara` | one `PriorityQueue.max_first_from` per row, each round popping every queue and adding the greatest popped. O(m n log n) |
| `greatest_count.kara` | each row counted into 101 buckets and read back from 100 down, the `k`-th value read raising the `k`-th column's greatest. O(m (n + 100)) |
| `greatest_iter.kara` | iterators: every row `map`ped to a sorted copy, each column `map`ped to the `max` of its rows' values, and the columns `sum`med |
| `greatest_solution.kara` | LeetCode's Rust template: `mut grid: Vec<Vec<i32>>` in, `i32` out; every row `sort_unstable()`d through `iter_mut()`, then each column's `max` summed; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and six
more; then 2000 random grids of 1 to 12 rows and columns with values to
100, and 2000 with values to 3, each as a checksum; then the
constraints' largest, 50 by 50: every value 100; each row `r` holding
`(c + r) % 50 + 1` in column `c`; and a checksum over 20 random grids.
`greatest.py` mirrors the ★ arm and its output is byte-identical, and
the mirror was checked on 5000 random grids of 1 to 6 rows and columns
against a simulation of the rounds, and the two agreed on every grid.

`check` first reports 3 errors on the template: `struct Solution;`, the
`mut grid` parameter, and `Vec<Vec<i32>>`. `karac fix` carries it in
one call, reporting 8 edits: `struct Solution {}`; the brackets; the
parameter becomes `grid: own Vec[Vec[i32]]` with `let mut grid = grid;`
as the body's first line; `sort_unstable()` becomes `sort()`; and the
wrapper's lossless `as i64` on the answer is dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: round by round, each row's greatest is found by a scan, the
row rebuilt without the first value equal to it, and the greatest of
the deleted values added, until the rows are empty. Nothing is sorted.
It checks 300 random grids of 1 to 6 rows and columns, values to 3 or
to 100; then 20 of a single cell; and 40 of 10 by 10 with values to 100.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | at least the grid's greatest value and at most `n` times it |
| P3 | the rows in reverse order: the same answer |
| P4 | every row reversed: the same answer |
| P5 | every row followed by a copy of itself: twice the answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the first round deletes the grid's greatest and every
round adds no more than it. P5 holds because each value then leaves
twice, in two rounds running, with its copy in every other row beside
it.

The differential prints `360 cases: checksum 986236992, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs the same rounds. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the rows left unsorted | P1 210, P6 210 |
| M2 | ★: the least kept, from 0 | P1 360, P2 360, P6 360 |
| M6 | ★: the first row left unsorted | P1 174, P3 183, P4 187, P5 184, P6 174 |
| M7 | remove: only the last round counted | P1 296, P2 289, P5 360, P6 296 |
| M9 | remove: the second value never asked | P1 162, P4 126, P5 162, P6 162 |
| M10 | remove: the last row's value for the round | P1 227, P2 28, P3 269, P6 227 |
| M12 | heap: the total begun at 1 | P1 360, P2 71, P5 360, P6 360 |
| M13 | heap: one round fewer | P1 360, P2 64, P5 360, P6 360 |
| M16 | heap: every round begun at 50 | P1 299, P2 170, P6 299 |
| M17 | count: the first value never counted | P1 360, P2 87, P4 244, P5 360, P6 360 |
| M18 | count: a bucket read once whatever its count | P1 149, P5 360, P6 149 |
| M19 | count: 100 never read | P1 50, P2 1, P6 50 |
| M23 | iter: the least of each column | P1 291, P2 82, P6 291 |
| M24 | iter: the first row's column only | P1 231, P2 37, P3 269, P6 231 |
| M26 | iter: the greatest column only | P1 296, P5 360, P6 296 |
| M29 | solution: the last column left out | P1 360, P2 122, P5 360, P6 360 |
| M30 | solution: only the first row sorted | P1 202, P3 152, P4 144, P5 138, P6 202 |

P1 and P6 kill all seventeen, P2 eleven, P5 ten, and P3 and P4 four
each.

Three of the first thirty-one edits survived, and all three are
equivalent: the remove arm taking out each row's least instead of its
greatest, the heap arm's queues made least-first, and the count arm
reading its buckets from the bottom. Each deletes the rows' values in
the opposite order, so round `k` becomes round `n - 1 - k`, and the sum
over the rounds is the same. They were replaced by the remove arm's
only the last round counted (M7), the heap arm's total begun at 1
(M12), and the count arm's first value never counted (M17), and the
edits above are the replacements.

Fourteen are not kept, and none survives. All fail exactly as a kept
one: the ★, heap and template arms' first row's column only (M3, M15,
M31) as the iter arm's (M24); the ★ arm's first column left out, the
remove arm's last round skipped, the count arm's last column dropped and
the iter arm's first column left out (M4, M11, M21, M25) as the heap
arm's one round fewer (M13); the ★ arm's only the last column kept (M5)
as the iter arm's greatest column only (M26); the remove arm's round's
least added from 0 (M8) as the ★ arm's least kept (M2); the heap and
count arms' last row's value for the round (M14, M20) as the remove
arm's (M10); the iter and template arms' rows left unsorted (M22, M27)
as the ★ arm's (M1); and the template's least of each column (M28) as
the iter arm's (M23).

## Verification

Every arm prints the same output as `greatest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 to 2.9 s and the differential 2.0 s; under `karac __mir-llvm-asan` the arms take 0.5 to 1.1 s and the differential 0.8 s; and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench builds 1000 grids of 50 by 50 with values to 100 once from its
own generator, then makes 32 passes. Each pass, for every grid, sets the
cell at row `check % 50` and column `check / 50 % 50` to `(check + p) %
100 + 1`, asks, and puts it back, folding the answer plus the pass into
the checksum. The bench uses the ★ arm in all five languages, each
sorting a fresh copy of the grid on every ask. Every implementation
prints `32 passes over 1000 grids of 50 by 50: checksum 930526004`.

BENCHTAB
