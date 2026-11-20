# 2352. Equal Row and Column Pairs

Given a **0-indexed** `n x n` integer matrix `grid`, *return the number
of pairs* `(ri, cj)` *such that row* `ri` *and column* `cj` *are equal*.

A row and column pair is considered equal if they contain the same
elements in the same order (i.e., an equal array).

```
grid = [[3,2,1],[1,7,6],[2,7,7]]                    ->  1
grid = [[3,1,2,2],[1,4,4,5],[2,4,2,2],[2,4,2,2]]    ->  3
```

**Constraints:** `n == grid.length == grid[i].length`;
`1 <= n <= 200`; `1 <= grid[i][j] <= 10^5`.

A row that appears `a` times and a column equal to it that appears `b`
times make `a b` pairs, so counting the rows by value and looking each
column up is enough. A grid of one value has `n^2` pairs, 40000 at the
largest.

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | the rows counted in a `Map` keyed by the row itself, then each column built and looked up there. O(n^2) beyond hashing n-long keys |
| `pairs_naive.kara` | no table: every row against every column, cell by cell, stopping at the first that differs. O(n^3) |
| `pairs_transpose.kara` | the grid flipped so its columns are rows, then every row of one compared with every row of the other by `==` on whole vectors. O(n^3) |
| `pairs_sorted.kara` | the rows sorted and the columns sorted, then the two lists walked together, each run of equal rows meeting its run of equal columns counted as their product. O(n^2 log n) |
| `pairs_iter.kara` | iterators: each column gathered by `map` and `collect`, the rows equal to it counted by `filter` and `count`, all summed |
| `pairs_solution.kara` | LeetCode's Rust template: a `HashMap<Vec<i32>, i32>` filled through `entry(...).or_insert(0)`, each column looked up with `if let Some(&count)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one cell;
200 x 200 ones; the 200 x 200 identity; the 200 x 200 grid of
`i j mod 7`, whose row `i` equals its column `i` and the row of every
`i'` with `i' = i mod 7`, 5716 pairs; then 1000 random grids of 1 to 6
rows of values from 1 to 1 up to 1 to 3, and 1 to `10^5` in every
tenth, with a checksum, the pairs summed and how many grids have none.
`pairs.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked against every row and column compared directly on
3000 random grids.

A `Vec[i64]` keys the `Map` as it is, compared and hashed by value, and
the sorted arm orders whole vectors with `sort` and `<`, both
lexicographic, as in Rust.

`karac fix` carries the template in one call, reporting 20 edits.
`check` first reports 10 errors, each with its edit: the `HashMap`
import deleted, `struct Solution;` given braces, the angle brackets of
`Vec<..>` and `HashMap<..>` made square, the `::` paths written with
`.`, `&grid` in the `for` made `ref grid`, `&column` as an argument
dropped, and `Some(&count)` made `Some(count)` over `.cloned()`. The
rest follow: `HashMap` made the prelude's `Map` once the import is
gone, and `let mut total = 0` annotated `: i32`, since an unsuffixed
literal is an `i64` in Kāra and the template returns `total` as an
`i32` after adding `i32` counts to it. `entry(...).or_insert(0)` with
`+= 1` through `*` stands as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every row and every column, the row written out and the
column written out as lists, and the pair counted when the lists have
the same length and the same value at every place. It checks 300 random
grids of 1 to 6 rows of values from 1 to 1 up to 1 to 3; then 40
symmetric grids of up to 40 rows of 1 and 2; then 20 grids of 50 to
120 rows whose cell `(i, j)` is `(a i j + b) mod m`. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | up to 40 rows, the answer is the literal reading's |
| P2 | from 0 to `n^2`, and at least `n` when the grid is symmetric |
| P3 | the grid transposed: the same answer |
| P4 | every value `x` made `3 x + 1`: the same answer |
| P5 | the grid turned half a circle, cell `(i, j)` taken from `(n - 1 - i, n - 1 - j)`: the same answer |
| P6 | each arm agrees with at least three of the other five |

P3 holds because row `r` equals column `c` exactly when, transposed,
column `r` equals row `c`; P5 because the half turn reverses every row
and every column alike, and maps row `r` and column `c` to row
`n - 1 - r` and column `n - 1 - c`.

The differential prints `360 cases: checksum 75682038, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and compares rows and columns as tuples. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: row j looked up for column j | P1 145, P3 29, P6 145 |
| M3 | ★: each column's last cell left out | P1 263, P2 215, P6 283 |
| M6 | ★: each row counted from 1 | P1 263, P2 152, P3 10, P6 283 |
| M7 | naive: the last cell ignored | P1 89, P5 71, P6 89 |
| M9 | naive: only columns from the row on | P1 146, P3 49, P5 49, P6 166 |
| M10 | naive: each pair counted n times | P1 223, P2 132, P6 243 |
| M13 | transpose: the first column skipped | P1 222, P2 84, P3 24, P5 41, P6 242 |
| M14 | transpose: only the first cells compared | P1 182, P5 145, P6 200 |
| M15 | transpose: only the upper triangle flipped | P1 212, P2 59, P3 32, P4 7, P5 43, P6 231 |
| M17 | sorted: two runs added, less one, not multiplied | P1 113, P6 133 |
| M18 | sorted: the columns left unsorted | P1 84, P2 56, P3 21, P5 78, P6 102 |
| M19 | sorted: a column passed over for a smaller row | P1 48, P3 14, P5 25, P6 48 |
| M22 | iter: column 0 for every column | P1 69, P3 24, P5 41, P6 80 |
| M25 | iter: each column counted once | P1 117, P3 10, P6 137 |
| M26 | iter: the largest count, not the sum | P1 183, P2 63, P3 10, P6 203 |
| M29 | solution: each column read bottom up | P1 91, P2 40, P6 107 |
| M30 | solution: the last column skipped | P1 222, P2 84, P3 32, P5 41, P6 242 |

P1 and P6 kill all seventeen, P3 eleven, P2 and P5 nine each, and P4
one. P4, every value made `3 x + 1`, is a one-to-one relabelling that
no arm's logic should notice, and it fails only the upper triangle
flipped, whose unwritten cells keep the 0 the flipped grid was filled
with: a grid of the differential can hold a 0, but not once relabelled,
so the stray zeros match rows before and not after. P2 fails the edits
that count too many or too few outright: a last cell left out, which
never matches; rows counted from 1; each pair counted `n` times; a
column skipped, so a symmetric grid falls under `n`. P5, the half turn,
fails the edits that treat one end of a row or a column unlike the
other, and P3, the transpose, those that treat rows unlike columns.

Of the thirty-one, fourteen were not kept. A repeated row counted once
and a found column counted once, in the ★ arm (M1, M5) and in the
template (M27, M28), fail as the iter arm's each column counted once
(M25): the grids where a row repeats and matches a column are the only
ones they get wrong. Row against row in the naive arm (M8) and the grid
never flipped in the transpose arm (M12) fail as the ★ arm's row `j`
looked up for column `j` (M2); the first column skipped in the ★ and
iter arms (M4, M24) as in the transpose arm (M13); and only the first
cells compared in the iter arm (M23) as in the transpose arm (M14). The
naive arm's first cell skipped (M11), the transpose arm's row counted
for every column after it (M16), the sorted arm's one column to a run
(M20) and rows sorted backwards (M21), and the template's first row
never counted (M31) fail apart from every kept one; they were left out
to keep three to an arm and two to the template.

## Verification

Every arm prints the same output as `pairs.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, sorted and template arms take 0.4 to
0.5 s, the transpose and iter arms 1.2 and 1.5 s, and the naive arm
4.3 s, its `n^3` cell reads on the three 200-row grids. The
differential takes 15.6 s there, nearly all of it the two cubic arms on
the grids of 50 to 120 rows, and 0.73 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 grids of 200 x 200 once, cell `(i, j)` of each
being `(a i j + b) mod m` with `a` from 1 to 5 and `m` from 2 to 10 so
that rows repeat and match columns, then makes 40 passes, pass `p`
folding each answer plus `p` into the checksum, with the ★ arm in all
five languages. Every implementation prints `40 passes over 10 grids of
200 x 200: checksum 116681223`. Each call builds its own table and
columns. Go cannot key a map by a slice, so its key is the row's values
written into a string, 8 bytes each; C has no map, so it counts in a
table of 512 slots by open addressing, hashing a row by FNV-1a and
comparing it in full.

BENCHTAB
