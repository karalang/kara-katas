# 1536. Minimum Swaps to Arrange a Binary Grid

Given an `n x n` binary `grid`, in one step you can choose two adjacent
rows of the grid and swap them. A grid is valid if all the cells above
the main diagonal are zeros. Return the minimum number of steps needed to
make the grid valid, or `-1` if it cannot be made valid. The main diagonal
runs from cell `(1, 1)` to cell `(n, n)`.

```
grid = [[0,0,1],[1,1,0],[1,0,0]]                    ->  3
grid = [[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0]]    ->  -1
grid = [[1,0,0],[1,1,0],[1,1,1]]                    ->  0
```

**Constraints:** `n == grid.length == grid[i].length`; `1 <= n <= 200`;
`grid[i][j]` is `0` or `1`.

## Approaches

| file | mechanism |
|---|---|
| `swaps.kara` ★ | greedy over each row's run of trailing zeros. Row `i` must end in at least `n - 1 - i` zeros; top down, the nearest row at or below `i` with enough is bubbled up to `i` by adjacent swaps. A nearer choice cannot exist, and each row it passes needs fewer zeros than row `i`, so moving it down one does no harm. O(n²) |
| `swaps_last_one.kara` | the same greedy over each row's last 1 (`-1` for a row of zeros), which row `i` needs at column `i` or before; the chosen row is taken out and put back at `i`, `j - i` swaps |
| `swaps_iter.kara` | the ★ arm with iterators: trailing zeros by `rev().take_while(..).count()`, the row for place `i` by `position` over `zeros[i..]`, moved with `remove` and `insert` |
| `swaps_solution.kara` | LeetCode's Rust template (`grid: Vec<Vec<i32>>`, `usize` counts, `(i..n).find(..)`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples, `[[1]]`,
`[[1, 1], [1, 0]]` and `[[1, 1], [0, 1]]`, 200 rows in reverse order
(19900 swaps), then the count of solvable grids and a checksum of the
answers for 3000 random grids of 1 to 8 rows and 300 of 1 to 200. Half of
the grids take each row's trailing zeros from a shuffle of 0 to n - 1
(each maybe one more), the other half draw each row's count from 0 to n.
`swaps.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a breadth-first search over the orders of the rows, one
adjacent swap a step, to the first order whose cells above the main
diagonal are all zero. It checks 3000 grids of 1 to 6 rows, every random
choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is `-1` exactly when the rows' trailing zeros, sorted from most, fall short somewhere: the k-th needs at least `n - 1 - k` |
| P3 | the rows sorted by trailing zeros, most first, need no swap |
| P4 | bits changed before each row's last 1 leave the answer |
| P5 | the answer is at most n(n - 1)/2 |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 368266489, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: row `i` asked for `n - i` zeros | P1 1845, P2 1487, P3 1487, P6 1845 |
| M2 | ★: trailing zeros counted two at a time | P1 778, P2 218, P4 315, P6 778 |
| M3 | ★: the bubbling swaps nothing | P1 951, P2 342, P6 951 |
| M4 | last one: a row's last 1 at column `i` refused | P1 1845, P2 1487, P3 1487, P6 1845 |
| M5 | last one: the chosen row put back where it was | P1 951, P2 342, P6 951 |
| M6 | last one: the last column never read | P1 866, P2 360, P4 462, P6 866 |
| M7 | iter: a row with exactly enough zeros refused | P1 1845, P2 1487, P3 1487, P6 1845 |
| M8 | iter: one swap counted per move | P1 2169, P3 2275, P5 942, P6 2169 |
| M9 | template: the chosen row moved to the bottom | P1 1276, P2 422, P3 737, P6 1276 |
| M10 | template: trailing ones counted | P1 1884, P2 1662, P3 1770, P4 45, P6 1884 |

A first M2, an all-zero row counted as `n - 1` zeros rather than `n`,
survived every property: no row ever needs more than `n - 1`, so it is
the same program.

## Benchmarks

The bench builds 50 random 200 x 200 grids once, from the same generator
as the harness, and answers each 50 times by the ★ arm, in all five
languages. Every implementation prints `50 passes over 50 grids of 200
rows: checksum 14772469`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `3d1fc8e26` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.068 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.085 s |
| Go | 0.119 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.153 s |
| Kāra (`karac build`) | 0.159 s |
| Rust (`rustc -O`) | 0.167 s |
| Python | 4.3 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.19 s and 0.19 s on one run).

Kāra is 1.80x Rust under overflow checks by median. Not traced, and the
rows do not order the way the work suggests: unchecked Rust ran slower
than checked Rust in every run. The runs are short (the grids' building
is part of each), so the spread is wide; read this row as unsettled.

## Verification

All four arms print the same output as `swaps.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `3d1fc8e26`.

## Writing it

The ★ and last-one arms were written in Kāra and checked as written. The
differential's search took one edit from `karac fix`: `while
!frontier.is_empty()` to `while not frontier.is_empty()`.

The iterator arm was refused as written, and is the reason for a compiler
fix. `match zeros[i..].iter().position(..) { .. Some(ahead) => {
zeros.remove(i + ahead); .. } }` was refused with "`zeros` cannot be
borrowed as `mut ref T` because it is also borrowed as `Slice[T]`": the
range view made in the scrutinee stayed borrowed through the arms,
although the scrutinee's value is an `Option[i64]` that holds nothing of
`zeros`. The same position bound by `let` first checked, and so did a
scrutinee with no range view. Fixed in kara `3d1fc8e26` (B-2026-11-14-5): a view
made in a `match` or `if let` scrutinee whose value holds no borrow ends
there, as it does at a `let`.

The Rust template took 7, 1 and 3 changed lines over three rounds:
`Vec<Vec<i32>>` to `Vec[Vec[i32]]` (and the same in the wrapper),
`Vec<usize>` to `Vec[usize]`, the closures' `|&&c|`, `|&j|` and `|&c|` to
`|c|`, `|j|` and `|c|`, and `Solution::` to `Solution.`; then the
`struct Solution {}` the template leaves out added; then `Vec[usize]` to
`Vec[i64]`, `let mut ans = 0` to `let mut ans: i32 = 0` (an `ans += x as
i32` leaves a literal at `i64`) and the closing `as i64` dropped. It
checks and agrees with no hand edit.
