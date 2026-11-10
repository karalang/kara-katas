# 2069. Walking Robot Simulation II

A `width x height` grid is on an XY-plane with the bottom-left cell at
`(0, 0)` and the top-right cell at `(width - 1, height - 1)`. The grid is
aligned with the four cardinal directions (`"North"`, `"East"`,
`"South"`, and `"West"`). A robot is initially at cell `(0, 0)` facing
direction `"East"`.

The robot can be instructed to move for a specific number of steps. For
each step, it does the following.

1. Attempts to move forward one cell in the direction it is facing.
2. If the cell the robot is moving to is out of bounds, the robot
   instead turns 90 degrees counterclockwise and retries the step.

After the robot finishes moving the number of steps required, it stops
and awaits the next instruction.

Implement the `Robot` class:

- `Robot(int width, int height)` Initializes the `width x height` grid
  with the robot at `(0, 0)` facing `"East"`.
- `void step(int num)` Instructs the robot to move forward `num` steps.
- `int[] getPos()` Returns the current cell the robot is at, as an array
  of length 2, `[x, y]`.
- `String getDir()` Returns the current direction of the robot,
  `"North"`, `"East"`, `"South"`, or `"West"`.

```
Robot(6, 3), step(2), step(2), getPos(), getDir(), step(2), step(1), step(4), getPos(), getDir()
  ->  null, null, null, [4, 0], East, null, null, null, [1, 2], West
```

**Constraints:** `2 <= width, height <= 100`; `1 <= num <= 10^5`; at
most `10^4` calls in total are made to `step`, `getPos`, and `getDir`.

The robot never leaves the edge of the grid: it starts in a corner,
walks along a side, and turns only at the next corner. So it walks a
loop of `2 (width + height) - 4` cells, and a step of `num` lands where
a step of `num` modulo the loop's length does. The one catch is the way
it faces: at `(0, 0)` it faces east before its first step and south ever
after, since it reaches that corner walking down the left side. The
approaches differ in how they keep the robot, and two walk it.

## Approaches

| file | mechanism |
|---|---|
| `robot.kara` ★ | the robot as its place on the loop of the edge, counted from `(0, 0)` going east, and a `moved` flag; a step adds modulo the loop's length, and the cell and the way it faces are read off the side the place is on. O(1) a call |
| `robot_table.kara` | every cell of the loop laid out once in a table, each with the way the robot faces there, built by walking it with `const` steps (`Array[i64, 4]`, `Array[Str, 4]` names) and `rotate_right(1)` to start at `(0, 0)`; the robot is its index |
| `robot_walk.kara` | the robot walked a cell at a time as the statement says, a turn the parallel assignment `dx, dy = -dy, dx`, `num` cut to the loop's length first with a whole loop kept for a remainder of 0; the way it faces a `match` on `(dx, dy)` |
| `robot_sides.kara` | a side at a time: an `enum Facing` with `turned` and `name`, a method `room` for the cells ahead before the edge, and a step that goes as far along the side as it can, turns and goes on |
| `robot_coords.kara` | the robot kept as its cell and the name of the way it faces, each step a round trip through the loop: the cell's place found by a `match` on `(x, y)` with guards, then the new place turned back into a cell and a name |
| `robot_solution.kara` | LeetCode's Rust template (`struct Robot` of `i32`s, `fn new(..) -> Self`, `&mut self` and `&self` receivers, `vec![..]` positions, `.to_string()` names), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm makes the same calls through one driver that takes LeetCode's
form, a list of calls (a step of `num`, `getPos`, `getDir`), and answers
each as LeetCode prints it. It prints the same 4 lines: LeetCode's
example and a robot walked round its edge exactly; then a checksum of
the answers for 300 random robots of 2 to 12 by 2 to 12, each with 1 to
40 calls, half of them steps of up to 60 or up to 100000 cells; then the
checksum and the last answers for the constraints' largest, a 100 by
100 robot with 10000 calls. `robot.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the robot moved one cell at a time for every unit of every
step, turning counter-clockwise whenever the next cell is off the grid,
with nothing cut short. It checks 300 random robots of 2 to 8 by 2 to 8
with 1 to 30 calls of steps up to 60; then 20 of 2 to 3 by 2 to 3 with
steps up to 1000, and 20 whose steps are one, two or three whole loops
of the edge, one cell less, exactly, or one cell more. All 340 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | every step a whole loop of the edge longer leaves every answer |
| P3 | every step split in two leaves every answer, the extra step's `null` aside |
| P4 | every position is a cell on the grid's edge |
| P5 | before any step the robot is at `(0, 0)` facing east, and after a step of one whole loop at `(0, 0)` facing south |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 robots: checksum 498232614, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
robots. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Twenty-nine edits to the differential, four to six to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones and the
survivor under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed, fails
the same way under both backends and not by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the loop four cells too long | P1 279, P2 268, P4 112, P6 279 |
| M2 | ★: the top right corner facing west | P1 42, P6 42 |
| M3 | ★: the left column read from the bottom | P1 73, P6 73 |
| M4 | table: the table not turned round to start at `(0, 0)` | P1 303, P5 340, P6 303 |
| M5 | table: the start facing south before any step | P1 113, P5 340, P6 113 |
| M6 | table: the table one cell short | P1 304, P2 286, P5 340, P6 304 |
| M7 | walk: a quarter turn clockwise | P1 281, P3 21, P5 340, P6 281 |
| M8 | walk: a turn costing a cell | P1 280, P3 249, P5 340, P6 280 |
| M9 | walk: the top row out of reach | P1 279, P3 230, P4 78, P5 340, P6 279 |
| M10 | sides: one cell more room going west | P1 266, P3 253, P4 150, P5 340, P6 266 |
| M11 | sides: a remainder of 0 walking nothing | P1 15, P3 13, P5 340, P6 15 |
| M12 | sides: south going up | P1 265, P3 241, P4 251, P5 340, P6 265 |
| M13 | coords: the top row's places counted from the left | P1 186, P3 198, P6 186 |
| M14 | coords: the start facing east after a step | P1 65, P5 340, P6 65 |
| M15 | coords: a step not taken round the loop | P1 288, P2 278, P3 12, P4 272, P6 288 |
| M16 | solution: the adapter's position the other way round | P1 260, P4 176, P6 260 |
| M17 | solution: the loop's length from the width alone | P1 227, P2 197, P4 47, P5 118, P6 227 |

P1 and P6 kill all seventeen, P5 eleven, P3 eight, P4 seven and P2
four. P5 is the corner the statement turns on, and `P5 340` is an arm
wrong there for every grid: facing east at `(0, 0)` after a step (M14),
or not before one (M5), or not standing there after a whole loop. P3
sees an edit whose answer depends on where a step stops (M7 to M13,
M15); P2 an arm whose loop is the wrong length (M1, M6, M17) or which
never takes a step round it (M15); P4 a robot that leaves the edge, or
an adapter that reports `[y, x]` (M16), which is off the edge of a grid
that is not square.

Of the twenty-nine, twelve were not kept. One survives, and it is
equivalent: the Rust arm's right column one cell short, since the one
place it moves to the top row's branch is the top right corner, which
that branch gives the same. One never ends and is not kept: the sides
arm's north turning to east leaves the robot at the top right corner
with no room either way, turning for ever, and was stopped at 300 s.
Four fail as a kept one: the ★ arm's `(0, 0)` facing east even after a
step, and the ★ and Rust arms' step that never marks the robot moved, as
M14; the walk arm's remainder of 0 walking nothing as M11. Two fail
alike and neither is kept: the table arm's step counted from the next
cell and the Rust adapter's step one more (P1 290, P3 291, P5 340). Four
are killed with checks of their own but were left out because their
arm keeps three: the table arm's quarter turn clockwise (P1 294, P4 158,
P5 340), the walk arm starting north (P1 313, P3 19, P5 340), the sides
arm's right column climbed one short from the bottom (P1 58, P3 34, P5
74), and the coords arm's left column counted from the bottom (P1 118,
P3 120).

## Verification

Every arm prints the same output as `robot.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

Under `karac __mir-run` the arms take 0.4 s to 0.6 s and the
differential 1.4 s (timed while other work shared the machine).

No arm met a compiler gap. The differential's test of a position on the
edge was first written with Rust's `trim_start_matches("[")`; the
checker named `strip_prefix`, and the test takes the text between the
brackets with `slice`. Its first parse of a number, a made-up
`parse_i64`, met a plain unknown-method error; Rust's own
`s.parse::<i64>()` is refused with the Kāra form, `i64.parse(s)`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 15 and 11 edits: Rust's spellings (`Vec<..>` to
brackets, `&mut self` to `mut ref self`, `&self` to `self`, `Robot::new`
and `Vec::new` to `.`, `format!` to an f-string, the `&` of `&(call,
num)` dropped); then the four `vec![..]` positions to list literals and
seven `.to_string()`s on a literal where a `String` is wanted dropped:
the first are deprecation warnings and the second a lint, all of which
`karac check` passes. The fixed arm reads as the template
does, `i32`s and all.

## Benchmarks

The bench makes 10000000 calls with the ★ arm in all five languages: 200
robots of 2 to 100 by 2 to 100, 50000 calls each, half of them steps of
up to 100000 cells and the rest `getPos` and `getDir`, every answer
folded into a checksum. Kāra, Rust and Go build a two-number list for
each `getPos` and Kāra and Rust a `String` for each `getDir`; C writes
the cell into the caller's pair and hands back a constant name. Every
implementation prints `200 robots, 10000000 calls: checksum 774961671`.

BENCHTAB
