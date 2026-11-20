# 2397. Maximum Rows Covered by Columns

You are given an `m x n` binary matrix `matrix` and an integer
`numSelect`.

Your goal is to select exactly `numSelect` **distinct** columns from
`matrix` such that you cover as many rows as possible.

A row is considered **covered** if all the `1`'s in that row are also
part of a column that you have selected. If a row does not have any
`1`s, it is also considered covered.

More formally, let us consider `selected = {c1, c2, ...., cnumSelect}`
as the set of columns selected by you. A row `i` is **covered** by
`selected` if:

- For each cell where `matrix[i][j] == 1`, the column `j` is in
  `selected`.
- Or, no cell in row `i` has a value of `1`.

Return the **maximum** number of rows that can be **covered** by a set
of `numSelect` columns.

```
matrix = [[0,0,0],[1,0,1],[0,1,1],[0,0,1]], numSelect = 2  ->  3
matrix = [[1],[0]], numSelect = 1                          ->  2
```

**Constraints:** `m == matrix.length`; `n == matrix[i].length`; `1 <=
m, n <= 12`; `matrix[i][j]` is either `0` or `1`; `1 <= numSelect <=
n`.

With at most 12 columns there are at most 4096 sets of columns, so
every set of the right size can be tried.

## Approaches

| file | mechanism |
|---|---|
| `rows.kara` ★ | each row as the mask of its 1s; every mask of columns with `numSelect` bits (`count_ones`) tried, a row covered when its mask is inside. O(2^n * m) |
| `rows_gosper.kara` | Gosper's hack: only the masks with `numSelect` bits are visited, each the next larger one with as many. O(C(n, k) * m) |
| `rows_search.kara` | backtracking: each column chosen or not while choices remain, and at the end every row checked cell by cell against a `Vec[bool]`; no bit operations |
| `rows_combos.kara` | combinations in order as `k` increasing indexes, the rightmost that can still rise raised and those after it reset; a row covered when its 1s in the chosen columns are all its 1s |
| `rows_iter.kara` | iterators: the rows' masks by `enumerate` and `fold`, every mask `filter`ed to `numSelect` bits, each `map`ped to the rows it holds, and the `max` |
| `rows_solution.kara` | LeetCode's Rust template: the rows folded into `u32` masks, every `0u32..(1 << n)` tried with `count_ones`, the covered rows counted through `\|&&r\|`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; a grid of
0s, every column chosen, and a row of all 1s against one of a single 1;
then a sparse and a dense 12 by 12 grid for every choice of 1 to 12
columns, as a checksum; then 2000 random grids of 1 to 8 rows and 1 to
8 columns, with a checksum and the total. `rows.py` mirrors the ★ arm
and its output is byte-identical, and the mirror was checked on 5000
random grids of up to 6 by 6 against every set of columns.

`rows_gosper.kara` was first written `mask & !chosen == 0`, Rust's
complement; `check` names `!` as no operator in Kāra, and `karac fix`
writes `~`, the complement for an integer, taking the operand's type.

`check` first reports 5 errors on the template, and `karac fix` carries
it in one call, reporting 9 edits: `struct Solution;` given its braces;
`Vec<Vec<i32>>` and `Vec<u32>` their brackets; the `&` of `|m, (j, &v)|`
and the `&&` of `|&&r|` dropped; and `let mut ans = 0;` given the `i32`
it is returned as. `0u32`, `count_ones`, `fold` over `enumerate`, the
`as` casts and the shifts stand as Kāra. `karac fmt` then drops the
parentheses of `(v as u32) << j`, `0u32..(1 << n)` and `(r & mask) ==
r`, which Kāra's precedence does not need.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every sequence of `numSelect` column indexes, the ones
strictly increasing kept as the sets of distinct columns, and a row
covered when each of its 1s is in a column of the set. No masks. It
checks 300 random grids of 1 to 8 rows and 1 to 6 columns, which the
literal reading answers; then 30 of up to 12 rows and 12 columns,
dense; then 30 of up to 12 rows and 12 columns, sparse. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 6 columns, the answer is the literal reading's |
| P2 | at least the rows of all 0s and at most every row, and every row when every column is chosen |
| P3 | the rows in reverse order: the same answer |
| P4 | the columns in reverse order: the same answer |
| P5 | one more column chosen, while there is one: the answer or more |
| P6 | each arm agrees with at least three of the other five |

P3 and P4 hold because neither the rows' order nor the columns' names
change which sets cover which rows, and P5 because a set with one more
column covers every row the smaller one did.

The differential prints `360 cases: checksum 249947219, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every combination. On a failure it prints the
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
| M2 | ★: one column too few chosen | P1 205, P2 106, P6 214 |
| M3 | ★: a row covered by any chosen 1 | P1 233, P2 92, P6 251 |
| M5 | ★: the last choice kept | P1 81, P4 105, P6 92 |
| M7 | gosper: the first choice one bit high | P1 228, P2 142, P4 70, P5 61, P6 243 |
| M8 | gosper: a row covered when it misses the choice | P1 223, P2 130, P5 118, P6 241 |
| M10 | gosper: the next choice the ripple alone | P1 50, P4 59, P6 58 |
| M13 | track: a dead end counting one row | P1 57, P6 63 |
| M14 | track: a chosen column not counted | P1 279, P2 229, P6 297 |
| M16 | track: every column taken | P1 78, P4 105, P6 88 |
| M17 | combos: a row of 0s not counted | P1 151, P2 105, P6 157 |
| M19 | combos: the reset indexes all equal | P1 6, P5 1, P6 10 |
| M21 | combos: the first row never counted | P1 230, P2 151, P3 44, P6 242 |
| M22 | iter: choices of more columns let in | P1 153, P6 167 |
| M23 | iter: a row covered when it holds the choice | P1 275, P2 139, P5 99, P6 298 |
| M24 | iter: the fewest rows kept | P1 122, P6 135 |
| M27 | solution: the choices of other sizes tried | P1 257, P2 106, P5 49, P6 273 |
| M30 | solution: the counts summed | P1 132, P2 128, P5 79, P6 145 |

P1 and P6 kill all seventeen, P2 ten, P5 six, P4 four and P3 one. P3,
the rows reversed, fails only the edit that never counts the first row
(M21): reversed, a different row is first. P4, the columns reversed,
fails the edits that do not try every set of columns alike: the last
choice kept rather than the best (M5), the first choice a bit high
(M7), the next choice the ripple alone (M10), and every column taken
(M16). P5, one more column, fails the edits whose answer can drop when a
column is added (M7, M8, M19, M23, M27, M30). P2, the bounds, passes the
seven whose answers stay between the rows of all 0s and every row (M5,
M10, M13, M16, M19, M22, M24).

Of the thirty-one, fourteen were not kept. The ★ arm's and the
template's each 1 a column to the right (M1, M29) fail alike, and apart
from every kept one; so do the last column never chosen or reached in
the ★, gosper and iter arms (M4, M9, M26). The search arm's row refused
by a chosen column (M12) fails as the gosper arm's row covered when it
misses the choice (M8); the gosper arm's every 1 in the first column,
the search arm's column left chosen and the iter arm's every 1 in the
first column (M11, M15, M25) as the iter arm's choices of more columns
let in (M22); and the template's row covered when it holds the choice
(M28) as the iter arm's (M23). The ★ arm's each row's 0s taken for its
1s (M6), the combos arm's each chosen 1 counted twice (M20) and the
template's every column never chosen at once (M31) each fail apart from
every kept one, and were left out to keep three to an arm and two to
the template. The combos arm's last column never reached (M18) indexed
past its array and stopped with a runtime error under both backends; a
crash is not kept.

## Verification

Every arm prints the same output as `rows.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.45 to 0.79 s. The differential
takes 3.0 s there and 0.60 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 200 grids of 12 by 12, each cell 1 with chance one in
2 to 5, once from the harness's generator, then makes 10 passes,
answering every grid for every choice of 1 to 12 columns and folding
each answer plus the pass into the checksum, with the ★ arm in all five
languages. Every implementation prints `10 passes over 200 grids of 12
by 12, every choice: checksum 834909952`. C counts bits with
`__builtin_popcountll`, Go with `bits.OnesCount64`, and Kāra and Rust
with `count_ones`.

BENCHTAB
