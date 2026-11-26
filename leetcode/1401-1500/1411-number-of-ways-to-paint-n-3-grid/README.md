# 1411. Number of Ways to Paint N × 3 Grid

You have a `grid` of size `n x 3` and you want to paint each cell of the
grid with exactly one of the three colors: Red, Yellow, or Green while
making sure that no two adjacent cells have the same color (i.e., no two
cells that share vertical or horizontal sides have the same color).
Given `n` the number of rows of the grid, return the number of ways you
can paint this `grid`. As the answer may grow large, the answer must be
computed modulo `10^9 + 7`.

```
n = 1     ->  12
n = 5000  ->  30228214
```

**Constraints:** `n == grid.length`, `1 <= n <= 5000`.

Each arm is `fn num_of_ways(n: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `num_of_ways.kara` ★ | every row is one of 6 with two colours, `aba`, or one of 6 with three, `abc`; below an `aba` row go 3 `aba` and 2 `abc` rows, below an `abc` row 2 of each, so two counts carried down the rows. O(n) |
| `num_of_ways_states.kara` | the 12 rows with no two neighbours alike as `(a, b, c)` tuples, a table of which rows may sit on which, and a count of the ways to end in each row. O(144 n) |
| `num_of_ways_matrix.kara` | the two-kind step as a `struct` of a 2 x 2 matrix, raised to the n - 1-th power by squaring, and the first row's 6 of each kind put through it. O(log n) |
| `num_of_ways_cells.kara` | the grid painted a cell at a time: the state is the last three cells painted, the one above the next and the one to its left among them, as a number of three base-3 digits, 27 states. O(243 n) |
| `num_of_ways_solution.kara` | a Rust solution as LeetCode's Rust users write it (`const MOD` in the body, `let (mut a, mut b) = (6i64, 6i64)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples, then n from
1 to 10 (`12 30228214 | 12 54 246 1122 5118 23346 106494 485778 2215902
10107954`); the constraints' most and below it (`n = 4998..5000:
821437694 134620719 30228214`); and every n from 1 to 600 folded (`n =
1..600: checksum 663348667`). `num_of_ways.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, states, matrix and cells arms check clean as first
written. The Rust solution takes one round of 13 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `let (mut a, mut b) =
(6i64, 6i64)` to `let mut (a, b) = (6, 6)`, since `mut` goes before the
whole pattern and the suffixes repeat the default, and `Solution::` to
`Solution.`. Its `const MOD: i64 = 1_000_000_007;` inside the function
is taken as written. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every cell painted in turn, row by row, with each colour its
painted neighbours above and to the left allow, and every whole grid
counted, while the grids are few, n up to 6. Every n from 1 to 60, the
constraints' most and the two below it, and 1940 random n up to 300.

The differential's `arm` first widened each answer with `ways as i64`;
an `i32` widens to `i64` implicitly, and `karac fix` drops the cast, 1
fix.

| | property |
|---|---|
| P1 | the statement read literally, n up to 6 |
| P2 | a count taken modulo 10^9 + 7, from 0 to 10^9 + 6 |
| P3 | the step from a row to the next is a 2 x 2 matrix of trace 5 and determinant 2, so f(n + 2) = 5 f(n + 1) - 2 f(n), modulo 10^9 + 7 |
| P4 | while no count wraps, n up to 11: a multiple of 6, since a grid with its colours swapped round is another, and each row more multiplies the count by more than 4 and less than 5 |
| P5 | LeetCode's answer for 5000, and the first seven counts |
| P6 | the ★ arm's answer |

All 30,895 checks pass on every arm: `2003 cases: checksum 810022959,
30895 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by the 12-row
table, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: two `aba` rows below an `aba` row, where there are three | P1 32, P3 2003, P4 78, P5 40, P6 7972 |
| M2 | ★: one step from a row to the next too many, so the count is for n + 1 rows | P1 42, P5 50, P6 8012 |
| M3 | states: rows that repeat a colour in their last two cells allowed | P1 42, P3 2003, P4 78, P5 50, P6 2003 |
| M4 | states: a row allowed on one with the same middle colour | P1 32, P3 2003, P4 78, P5 40, P6 1993 |
| M5 | matrix: three `abc` rows below an `abc` row, where there are two | P1 32, P3 2003, P4 78, P5 40, P6 1993 |
| M6 | matrix: the base squared where the power takes it once | P1 32, P3 2003, P4 78, P5 40, P6 1993 |
| M7 | cells: a row's first cell checked against the cell to its left, and its second not | P1 26, P3 10, P5 34, P6 1987 |
| M8 | cells: the state's window kept on the two older cells, losing the one just painted | P1 32, P3 2003, P4 78, P5 40, P6 1993 |
| M9 | solution: three `abc` rows below an `abc` row | P1 32, P3 2003, P4 78, P5 40, P6 1993 |
| M10 | solution: the `abc` count never carried to the next row | P1 32, P3 2003, P4 78, P5 40, P6 1993 |

## Benchmarks

The bench runs the ★ arm on 40000 grids, each n up to 5000 drawn from
the checksum so far. Every implementation prints `40000 grids of up to
5000 rows: checksum 122789323`.

BENCHTAB

Kāra is level with Rust, C and Go here, measured by hand at 0.59 s
against Rust's 0.57 s, with overflow checks on or off, C's 0.58 s and
Go's 0.54 s: the loop is two multiplications and a division by the
modulus a row, carried from one row to the next.
