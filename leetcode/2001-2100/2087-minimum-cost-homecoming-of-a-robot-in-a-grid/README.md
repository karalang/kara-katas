# 2087. Minimum Cost Homecoming of a Robot in a Grid

There is an `m x n` grid, where `(0, 0)` is the top-left cell and
`(m - 1, n - 1)` is the bottom-right cell. You are given an integer array
`startPos` where `startPos = [startrow, startcol]` indicates that
initially, a robot is at the cell `(startrow, startcol)`. You are also
given an integer array `homePos` where `homePos = [homerow, homecol]`
indicates that its home is at the cell `(homerow, homecol)`.

The robot needs to go to its home. It can move one cell in four
directions: left, right, up, or down, and it can not move outside the
boundary. Every move incurs some cost. You are further given two
0-indexed integer arrays: `rowCosts` of length `m` and `colCosts` of
length `n`.

- If the robot moves up or down into a cell whose row is `r`, then this
  move costs `rowCosts[r]`.
- If the robot moves left or right into a cell whose column is `c`, then
  this move costs `colCosts[c]`.

Return the minimum total cost for this robot to return home.

```
startPos = [1,0], homePos = [2,3], rowCosts = [5,4,3], colCosts = [8,2,6,7]  ->  18
startPos = [0,0], homePos = [0,0], rowCosts = [5], colCosts = [26]           ->  0
```

**Constraints:** `m == rowCosts.length`; `n == colCosts.length`; `1 <= m,
n <= 10^5`; `0 <= rowCosts[r], colCosts[c] <= 10^4`; `startPos.length ==
2`; `homePos.length == 2`; `0 <= startrow, homerow < m`; `0 <= startcol,
homecol < n`.

Every path home enters each row between the start's and home's, home's
included, at least once, and each such column likewise, and the straight
path enters each exactly once; the costs are never negative. So the
answer is two ranges of costs summed, O(m + n), and no search is needed.
The approaches differ in how they find and sum the ranges.

## Approaches

| file | mechanism |
|---|---|
| `homecoming.kara` ★ | each axis's range sliced and summed, `costs[from + 1..=to].iter().sum()` forward and `costs[to..from]` back. O(m + n) |
| `homecoming_walk.kara` | the walk itself: the robot moved a row at a time with `signum()` of the distance as its step, paying for each row it enters, then a column at a time |
| `homecoming_prefix.kara` | prefix sums of each axis, `before[i]` the costs before place `i`, the way home a difference of two |
| `homecoming_filter.kara` | every place of an axis from `iter().enumerate()`, kept by `filter` when it lies between start and home and is not the start's, and summed |
| `homecoming_struct.kara` | a `struct Axis` of one direction's costs with `toll(from, to)`, the places entered walked by a range, `rev()`ed on the way back |
| `homecoming_solution.kara` | LeetCode's Rust template (`Vec<i32>` throughout, `let (mut r, mut c)`, `r += if hr > r { 1 } else { -1 }`, `row_costs[r as usize]`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and five
more, each grid and its cost; then the sum and a checksum of the costs
for 2000 random grids of 1 to 50 rows and columns, costs up to `10^4`;
then the costs for the constraints' largest, `10^5` rows and columns,
corner to corner and back. `homecoming.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the cheapest path over the grid's cells, each move up, down,
left or right paying for the row or column it enters, found by relaxing
every cell's best cost until none falls. It checks 300 random grids of
1 to 6 rows and columns, costs up to 20; then 20 whose robot starts at
home, and 20 of one row. All 340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the cost is the statement read literally |
| P2 | the way back costs the way home less home's row and column, and more the start's |
| P3 | the grid transposed, rows for columns, costs the same |
| P4 | every row's cost raised by 7 costs 7 more for each row between |
| P5 | the rows mirrored, the last first, cost the same |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 grids: checksum 363463282, 12240 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal costs was checked against a Dijkstra search of the same
grids in Python. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-two edits to the differential, four to seven to each of its arms,
each run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen
are kept, three to each Kāra arm and two to the Rust-template arm. Each
kept one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the start paid for on the way forward | P1 129, P2 247, P4 84, P5 170, P6 129 |
| M2 | ★: the dearest row alone paid on the way back | P1 72, P2 136, P4 35, P5 74, P6 72 |
| M3 | ★: the start paid for on the way back, home not | P1 154, P2 246, P5 167, P6 154 |
| M4 | walk: each row paid as it is left | P1 167, P2 167, P3 248, P6 167 |
| M5 | walk: a free column costing 1 | P1 11, P2 14, P3 17, P6 11 |
| M6 | walk: the start's row paid | P1 327, P2 167, P3 321, P4 340, P6 327 |
| M7 | prefix: the start counted going forward | P1 297, P2 247, P4 245, P5 170, P6 297 |
| M8 | prefix: the sums not carried | P1 224, P2 246, P4 151, P5 172, P6 224 |
| M9 | prefix: the columns walked from home | P1 172, P2 172, P3 248, P6 172 |
| M10 | filter: the dearest place alone paid | P1 138, P2 104, P4 75, P6 138 |
| M11 | filter: the higher end taken as home | P1 73, P2 139, P4 35, P5 75, P6 73 |
| M12 | filter: the first place never paid | P1 95, P2 159, P4 48, P5 83, P6 95 |
| M13 | axis: the start paid going forward, home not | P1 132, P2 246, P5 167, P6 132 |
| M14 | axis: the columns' costs halved | P1 177, P2 164, P3 250, P6 177 |
| M15 | axis: each place forward one dearer | P1 137, P2 243, P5 179, P6 137 |
| M16 | solution: home's row paid at every step | P1 73, P2 70, P3 136, P6 73 |
| M17 | solution: the adapter's numbers halved | P1 253, P2 244, P4 179, P5 119, P6 253 |

P1, P2 and P6 kill all seventeen, P5 ten, P4 nine, and P3 six. P2, which
walks the robot back and expects the two ends' costs to trade places,
sees every edit, since each one pays for the wrong end of a range, pays
a place twice or not at all, or treats the two ways differently. P5,
which mirrors the rows so that a walk down becomes a walk up, sees an
edit that treats the two directions differently (M1, M2, M3, M7, M8,
M11, M12, M13, M15) or moves the robot (M17). P4 sees an edit that pays
for the wrong number of rows (M1, M6, M7, M11, M12) or does not add the
costs up (M2, M8, M10), or moves the robot (M17). P3, which trades rows for columns, sees only an
edit that treats them differently: the columns halved (M14), dearer
(M5), walked from home (M9), a row paid as it is left (M4) or at home's
cost (M16), the start's row paid (M6).

Of the thirty-two, fifteen were not kept, and none survives. Three fail
as a kept one: the prefix and axis arms' way back shifted a place as
M3, and the ★ arm's rows walked from home to the start as M4. Twelve are
killed with checks of their own but were left out because their arm
keeps three, or the Rust arm two: the ★ arm's columns' cost taken off,
the axis arm's columns paid twice and the Rust arm's columns never
walked, which fail alike (P1 177, P2 172, P3 252); the filter arm's home
left out instead of the start and the Rust adapter's start and home
swapped (P1 246, P2 246); the filter arm's higher end left out and the
★ arm's home not paid going forward (P1 132, P2 247, P4 84, P5 174); the
walk arm's home column not paid (P1 329, P2 172, P3 328); the Rust arm's
columns one dearer (P1 181, P3 224) and its cost starting at 1 (P1 340);
the prefix arm's way back paying the first place too (P1 157, P2 242,
P4 95, P5 171); the axis arm's way back skipping its first place (P1
160, P2 247, P4 95, P5 175).

## Verification

Every arm prints the same output as `homecoming.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.9 s to 1.6 s, but for the
filter arm's 2.4 s, which looks at every place of both axes for each
grid, and the differential 0.6 s (timed while other work shared the
machine).

The Rust arm met one compiler gap. It walks the robot home with
`r += if hr > r { 1 } else { -1 };` over `r: i32`, and an `if` whose
every value is an unsuffixed literal was typed `i64` at once, so the
sum widened and the store was refused as narrowing, with no fix
(B-2026-11-10-6, filed by kata 2055). As an operand, or the value of a
compound assignment, such an `if` or `match` now takes the other
operand's type when every literal fits it, as a literal written there
does. Fixed in kara 81aca4606b, test `tests/kata_2087_literal_if_operand.rs`.
The same `if` bound by a `let` first and added in later is typed
`i64`, as design.md §8 Literals means it to be: a binding's literal
beside a type that widens keeps its default, so that form writes `let
step: i32`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds of 31, 2 and 1 edits: Rust's spellings (`Vec<i32>` to
brackets, `let (mut r, mut c)` to `let mut (r, c)`, the adapter's `&`s
and `&Vec<i64>`, the `&` of `|&x|`, `struct Solution;` to `struct
Solution {}`, `Solution::` to `.`); then `let mut ans = 0` to `ans: i32`,
as the literal kept the default `i64` against the `i32` the method
returns, and the adapter's `as i64`, which the `i32` widens to anyway;
then the adapter's `ref Vec[i64]` parameter to a bare one, which
borrows already. The fixed arm reads as the template does, `as usize`
index and all.

## Benchmarks

The bench builds one grid of `10^6` rows and `10^6` columns, each cost up
to `10^4`, and walks 2000 trips home between random places on it with
the ★ arm in all five languages, each trip the two ranges of costs
summed over a view where the language has one (a `Slice`, a Rust
slice, a Go slice, a pointer and a length) and a copied slice in Python:
about `1.3 · 10^9` costs added. Every implementation prints `2000 trips:
sum 6096860643703, checksum 10512380`.

BENCHTAB
