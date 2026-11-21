# 2435. Paths in Matrix Whose Sum Is Divisible by K

You are given a **0-indexed** `m x n` integer matrix `grid` and an
integer `k`. You are currently at position `(0, 0)` and you want to
reach position `(m - 1, n - 1)` moving only **down** or **right**.

Return *the number of paths where the sum of the elements on the path
is divisible by* `k`. Since the answer may be very large, return it
**modulo** `10^9 + 7`.

```
grid = [[5,2,4],[3,0,5],[0,7,2]], k = 3         ->  2
grid = [[0,0]], k = 5                           ->  1
grid = [[7,3,4,9],[2,3,6,2],[2,3,7,0]], k = 1   ->  10
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`1 <= m, n <= 5 * 10^4`; `1 <= m * n <= 5 * 10^4`;
`0 <= grid[i][j] <= 100`; `1 <= k <= 50`.

A path reaches a cell from above or from the left, and only its sum
modulo `k` matters to what follows, so each cell keeps a count of the
paths into it for each remainder: those from above and from the left
at the remainder the cell's value leaves behind. That is `m n k` steps,
at most 2.5 million; the arms differ in which way the counts flow and
how much of the table is kept.

## Approaches

| file | mechanism |
|---|---|
| `paths.kara` ★ | one row of counts by remainder kept: a cell's counts are those above it, still in place, plus those to its left, shifted by the cell's value. O(m n k) time, O(n k) space |
| `paths_naive.kara` | the table read directly: `ways[i][j][r]` the paths into each cell at each remainder, each pulled from the cell above and the cell to the left at the remainder before the cell's value. O(m n k) time and space |
| `paths_memo.kara` | top-down: the paths from a cell to the end that finish at remainder 0, by recursion right and down, each answer kept in a flat memo of `m n k` entries, -1 until known. O(m n k) |
| `paths_flat.kara` | pushed forward over one flat `Vec[i64]` of `m n k` counts, each count, once its cell is done, added to the cell below and the cell to the right. O(m n k) |
| `paths_iter.kara` | iterators: the rows folded by `fold`, each row's counts built from the row above by `scan` along the row, each cell's by `map` over the remainders. O(m n k) |
| `paths_solution.kara` | LeetCode's Rust template: a `const MOD` written `1_000_000_007` inside the function, `let (m, n, k) = (..)` with `k as usize`, the whole `vec![vec![vec![0i64; k]; n]; m]`, and counts pushed forward with `usize` remainders; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples; one cell
divisible, and not; a 2 by 2 of zeros, both paths counting; the
constraints' largest, a 200 by 250 grid with `k` = 50, whose count
passes `10^9 + 7` many times over; 2 by 25000 with `k` = 17; 250 by 200
of all 100 with `k` = 1, every one of the `C(448, 199)` paths counting;
and 3000 random grids of 1 to 4 by 1 to 4, values up to 9, `k` from 1 to
6, as a checksum and the total. `paths.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked on 20000 random
grids of up to 5 by 5 against every path walked, and the all-100 count
against `C(448, 199)` taken by Python's `math.comb`.

`check` first reports 2 errors on the template, and `karac fix` carries
it in one call, reporting 15 edits: the brackets of `Vec<Vec<i32>>` and
`struct Solution;` given its braces; then, once the template parses,
the three `vec!` written `Vec.filled`, the `i64` suffix of `0i64`
dropped as the default, `k as usize` written `k as i64`, and the `as
usize` on each grid value dropped, Kāra indexing by `i64`. The `const`
inside the function, the literal `1_000_000_007`, the tuple `let (m, n,
k) = (..)`, `continue` and the final `as i32` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every path walked by recursion, right or down from the
top-left, its sum added as it goes, and counted when the bottom-right is
reached with a sum divisible by `k`. No remainder is tracked. It checks
300 random grids of 1 to 5 by 1 to 5, values up to 9, `k` from 1 to 8;
then 30 of up to 7 by 7, values up to 100, `k` from 1 to 50; then 30 of
one or two rows or columns up to 30 long, values up to 100, `k` from 1
to 50. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the grid transposed: the same answer |
| P3 | the grid turned half round: the same answer |
| P4 | no more than every path, `C(m + n - 2, m - 1)` |
| P5 | `k` = 1: every path, the binomial `C(m + n - 2, m - 1)` |
| P6 | each arm agrees with at least three of the other five |

P2 holds because transposing swaps right and down, and P3 because
turning the grid half round walks every path backwards, each over the
same cells. P4 and P5 hold because a path is a choice of which of its
`m + n - 2` steps go down, and every sum is divisible by 1; the cases
have at most 924 paths, so no count is reduced.

The differential prints `360 cases: checksum 944396558, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and walks every path. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: a path started at every row | P1 181, P2 216, P3 153, P4 41, P5 276, P6 181 |
| M5 | ★: the start at remainder 1 | P1 203, P6 203 |
| M6 | ★: the remainder 1 answered | P1 207, P6 207 |
| M7 | naive: the up and left from the same column | P1 191, P2 47, P5 285, P6 191 |
| M8 | naive: the current remainder pulled | P1 188, P3 94, P6 188 |
| M11 | naive: the first row never pulled from the left | P1 159, P2 177, P3 98, P5 285, P6 159 |
| M12 | memo: the end counted for any remainder | P1 288, P6 288 |
| M14 | memo: the memo keyed without the remainder | P1 127, P2 72, P3 79, P6 127 |
| M15 | memo: the move down never tried | P1 184, P2 47, P5 276, P6 184 |
| M18 | flat: the down move by the cell's own value | P1 160, P2 173, P3 140, P6 160 |
| M19 | flat: the start at zero | P1 153, P3 140, P6 153 |
| M21 | flat: the counts added twice down | P1 184, P2 181, P4 142, P5 276, P6 184 |
| M22 | iter: the cell above read one to the left | P1 154, P2 134, P3 112, P5 158, P6 154 |
| M25 | iter: the first cell of the last row read | P1 185, P2 104, P3 76, P5 216, P6 185 |
| M26 | iter: the left pulled at the current remainder | P1 163, P2 163, P3 127, P6 163 |
| M29 | solution: the right move by the cell's own value | P1 152, P2 173, P3 138, P6 152 |
| M31 | solution: the count added to itself | P1 102, P2 108, P3 109, P4 15, P6 102 |


P1 and P6 kill all seventeen, P2 twelve, P3 eleven, P5 seven and P4
three.

Fourteen are not kept. Ten fail exactly as a kept one. The ★ arm's
left never added and the iter arm's left never carried (M1, M23) fail
as the naive arm's up and left from the same column (M7), each losing
the paths from the left; the ★ arm's above never added and the
template's down move never made (M2, M30) as the memo arm's move down
never tried (M15), each losing the paths from above; the ★ arm's value
never added, the naive arm's start counted for every remainder and the
iter arm's remainder itself pulled (M4, M9, M24) as the memo arm's end
counted for any remainder (M12), each counting every path; the naive
arm's up doubled (M10) as the flat arm's counts added twice down (M21);
and the memo arm's and the template's start without its value (M16,
M28) as the flat arm's start at zero (M19).

Four are equivalent and three of them were replaced. The ★ arm's value
shifted the wrong way tracks the remainder of the sum's negative, which
is 0 exactly when the sum's is; the iter arm's above kept in the first
row reads a row that is all zeros there but at the first cell; the
memo arm's memo never read only recomputes; and the template's zero
counts pushed too adds zeros. The ★ arm's and the iter arm's became a
path started at every row (M3) and the cell above read one to the left
(M22); a first replacement for the ★ arm, the second column never fed
from the left, failed as M7 does. The flat arm's right move into the
next row and last column's right move kept (M17, M20) end in an index
out of bounds under both backends, crashes; the flat arm keeps its
other three.

P4 was at first every value raised by `k`, the same answer. No
mutation failed it: each one that slipped on a remainder slipped before
the raise as well, and P1 caught it. It became no more than every path,
which three kept mutations fail.

## Verification

Every arm prints the same output as `paths.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 3.8 to 7.2 s, the memo arm 14.1 s,
its recursion paying for every call; under `karac run` every arm takes
0.4 to 0.6 s. The differential takes 1.2 s under `karac __mir-run`,
0.8 s under `karac __mir-llvm-asan` and 0.8 s under `karac run`.

## Benchmarks

The bench builds 5 grids of 200 by 250, the constraints' largest, once
from its own generator, values up to 100. It then makes 10 passes; each
sets one cell of every grid, so no answer can be carried from one pass
to the next, then answers every grid with `k` = 50, folding the answer
plus the pass into the checksum. The bench uses the ★ arm, one row of
counts by remainder, in all five languages. Every implementation prints
`10 passes over 5 grids of 200 by 250: checksum 755320922`. Each grid is
a list of rows in every language, and in C an array of row pointers;
each answer allocates its row of counts afresh.

BENCHTAB
