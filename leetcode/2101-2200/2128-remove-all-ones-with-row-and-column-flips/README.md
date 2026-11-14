# 2128. Remove All Ones With Row and Column Flips

You are given an `m x n` binary matrix `grid`.

In one operation, you can choose any row or column and flip each value
in that row or column (i.e., change all `0`'s to `1`'s, and all `1`'s
to `0`'s).

Return `true` if it is possible to remove all `1`'s from `grid` using
any number of operations or `false` otherwise.

```
grid = [[0,1,0],[1,0,1],[0,1,0]]  ->  true
grid = [[1,1,0],[0,0,0],[0,0,0]]  ->  false
grid = [[0]]                      ->  true
```

**Constraints:** `m == grid.length`; `n == grid[i].length`; `1 <= m, n
<= 300`; `grid[i][j]` is either `0` or `1`.

Flips commute, and two flips of one line undo each other, so a grid
clears exactly when some set of rows and some set of columns, each
flipped once, clears it: when each cell is its row's flip xor its
column's. That holds exactly when every row is the first row or its
complement, which each cell shows against its row's first cell and the
first row's. One pass, O(m * n).

## Approaches

| file | mechanism |
|---|---|
| `flips.kara` ★ | every cell checked against the first row by xor with its row's first cell, `let first = ref grid[0];` and a `for` loop that stops at the first cell out of line |
| `flips_simulate.kara` | the flips made on a `clone`: every row starting with a 1 flipped through `iter_mut`, then each column compared with its top cell |
| `flips_pattern.kara` | each row written as a `String`, turned over to start with a 0, and gathered into a `Set[String]`; one pattern left means it clears |
| `flips_struct.kara` | a `struct Pattern { first }` whose `fits` (`ref self`) matches on whether a row's first cell agrees with the first row's, then compares the row through `zip` and `all`; driven by `all` |
| `flips_iter.kara` | one condition over every cell, `(1..m).all(\|i\| (1..n).all(\|j\| ..))`: a cell, its row's first cell, its column's top cell and the corner xor to zero |
| `flips_solution.kara` | LeetCode's Rust template: `row == first` or every pair of a `zip` unequal, carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (one row, one column, all ones, one 1 in a corner), each with its
answer; then the grids cleared and a checksum over 3000 random grids of
1 to 6 by 1 to 6, every other one cell by cell and the rest a zero
grid's rows and columns flipped, one in three of those with one cell
then flipped; then the constraints' largest, 300 by 300 of rows and
columns flipped, the same with its last cell changed, and with its
first. `flips.py` mirrors the ★ arm and its output is byte-identical.

No compiler gap was met in the arms. The ★ arm was first written `let
first = grid[0];`, a move out of an index, which `karac check` refused
and `karac fix` turned into `ref grid[0]`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every grid reachable from this one by flipping one row or one
column at a time is found, breadth first over the grids as bit masks,
and the answer is whether the grid of zeros is among them; nothing is
assumed about the order of the flips or how often one is made. It
checks 300 random grids of 1 to 4 by 1 to 4, a cell a 1 with chance a
quarter, a half or three quarters in turn; then 30 of 2 to 4 by 2 to 4
made of a zero grid's rows and columns flipped, every other one with
one cell flipped as well; then 30 of one row or one column. All 360 are
drawn before any arm answers; 209 of them clear.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the grid transposed: the same answer |
| P3 | the rows in reverse order: the same answer |
| P4 | one column flipped: the same answer |
| P5 | the first row turned over added at the bottom: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 grids: checksum 779210279, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
grids by the same search. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-one edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: only the first two cells of each row checked | P1 32, P2 55, P6 32 |
| M3 | ★: the last row never checked | P1 52, P2 57, P3 33, P5 52, P6 52 |
| M5 | ★: the first row not turned by its first cell | P1 108, P3 43, P4 136, P6 108 |
| M7 | simulate: only a row's first cell flipped | P1 37, P2 46, P5 126, P6 37 |
| M9 | simulate: every cell compared with the corner | P1 37, P2 46, P3 41, P4 76, P5 77, P6 37 |
| M10 | simulate: the second row never checked | P1 53, P2 60, P3 9, P6 53 |
| M11 | pattern: the rows never turned over | P1 55, P2 115, P5 154, P6 55 |
| M12 | pattern: two patterns allowed | P1 102, P6 102 |
| M13 | pattern: a row's last cell left out | P1 65, P2 57, P6 65 |
| M15 | struct: a row as it is refused | P1 209, P6 209 |
| M18 | struct: a row as it is compared one cell along | P1 74, P2 115, P4 91, P6 74 |
| M19 | struct: only the first row tried | P1 151, P6 151 |
| M20 | iter: the corner's own cell left out | P1 38, P3 39, P4 28, P5 49, P6 38 |
| M23 | iter: an or for the first xor | P1 38, P3 7, P4 12, P5 52, P6 38 |
| M30 | iter: any column enough in each row | P1 138, P2 222, P3 26, P5 24, P6 138 |
| M25 | solution: a row turned over compared one cell along | P1 32, P2 26, P3 35, P4 64, P5 81, P6 32 |
| M26 | solution: a row the same when its first cell is | P1 56, P2 81, P3 21, P6 56 |

P1 and P6 kill all seventeen, P2 eleven, P3 nine, P5 eight and P4 six.
P2 transposes, so it sees the edits that treat rows unlike columns: a
row or a column left out (M2, M3, M10, M13), a row turned over or not
by the wrong cell (M7, M11, M26), a comparison shifted along the row
(M18, M25), `any` for `all` (M30). P3 moves the last row to the top and
P4 flips a column, which see the edits that lean on the first row or
the first column being as given: the first row not turned (M5), the
corner read in place of the top cell (M9), the corner left out (M20).
P5 adds the first row turned over at the bottom, which every correct
arm accepts and which sees the edits that refuse a row that is the
first one's complement (M7, M11), or never read the last row (M3). M12
and M19 accept too much and M15 too little, and only P1 sees that.

Of the thirty-one, fourteen were not kept. Five are equivalent: the ★
arm taking the last row as the one to compare with, the simulate arm
flipping the rows that start with a 0 rather than a 1, the struct arm
matching on the last cells rather than the first, and the adapter
handing each row reversed or each cell doubled, since columns can be
put in any order and a doubled cell is still unequal to a 0. None
survives, and none fails by a crash. Eight fail as a kept one does: the
★ arm comparing rows as they are and the pattern arm turning each row
by the grid's first cell as M11; the struct arm taking the first row's
first cell as a 0 as M5; the simulate and iter arms leaving the last
column out as M13; the iter arm starting at the third row as M10; the
Rust arm needing both tests as M15; and its adapter keeping two columns
as M2. One is killed with checks of its own but was left out because
its arm keeps its share: the iter arm reading the first row's cell from
the second (P1 38, P2 64, P3 26, P5 104, P6 38).

## Verification

Every arm prints the same output as `flips.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 s to 0.9 s and the
differential 0.58 s.

`karac fix` carries the template in two rounds of 15 and 1 edits:
Rust's spellings (`Vec<Vec<i32>>` to `Vec[Vec[i32]]`, `&grid[0]` to
`ref grid[0]`, `for row in &grid` to `for row in ref grid`, `!` to
`not`, `&&` to `and`, `struct Solution;` to `struct Solution {}`, the
adapter's `&Vec` to `ref Vec`, `Solution::` to `Solution.`, `|&x|` to
`|x|`); then the `ref` dropped from the adapter's parameter, which
borrows already. The adapter's `x as i32` stays: an `i64` narrows only
by a cast.

## Benchmarks

The bench builds 20 grids of 300 by 300 once, each a zero grid's rows
and columns flipped, then solves every grid 100 times, one random row
flipped before each solve so that no solve repeats one before, and
every other time one random cell flipped for that solve and back after
it, with the ★ arm in all five languages. Every implementation prints
`2000 solves: 987 cleared, checksum 119132364`.

BENCHTAB
