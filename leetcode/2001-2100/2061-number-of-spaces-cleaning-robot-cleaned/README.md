# 2061. Number of Spaces Cleaning Robot Cleaned

A room is represented by a 0-indexed 2D binary matrix `room` where a `0`
represents an empty space and a `1` represents a space with an object.
The top left corner of the room will be empty in all test cases.

A cleaning robot starts at the top left corner of the room and is facing
right. The robot will continue heading straight until it reaches the edge
of the room or it hits an object, after which it will turn 90 degrees
clockwise and repeat this process. The starting space and all spaces that
the robot visits are cleaned by it.

Return the number of clean spaces in the room if the robot runs
indefinitely.

```
room = [[0,0,0],[1,1,0],[0,0,0]]  ->  7
room = [[0,1,0],[1,0,0],[0,0,0]]  ->  1
room = [[0,0,0],[0,0,0],[0,0,0]]  ->  8
```

**Constraints:** `m == room.length`; `n == room[r].length`;
`1 <= m, n <= 300`; `room[r][c]` is either `0` or `1`; `room[0][0] == 0`.

The robot's whole state is its cell and the way it faces, `4 · m · n`
states at most, and each state has one next state. So its walk runs into
a loop within `4 · m · n` moves and repeats it forever; the answer is the
number of cells the walk stands on up to the loop's first repeat. The
approaches differ in how they notice the loop.

## Approaches

| file | mechanism |
|---|---|
| `robot.kara` ★ | the robot walked one move at a time, each state marked in a `Vec[bool]` of `m · n · 4` and each cell in another, until a state comes round again; the steps are two `const` arrays. O(m · n) |
| `robot_runs.kara` | a straight run at a time: from where it last turned, on to the last empty cell before an edge or an object (a closure tests a cell), then a turn; only the states it turns from are kept, in a `Set[(i64, i64, i64)]`, and the cells in a `Set[(i64, i64)]` |
| `robot_bounded.kara` | no states kept at all: by its `4 · m · n`-th move the robot has met every state it ever will, so it is walked exactly that many moves, a turn the parallel assignment `dr, dc = dc, -dr`, and the cells it stood on counted in a `Set` |
| `robot_floyd.kara` | the walk as a function from state to state, its loop found by Floyd's tortoise and hare with nothing stored: `mu` moves to reach the loop, `lambda` round it; then `mu + lambda` moves walked and the cells marked in a `Vec[Vec[bool]]` |
| `robot_struct.kara` | the robot as a value: an `enum Facing` with `turned` and `step`, a `struct Robot` deriving `Copy`, `Eq` and `Hash`, the states met a `Set[Robot]`, and the cells a `Map` from each to the facings the robot stood on it with |
| `robot_solution.kara` | LeetCode's Rust template (`Vec<Vec<i32>>`, a `vec![vec![0u8; n]; m]` of direction bits per cell, `1 << d`, `usize` places with `as i32` and `as usize` round trips, `loop` and `break`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples and five
more, each room and its answer; then the sum of the answers and a
checksum for 500 random rooms of 1 to 12 by 1 to 12, objects with a
chance of 0 to 50 in 100; then the answers for four rooms of 300 by 300,
objects with a chance of 0, 1, 3 and 10 in 100. `robot.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the robot moved once at a time, every state it has been in
kept in a list and each new one looked for in all of it, the cells it
stood on counted once each. It checks 300 random rooms of 1 to 8 by 1 to
8, then 40 of a single row or column, 20 with no objects, and 40 whose
first row and column are blocked early (an object at row 1 of column 0
and one in row 0), where the robot often comes to its loop by a turn,
partway round it. All 400 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least 1 and at most the number of empty cells |
| P3 | an empty cell the robot never stands on, made an object, leaves the answer |
| P4 | a row of objects added below and a column of them to the right leave the answer |
| P5 | the answer is at least the empty cells the first row starts with and the empty cells straight below the last of them |
| P6 | each arm agrees with at least three of the other five |

P4 holds because the robot meets an object as it meets an edge.

The differential prints `400 rooms: checksum 971391955, 14400 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
rooms. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, four to seven to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones under `karac
__mir-run` too. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under both
backends and not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the bottom row out of reach | P1 211, P3 29, P4 211, P5 115, P6 211 |
| M2 | ★: an object walked through | P1 290, P2 155, P4 400, P6 290 |
| M3 | ★: up a step down | P1 194, P3 53, P6 194 |
| M4 | runs: the cell turned at not cleaned | P1 140, P2 49, P5 74, P6 140 |
| M5 | runs: a run looking two cells ahead | P1 368, P3 78, P5 205, P6 368 |
| M6 | runs: a turning state kept without its direction | P1 85, P5 75, P6 85 |
| M7 | bounded: a quarter of the moves | P1 53, P4 53, P5 26, P6 53 |
| M8 | bounded: a quarter turn counter-clockwise | P1 176, P3 61, P5 69, P6 176 |
| M9 | bounded: the top row out of reach | P1 277, P3 63, P5 147, P6 277 |
| M10 | floyd: the moves to the loop left out | P1 64, P5 14, P6 64 |
| M11 | floyd: the loop one move short | P1 10, P6 10 |
| M12 | floyd: down a step up | P1 255, P5 255, P6 255 |
| M13 | struct: left a step right | P1 187, P3 35, P6 187 |
| M14 | struct: the states counted, not the cells | P1 400, P2 177, P6 400 |
| M15 | struct: the robot starting down | P1 88, P3 24, P6 88 |
| M16 | solution: a cell first stood on facing right counted twice | P1 400, P2 110, P6 400 |
| M17 | solution: left and up swapped | P1 155, P6 155 |

P1 and P6 kill all seventeen, P5 nine, P3 seven, P2 four and P4 three.
The 40 rooms blocked early are what kill M11: the first 360 rooms never
had the robot come to its loop by a turn in a way that left a cell stood
on only by the loop's last state, and M11 and one like it survived. A
search of every room up to 4 by 4 and 200000 random ones up to 10 by 10
found such rooms (905 of 237477, none smaller than 4 by 4), shaped like
the family now drawn: 10 of its 40 kill M11. P2 sees answers too large
for the room (M2, M14, M16) or a start never counted (M4). P3 and P4 see
edits that make the robot's path depend on cells it should never reach:
an edge moved in (M1, M9), a robot that walks through objects (M2) or is
cut short (M7). P5 catches edits that lose the first two runs, a turn
the wrong way or a step reversed.

Of the thirty-one, fourteen were not kept. Ten fail as a kept one: the ★
arm's cell counted each time it is stood on as M14; the ★ and runs arms'
quarter turn counter-clockwise as M8; the ★ arm's state kept without its
direction, the Floyd arm's half turn and the struct arm's right turned
to up as M12; the bounded arm's robot starting down as M15; the Floyd
arm's one move fewer walked as M11; the struct and Rust arms' top row
out of reach as M9. Four are killed with checks of their own but were
left out because their arm keeps three or two: the ★ arm's count started
at one (P1 400, P2 92), the runs arm's last column out of reach (P1 198,
P3 34, P4 198, P5 109), and the Rust arm's adapter swapping objects and
empty cells (P1 388) and its robot never facing up (P1 154, P3 28).

## Verification

Every arm prints the same output as `robot.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

Under `karac __mir-run` the arms take 0.6 s to 1.1 s, except the
bounded arm at 2.1 s, which takes all `4 · m · n` moves in every room,
and the differential 1.1 s (timed while other work shared the machine).

No arm met a compiler gap. Four Rust spellings in the first drafts were
each refused with the Kāra form and carried by `karac fix`: the ★ arm's
`[i64; 4]` (to `Array[i64, 4]`) and `let (mut r, mut c, mut d)` (to
`let mut (r, c, d)`), the bounded arm's `(dr, dc) = (dc, -dr)` (to `dr,
dc = dc, -dr`), and the struct arm's `#[derive(Copy, Eq, Hash)]`, to
which `karac fix` adds the `Clone` and `PartialEq` they need.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds of 13, 2 and 1 edits: `Vec<..>` to brackets, the
`mut` of each binding moved before the pattern, `&&` to `and`, `struct
Solution;` to `struct Solution {}` and `Solution::` to `Solution.`; then
the inner `vec![0u8; n]` to `Vec.filled` and the adapter's `as i64` that
the `i32` answer widens to anyway; then the outer `vec![..; m]`. The
last three come from lints that are allowed under `karac check`, which
passes the arm after the first round, and on under `karac fix`. The fixed arm reads as the template does,
`usize` places and all.

## Benchmarks

The bench walks the robot through 600 spiral rooms of 200 to 300 by 200
to 300 with the ★ arm in all five languages, one move at a time, the
states and cells it has seen kept per room. Every implementation prints
`600 rooms: 18895001 cleaned, checksum 333332282`.

BENCHTAB
