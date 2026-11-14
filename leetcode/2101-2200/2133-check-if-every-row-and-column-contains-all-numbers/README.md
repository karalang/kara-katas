# 2133. Check if Every Row and Column Contains All Numbers

An `n x n` matrix is **valid** if every row and every column contains
**all** the integers from `1` to `n` (**inclusive**).

Given an `n x n` integer matrix `matrix`, return `true` if the matrix is
**valid**. Otherwise, return `false`.

```
matrix = [[1,2,3],[3,1,2],[2,3,1]]  ->  true
matrix = [[1,1,1],[1,2,3],[1,2,3]]  ->  false
```

**Constraints:** `n == matrix.length == matrix[i].length`;
`1 <= n <= 100`; `1 <= matrix[i][j] <= n`.

Every value is 1 to n, so a line of n values holds all of them exactly
when it holds none twice: the question is whether any row or column has
a repeat. O(n^2).

## Approaches

| file | mechanism |
|---|---|
| `valid.kara` ★ | one `Vec[i64]` of marks for all 2n lines: a value is marked with the number of the line it was last seen in, and is a repeat when its mark is the current line's, so the table is never cleared |
| `valid_sets.kara` | each row and column collected into a `Set[i64]`, judged by a closure: n of them, all in range |
| `valid_sorted.kara` | each line copied out to an `own Vec[i64]` parameter, sorted in place there and compared with `1..n + 1` collected; `all` over the rows |
| `valid_struct.kara` | a `struct Tally` of counts for one line: `add` and `clear` (`mut ref self`), `whole` (`ref self`), cleared between lines |
| `valid_bits.kara` | each line's values as bits in a `Vec[u64]`, value v at bit v - 1, read through a `Fn(i64) -> i64` closure so that one function serves rows and columns; a bit set twice is a repeat, and the line is whole when every full word is `u64.MAX` and the last its low `n % 64` bits |
| `valid_solution.kara` | LeetCode's Rust template: a `HashSet` for row i and for column i filled side by side, `!insert` for a repeat; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one cell, a square of two, its rows equal so its columns fail, and its
columns equal so its rows fail), each with its answer; then the count
valid and a checksum over 2000 random matrices of order 1 to 6, in turn
values of 1 to n at random, a Latin square, and a Latin square with one
cell redrawn; then the constraints' largest, order 100: a Latin square,
the same with two cells of a row swapped, and every row 1 to 100.
`valid.py` mirrors the ★ arm and its output is byte-identical.

No compiler gap was met. `karac fix` carries the template in three
rounds of 19, 2 and 1 edits: Rust's spellings (the `use` dropped, `<..>`
to `[..]`, `HashSet::new` to `HashSet.new`, `!` to `not` and `||` to
`or`, `struct Solution;` to `struct Solution {}`, the adapter's `&Vec`
to `ref Vec` and its `|&v|` to `|v|`, `Solution::` to `.`); then
`HashSet` to `Set`; then the `ref` dropped from the adapter's parameter,
which borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every row and every column, each number of 1 to n is
looked for along it; nothing is counted and no repeat is looked for. It
checks 300 random matrices of order 1 to 5, in turn values of 1 to n at
random, a Latin square, and a Latin square with one cell redrawn; then
30 Latin squares with two cells of a row swapped; then 30 of order 1 to
3 at random; then 30 Latin squares of order 60 to 70, across a 64-bit
word, every other one with a cell redrawn. All 390 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the matrix transposed: the same answer |
| P3 | the rows in reverse order: the same answer |
| P4 | the columns turned by one, the first moved last: the same answer |
| P5 | every value v made n + 1 - v: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `390 matrices (199 valid): checksum 60266990,
14040 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python reading
of the same matrices. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Twenty-nine edits to the differential, four to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the columns never checked | P1 22, P2 26, P6 22 |
| M2 | ★: a row and its column sharing a mark | P1 199, P6 199 |
| M3 | ★: each row's last value never checked | P1 4, P2 17, P6 4 |
| M5 | sets: a line of n - 1 values enough | P1 134, P6 134 |
| M7 | sets: the column read along the diagonal | P1 116, P2 17, P3 25, P4 2, P6 116 |
| M8 | sets: the first row alone | P1 50, P3 30, P4 44, P6 50 |
| M9 | sorted: a line unsorted | P1 115, P6 115 |
| M11 | sorted: one row good enough | P1 94, P3 16, P4 19, P6 94 |
| M12 | sorted: a line compared without its last | P1 12, P5 24, P6 12 |
| M14 | struct: whole when any value counted | P1 191, P6 191 |
| M15 | struct: the value 1 never asked | P1 20, P5 41, P6 20 |
| M27 | struct: the tally never cleared after a column | P2 6 |
| M18 | bits: the full mask one bit short | P1 198, P6 198 |
| M19 | bits: a full word asked for one bit less | P1 9, P6 9 |
| M28 | bits: every value set in the first word | P1 8, P6 8 |
| M24 | solution: the adapter dropping the last row | P1 74, P3 41, P4 33, P6 74 |
| M25 | solution: the adapter folding values past n | P1 75, P6 75 |

P1 and P6 kill sixteen, P2 four, P3 four, P4 four and P5 two. The
transpose swaps rows with columns, so P2 sees an edit that checks the
two unlike: the columns left out (M1), each row's last value (M3), a
column read along the diagonal (M7). P3 and P4 move rows and columns
about, which sees an edit that looks at one place rather than every
line: the first row alone (M8), one row enough (M11), the diagonal (M7)
and the adapter's lost last row (M24). P5 relabels the values, which
sees an edit that treats one value unlike the rest, the value 1 (M15)
or the value n (M12). The rest are wrong on the matrix and on each of
its rearrangements alike, and fail P1 alone.

M27 is the one that P1 does not see. Without the clear after column i,
row i + 1 is counted on top of column i's tally, so when that column was
whole, row i + 1 looks whole whatever it holds. Among the 390 that never
changes an answer, but among their transposes it calls six valid that
are not; P2 alone kills it.

Of the twenty-nine, twelve were not kept. Two are equivalent, both in
the bits arm: the repeat never looked for, since a line of n values of
1 to n without one of them has a gap that the full mask then sees; and
only the first word asked, since without a repeat the n values fill
every bit and the first word is full only when the rest are. None
survives otherwise, and none fails by a crash. Nine fail as a kept one
does: seven ways of never checking the columns, the ★ arm reading its
column as the row, the sets arm and the template never asking the
column's set, the sorted and bits arms reading the row again, and the
struct arm's tally cleared but never judged after a row or after a
column, as M1; the template's sets made once for all lines as M9; and
the bits arm's repeat looked for in the first word as M28. One is killed
with checks of its own but was left out because its arm keeps its share:
the struct arm's value n never asked (P1 21, P5 41, P6 21).

## Verification

Every arm prints the same output as `valid.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 s to 0.5 s and the
differential 7.6 s, nearly all of it the literal reading of the 30
squares of order 60 to 70.

## Benchmarks

The bench builds 10 Latin squares of order 100 once, then solves 20000
times, each solve of one square: on an odd round two of its rows are
swapped for good, which keeps it valid, and on an even round two cells
of a row are swapped for the solve and back after, with the ★ arm in all
five languages. Every implementation prints `20000 solves: 10088 valid,
checksum 772937774`.

BENCHTAB
