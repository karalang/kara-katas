# 489. Robot Room Cleaner

You are controlling a robot that is located somewhere in a room. The
room is modelled as an `m × n` binary grid where `0` is a wall and `1`
an empty cell. The robot starts at an unknown location in the room that
is guaranteed to be empty, and you do not have access to the grid, but
you can move the robot using the given API `Robot`.

Use the robot to clean the entire room, every empty cell. The robot can
move forward, turn left or turn right, each turn 90 degrees. When it
tries to move into a wall, its bumper detects the obstacle and it stays
on its cell.

```
interface Robot {
    boolean move();      // true if the robot moved into the cell ahead
    void turnLeft();
    void turnRight();
    void clean();        // clean the current cell
}
```

The robot starts facing up. All four edges of the grid are surrounded
by walls.

```
room = [[1,1,1,1,1,0,1,1],
        [1,1,1,1,1,0,1,1],
        [1,0,1,1,1,1,1,1],
        [0,0,0,1,0,0,0,0],
        [1,1,1,1,1,1,1,1]],  row = 1, col = 3  ->  every empty cell cleaned
```

**Constraints:** `1 <= m <= 100`; `1 <= n <= 200`; `room[row][col] == 1`.

## Approaches

The `Robot` here is a struct in the harness that holds the hidden room;
its calls are `forward()`, `turn_left()`, `turn_right()` and `clean()`.
Every arm is `fn clean_room(robot: mut ref Robot)` and sees nothing but
those four calls, so each counts its position from where it starts,
(0, 0), facing up.

| file | mechanism |
|---|---|
| `robot_room_cleaner.kara` ★ | backtracking: from each new cell, clean, then look in the four directions in turn, turning right each time; step into each new open cell, explore it, and back out (turn around, step, turn around), so the robot faces as it did before. A `Set` of the cells entered |
| `robot_room_cleaner_stack.kara` | the same walk without recursion: a stack of the cells entered and how many directions each has looked at; a cell that has looked all four ways faces its arrival direction again, so popping it backs the robot out |
| `robot_room_cleaner_frontier.kara` | frontier exploration: a map of cells known open and known walls; walk (breadth-first over known open cells) to the nearest open cell with an unknown neighbour, probe each such neighbour (a new open cell is cleaned and stepped back out of), repeat until nothing is unknown |
| `robot_room_cleaner_survey.kara` | survey, then sweep: map the room without cleaning (backtracking, looking left about), then clean the open cells row by row, walking to each by a shortest path over the map |
| `differential.kara` | the four arms on 1,500 random rooms, five properties |

The harness's robot counts every call and stops moving after
`16 × cells² + 1000` of them, far more than any arm needs (the survey
and frontier arms, the hungriest, walk on the order of `cells²` steps,
by how they are built). Without it a search that has lost track of
where it is need never end: before it was added, six of the eight
mutants below overflowed the stack, were killed (exit -9) or hit the
600 s limit, instead of failing a property.

Every arm prints the same 7 lines: the LeetCode example, one cell, a
corridor, a room whose corner is walled off, a spiral, an open room,
and for 300 random rooms (1 to 8 by 1 to 8 cells, a wall in each cell
with odds of 1 in 5, 1 in 3 or 1 in 2 in turn) the cells cleaned and
how many rooms were cleaned right. A room is cleaned right when every
cell reachable from the start (by a flood fill the robot never sees)
was cleaned exactly once and no other cell was. `robot_room_cleaner.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random rooms of 1 to 7 by 1 to 7 cells, at the same three odds.

| | property |
|---|---|
| P1 | every cell reachable from the start is cleaned exactly once, and no other cell |
| P2 | starting facing right, down or left (the arm still counts it as up) cleans the same cells |
| P3 | the room turned a quarter cleans as many cells |
| P4 | the room mirrored left to right cleans as many cells |
| P5 | a wall next to the reachable cells opened never means fewer cells cleaned |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, in 14 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: backing out turns around but not back again | P1 1117, P2 929, P3 751, P4 1029, P5 255 |
| M2 | ★: the direction the arm reckons it faces never changes | P1 1286, P2 1005, P3 786, P4 803, P5 97 |
| M3 | stack: a finished cell is left without stepping back | P1 1121, P2 813, P3 777, P4 833, P5 254 |
| M4 | stack: each cell looks only three ways | P1 1113, P2 864, P3 785, P4 960, P5 195 |
| M5 | frontier: a new cell is not stepped back out of | P1 1286, P2 1053, P3 912, P4 928, P5 185 |
| M6 | frontier: a quarter turn left is made as a turn right | P1 1205, P2 1286, P3 1169, P4 754, P5 38 |
| M7 | survey: each cell looks only three ways | P1 1135, P2 990, P3 764, P4 925, P5 70 |
| M8 | survey: the sweep turns the wrong way round | P1 903, P2 1045 |

Each of these leaves the arm believing it stands somewhere it does not,
or facing a way it does not, and from then on its map and the room
disagree, which every property can see. M8 is the exception: the
survey is right and only the sweep goes astray, and P3 and P4 compare
only how many cells are cleaned, which under M8 agreed in every turned
and mirrored room with the room itself (why was not investigated). One
first draft was equivalent and was replaced: sweeping the surveyed
cells in reverse order rather than row by row, since any order cleans
each cell once.

## Verification

All four arms print the same output as `robot_room_cleaner.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on the ★, stack and frontier arms:
`karac run --interp`, LLJIT, legacy `karac build` and a
`KARAC_AUTO_PAR=1` build print the same output. Legacy `karac build`
warns on them that a value (`room`, or the frontier arm's `open` set)
is "moved here, used again here", where a function lends it twice and
legacy reads the first as a move; the output is right all the same.
The survey arm and the differential do not type-check on legacy, which
reads the items of `open.iter()` as `(i64, i64)` and refuses `*cell`.
The bench program does not build on legacy (see Benchmarks). Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 300 rooms of 100 by 100
cells (a wall in each cell with odds of 1 in 4, the start on an open
cell) once, then cleans each once. Every implementation prints `300
rooms of 100 by 100: 2192124 cells cleaned, checksum 796337731`, the
Kāra program under `karac __mir-run` included (in 56 s). The checksum
takes in each robot's count of calls, so the mirrors make the same
calls in the same order.

Every mirror copies the room into its robot and keeps the visited cells
in a hash set of coordinate pairs: Rust `HashSet<(i64, i64)>`, Go a
`map[[2]int64]bool`, Python a `set` of tuples, and in C an
open-addressing table written out by hand, since C has none. The search
recurses once per cell, up to 10,000 deep, so the Rust and Python
mirrors run it on a thread with a larger stack. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.32 to 0.36 s |
| Rust (`rustc -O`) | 0.56 to 0.75 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.52 to 0.68 s |
| Go | 0.73 to 0.76 s |
| Python | 7.3 s |
| Kāra (`karac build --mir`) | 0.58 to 0.79 s |

The legacy `karac build` refuses this program: "cannot move out of an
index expression", on `make_robot(rooms[k], row, col, 0)`, which v2
reads as a borrow. So `bench.sh` builds the Kāra program with
`karac build --mir`, the v2 compiled backend. That edit is by hand, on
top of the `scripts/new-bench.sh` output. The `--mir` row is timed at
kara `d9a7136c58`. Under `karac __mir-llvm-run` the program prints the
same line in 6.0 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends.
