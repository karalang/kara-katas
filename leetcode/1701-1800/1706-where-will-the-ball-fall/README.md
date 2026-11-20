# 1706. Where Will the Ball Fall

You have a 2-D `grid` of size `m x n` representing a box, and you have
`n` balls. The box is open on the top and bottom sides.

Each cell in the box has a diagonal board spanning two corners of the
cell that can redirect a ball to the right or to the left.

- A board that redirects the ball to the right spans the top-left corner
  to the bottom-right corner and is represented in the grid as `1`.
- A board that redirects the ball to the left spans the top-right corner
  to the bottom-left corner and is represented in the grid as `-1`.

We drop one ball at the top of each column of the box. Each ball can get
stuck in the box or fall out of the bottom. A ball gets stuck if it hits
a "V" shaped pattern between two boards or if a board redirects the ball
into either wall of the box.

Return *an array* `answer` *of size* `n` *where* `answer[i]` *is the
column that the ball falls out of at the bottom after dropping the ball
from the* `ith` *column at the top, or `-1` if the ball gets stuck in the
box.*

```
grid = [[1,1,1,-1,-1],[1,1,1,-1,-1],[-1,-1,-1,1,1],[1,1,1,1,-1],[-1,-1,-1,-1,-1]]  ->  [1,-1,-1,-1,-1]
grid = [[-1]]                                                                     ->  [-1]
grid = [[1,1,1,1,1,1],[-1,-1,-1,-1,-1,-1],[1,1,1,1,1,1],[-1,-1,-1,-1,-1,-1]]       ->  [0,1,2,3,4,-1]
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`1 <= m, n <= 100`; `grid[i][j]` is `1` or `-1`.

## Approaches

| file | mechanism |
|---|---|
| `ball.kara` ★ | each ball followed down a row at a time: in row r at column c the board sends it to c + grid[r][c], which it reaches only if that column is inside the box and its board slopes the same way; a wall or a V stops it. O(m * n) |
| `ball_rows.kara` | every ball moved together: `place[b]` is ball b's column, -1 once stuck, and each row moves every ball still falling by the same rule, so the rows are walked once, outermost. O(m * n) |
| `ball_exits.kara` | where a ball leaves from any column, worked out from the bottom up: `exit[c]` for the rows below, rewritten a row at a time from the last row up, so the table for the top row answers every starting column. O(m * n) |
| `ball_solution.kara` | a Rust solution as LeetCode's Rust users write it, `(0..n).map(\|start\| { .. }).collect()` with the column an `i32`, `as usize` at each index, `return -1` from the closure, and `for row in &grid`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

The answer prints as a list. Every arm prints the same 8 lines:
LeetCode's three examples, a V in one row, and boards pointing out to
both walls; then the balls that fall out and a checksum of every answer
for 3000 random boxes of up to 6 by 6, 300 of up to 30 by 30 and 100 of
up to 100 by 100, LeetCode's largest, each board 1 with a chance of its
box's own. `ball.py` mirrors the ★ arm and its output is byte-identical.

```
[1, -1, -1, -1, -1]
[-1]
[0, 1, 2, 3, 4, -1]
[-1, -1]
[-1, 0, 3, -1]
3000 boxes of up to 6 by 6: 1712 balls out, checksum 739217342
300 boxes of up to 30 by 30: 432 balls out, checksum 308680371
100 boxes of up to 100 by 100: 305 balls out, checksum 63946310
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, in the box's geometry: a ball falls into a row in the middle
of its column, rolls down the board to the corner it slopes to, and at
that corner is stopped by the wall, or by the next cell's board when that
board ends at the same corner (a V); otherwise it is under that board and
drops into the next row in the middle of that cell. Positions are kept
in doubled coordinates so the middles and corners are whole numbers. It
checks 3000 random boxes of 1 to 6 rows by 1 to 6 columns. Every case is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the box mirrored, every board turned, gives the answer mirrored |
| P3 | a row of 1s on top moves every ball one column on, the last stuck |
| P4 | no two balls fall out of the same column |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 658330404, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading gives the same checksum. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first drafts were replaced: the
exits arm's test that the next board is not the opposite of this one,
`!= -row[c]`, is the same test as `== row[c]` for boards of 1 and -1;
and a solution arm that let a ball reach the wall's column ran off the
row. M1, which ignores the V, is the one P4 sees most: balls that should
stick in a V are let through, and two of them can land together.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a V does not stop a ball | P1 1075, P4 599, P5 1075 |
| M2 | ★: a ball that reaches column 0 counted as stuck | P1 355, P2 682, P5 355 |
| M3 | ★: a ball that falls out reported at its starting column | P1 840, P3 733, P5 840 |
| M4 | rows: the balls after a stuck one left where they are | P1 1227, P2 1413, P3 875, P4 7, P5 1227 |
| M5 | rows: a stuck ball left in its column, not -1 | P1 3000, P3 3000, P4 2464, P5 3000 |
| M6 | exits: a ball's next column taken as where it falls out | P1 1828, P3 2535, P5 1828 |
| M7 | exits: the rows taken from the top down | P1 371, P3 636, P5 371 |
| M8 | exits: a stuck ball read as falling out of column 0 | P1 3000, P2 2535, P3 3000, P4 2422, P5 3000 |
| M9 | solution: a stuck ball reported at the column it stuck in | P1 3000, P3 3000, P4 2159, P5 3000 |
| M10 | solution: a ball moved half a column, which rounds to none | P1 1484, P3 1404, P5 1484 |

## Benchmarks

The bench draws 1000 random boxes of 100 by 100, LeetCode's largest,
each row long runs of one slope (a board turns the other way one time
in 20, so balls get past more rows), all of them first, then answers
each 100 times by the ★ arm in all five languages. Every implementation
prints `1000 boxes of 100 by 100, 100 rounds: 44900 balls out, checksum
13287252`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 1.095 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.332 s |
| Kāra (`karac build`) | 1.444 s |
| Go | 1.594 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.605 s |
| Rust (`rustc -O`) | 1.659 s |
| Python | 15 s |

The sequential Kāra build is 20% faster than Rust and 17% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md). C is the fastest here at 1.095 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.128 s and 1.156 s on one
run).

## Verification

All four arms print the same output as `ball.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and rows arms checked clean as first written. The exits arm's
first draft took each row `let row = grid[r];`, a move out of an index
that `karac check` refused (E_INDEX_MOVE_NON_COPY); the row is only
read, and `karac fix` wrote `ref grid[r]`.

LeetCode's Rust template took one `karac fix`: `struct Solution {}`
added, the `Vec<..>`s written in brackets, `for row in &grid` written
`for row in ref grid`, and the two `||` written `or`. The `i32` column
indexing as `row[c as usize]` carried over as written, as #1700's
`usize` index did: Kāra takes a `usize` index where it does not meet an
`i64`.

The bench's first draft flipped `let mut board = 1;` by `-board` and
pushed it into a `Vec[i32]`; nothing fixes the literal's type there, so
it kept the default `i64`, and `karac check` refused the push as a
narrowing (E0200) and named the declaration; `karac fix` wrote `board:
i32`.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
