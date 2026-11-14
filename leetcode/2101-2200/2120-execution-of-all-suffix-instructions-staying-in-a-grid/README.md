# 2120. Execution of All Suffix Instructions Staying in a Grid

There is an `n x n` grid, with the top-left cell at `(0, 0)` and the
bottom-right cell at `(n - 1, n - 1)`. You are given the integer `n` and
an integer array `startPos` where `startPos = [startrow, startcol]`
indicates that a robot is initially at cell `(startrow, startcol)`.

You are also given a 0-indexed string `s` of length `m` where `s[i]` is
the `i`th instruction for the robot: `'L'` (move left), `'R'` (move
right), `'U'` (move up), and `'D'` (move down).

The robot can begin executing from any `i`th instruction in `s`. It
executes the instructions one by one towards the end of `s` but it stops
if either of these conditions is met:

- The next instruction will move the robot off the grid.
- There are no more instructions left to execute.

Return an array `answer` of length `m` where `answer[i]` is the number
of instructions the robot can execute if the robot begins executing
from the `i`th instruction in `s`.

```
n = 3, startPos = [0, 1], s = "RRDDLU"  ->  [1, 5, 4, 3, 1, 0]
n = 2, startPos = [1, 1], s = "LURD"    ->  [4, 1, 0, 0]
n = 1, startPos = [0, 0], s = "LRUD"    ->  [0, 0, 0, 0]
```

**Constraints:** `m == s.length`; `1 <= n, m <= 500`; `startPos.length
== 2`; `0 <= startrow, startcol < n`; `s` consists of `'L'`, `'R'`,
`'U'`, and `'D'`.

With `m` at most 500, walking every suffix from the start is at most
125250 moves, so the direct simulation is the intended answer. The
other arms differ in how a walk is written down, and one in what it
keeps: the robot leaves the grid at the first move that takes its row
or column offset from the start past an edge, so the farthest offsets
in each direction are all a suffix needs.

## Approaches

| file | mechanism |
|---|---|
| `suffix.kara` ★ | each suffix simulated over `bytes()` with a `match` on the move, stopping at the first one off the grid. O(m^2) |
| `suffix_struct.kara` | a `struct Robot { n, row, col }` whose `step` (`mut ref self`) moves only when the move stays on the grid and says whether it did; a fresh robot per suffix |
| `suffix_scan.kara` | each move turned into a `(dr, dc)` pair once; per suffix, `scan` carries the position over the pairs, `take_while` stops off the grid and `count` answers |
| `suffix_recurse.kara` | `moves_from(n, s, j, row, col)` over a `Slice[u8]`: zero when no move is left or the next one leaves, else one more than the moves from where it lands |
| `suffix_bounds.kara` | per suffix, only the least and most row and column offsets from the start; a suffix stops at the first move that pushes one of them past an edge |
| `suffix_solution.kara` | LeetCode's Rust template: the simulation over `as_bytes()` with `i32` positions into a `vec![0; m]`, carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and three
more (a one-cell grid with one move, a robot in the corner, a walk
along an edge), each with its answer; then the total moves and a
checksum of the answers over 2000 random grids of side 1 to 8 with 1 to
30 moves; then the constraints' largest, 500 moves going round a square
from the centre of a 500 grid. `suffix.py` mirrors the ★ arm and its
output is byte-identical.

Two arms were first written with Rust's spellings and carried by `karac
fix` in one round each. The scan arm's closure wrote its state through
`*at = ..` and returned `Some(*at)`, as Rust's `scan` takes a `&mut`;
Kāra's `scan` takes the state by value and returns the next one with
the item, and the fix rewrote the body to `let at = (at.0 + dr, at.1 +
dc); Some((at, at))`. The bounds arm's `let (mut dr, mut dc)` and `let
(mut up, mut down, mut left, mut right)` became `let mut (dr, dc)` and
`let mut (up, down, left, right)`, 8 edits.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the grid's cells put in a `Set`, and each suffix walked
until the robot's next cell is not one of them. It checks 300 random
grids of side 1 to 6 with 1 to 20 moves; then 30 of side up to 20 with
up to 80 moves; then 30 of side 1 to 3, where most moves leave. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | one answer per instruction, the answer for `i` between 0 and the `m - i` moves left |
| P3 | the grid seen in a mirror (`L` and `R` swapped, the start's column reflected): the same answers |
| P4 | the grid transposed (`L` with `U`, `R` with `D`, the start's row and column swapped): the same answers |
| P5 | a grid one larger, the same start: no answer falls |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 grids: checksum 253903134, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
grids. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, five to six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the bottom edge one row too far | P1 192, P4 279, P6 192 |
| M3 | ★: the move that leaves counted | P1 328, P6 328 |
| M6 | ★: the start's column read as its row | P1 184, P3 222, P4 198, P6 184 |
| M7 | struct: the left edge ignored | P1 175, P3 282, P4 251, P6 175 |
| M8 | struct: one robot for every suffix | P1 230, P5 79, P6 230 |
| M10 | struct: `R` stays put | P1 258, P3 299, P4 313, P6 258 |
| M13 | scan: `filter` for `take_while` | P1 262, P6 262 |
| M14 | scan: each move made from the start | P1 215, P6 215 |
| M17 | scan: `U` read as `L` | P1 209, P3 213, P4 239, P6 209 |
| M18 | recurse: the end counted as a move | P1 232, P2 232, P6 232 |
| M21 | recurse: the last row off the grid | P1 166, P4 219, P6 166 |
| M23 | recurse: the start transposed | P1 198, P3 254, P6 198 |
| M24 | bounds: `up` tracking the largest offset | P1 195, P4 251, P6 195 |
| M25 | bounds: `right` never grows | P1 204, P3 282, P4 279, P6 204 |
| M27 | bounds: the offsets kept across suffixes | P1 229, P6 229 |
| M29 | solution: the position kept across suffixes | P1 280, P5 48, P6 280 |
| M32 | solution: the last move never made | P1 232, P6 232 |

P1 and P6 kill all seventeen, P4 eight, P3 six, P5 two and P2 one. P4
and P3 see the edits that treat one direction or one edge unlike its
partner: the transpose swaps rows with columns and the mirror swaps
left with right, so a wrong edge (M1, M7, M21, M25), a wrong move or offset (M10,
M17, M24) or a start read the wrong way round (M6, M23) answers
differently once the grid is turned. The edits that treat every
direction alike are seen by P1 alone, or with P5 when a suffix starts
where the last one stopped (M8, M29): in a larger grid that robot has
wandered differently, and an answer can fall. P2 sees the one edit
that answers more moves than are left (M18); the move that leaves
counted (M3) never does, since it stops there.

Of the thirty-two, fifteen were not kept, all killed. Seven fail as a
kept one does: the move that leaves counted in the recurse and Rust
arms, and the scan arm checking the cell before the move, as M3; the
recurse arm's position never carried as M14; the bounds arm's bottom
edge as M1; the Rust arm's right edge as M25; and the struct arm's last
move never made as M32. Eight are killed with checks of their own but
were left out because their arms keep their share: `L` and `R` swapped
(P1 223, P4 262), the first move skipped (P1 271, also in the scan
arm), and `U` read as `D` (P1 213, P4 249) in the ★ arm; every step the
suffix's first (P1 233) and the column never updated (P1 172, P4 215)
in the struct arm; `U` also moving left (P1 172, P3 194, P4 220) in the
recurse arm; and `L` read as `U` (P1 225, P3 252, P4 239) in the bounds
arm.

## Verification

Every arm prints the same output as `suffix.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.35 s to 0.75 s, the scan arm
1.4 s, and the differential 1.2 s; compiled it takes 0.5 s.

`karac fix` carries the template in two rounds of 20 and 2 edits:
`Vec<i32>` to `Vec[i32]`, the `mut` inside the tuple pattern moved
before it, `||` to `or`, the closures' `|&x|` to `|x|`, `struct
Solution;` to `struct Solution {}` and `::` to `.`; then `as_bytes()` to
`bytes()` and `vec![0; m]` to `Vec.filled(m, 0)`. No compiler gap was met.

## Benchmarks

The bench builds 40 grids once, each of side 100 to 500 with a start
inside and 500 random moves, then solves every grid 20 times, the start
one row lower (wrapping) in each round so that no solve repeats one
before, with the ★ arm in all five languages. Every implementation
prints `800 solves: 91415659 moves, checksum 446209668`.

BENCHTAB
