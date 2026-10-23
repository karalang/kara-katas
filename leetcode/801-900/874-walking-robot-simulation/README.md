# 874. Walking Robot Simulation

A robot on an infinite XY-plane starts at point `(0, 0)` facing north.
The robot receives an array of integers `commands`, which represents a
sequence of moves that it needs to execute. There are only three
possible types of instructions the robot can receive:

- `-2`: Turn left 90 degrees.
- `-1`: Turn right 90 degrees.
- `1 <= k <= 9`: Move forward `k` units, one unit at a time.

Some of the grid squares are `obstacles`. The `i`-th obstacle is at grid
point `obstacles[i] = (xi, yi)`. If the robot runs into an obstacle, it
will stay in its current location (on the block adjacent to the
obstacle) and move onto the next command. Return the maximum squared
Euclidean distance that the robot reaches at any point in its path. If
there is an obstacle at `(0, 0)`, the robot ignores it until it has
moved off the origin, but it will be unable to return to `(0, 0)`.

```
commands = [4,-1,3],         obstacles = []        ->  25
commands = [4,-1,4,-2,4],    obstacles = [[2,4]]   ->  65
commands = [6,-1,-1,6],      obstacles = [[0,0]]   ->  36
```

**Constraints:** `1 <= commands.length <= 10^4`, `commands[i]` is -2, -1
or in `[1, 9]`, `0 <= obstacles.length <= 10^4`, `-3 * 10^4 <= xi, yi <=
3 * 10^4`, and the answer is less than `2^31`.

## Approaches

| file | mechanism |
|---|---|
| `robot_sim.kara` ★ | the robot walked one square at a time against a set of obstacles: each obstacle goes into a `Set` as one number, and the direction is an index into the four steps north, east, south and west, a right turn the next index and a left turn the one before. A move of k is k single steps, stopping before the first obstacle, with the squared distance taken after every step. O(c + s) for c commands and s steps |
| `robot_sim_pairs.kara` | the direction a vector turned by rotation: a `Set` of `(x, y)` pairs, and the step `(dx, dy)` itself turned a quarter turn left to `(-dy, dx)` or right to `(dy, -dx)` |
| `robot_sim_facing.kara` | the direction as an enum: `Facing` is `North`, `East`, `South` or `West`, and `left`, `right` and `step` match on it |
| `robot_sim_jump.kara` | each move in one jump, by binary search: the obstacles grouped by column and by row in sorted `Vec`s, and the first obstacle in the robot's way found by a binary search of its line. The distance along a straight move is largest at one of its ends, so only the end of each move is measured. O((c + n) log n) for n obstacles |
| `robot_sim_range.kara` | each move in one jump, by a range query: a `SortedSet` of obstacles per column and per row, and the first obstacle in the stretch the move covers taken from `range` (`next` going up, `last` going down) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples and seven
more (turns and no move; an obstacle straight ahead; a walk west then
south, stopped one square short; a turn round to face south, stopped by
an obstacle, then a walk west; a square walked back to the origin and a
move north stopped below an obstacle; obstacles at LeetCode's extremes,
3 x 10^4; and an obstacle at the origin that the robot leaves and then
cannot return to); the distances of 3,000 random walks of 1 to 10
commands among up to 11 obstacles within 5 squares of the origin,
879,923 in all, with 220 walks that never leave the origin; and 12
walks of 10^4 commands among 10^4 obstacles, LeetCode's largest, the
obstacles crowded within 150 to 650 squares of the origin or spread to 3
x 10^4, with a checksum. `robot_sim.py` mirrors the ★ arm and its output
is byte-identical.

`robot_sim_jump.kara` looks up a line that may have no obstacles as
`columns.get(x).unwrap_or(empty)`, `empty` an empty `Vec` declared before
the command loop. `karac check` (and so `karac run`) refuses it, saying
`empty` is moved inside the loop, while the MIR backends run it and
leave `empty` usable; the same default written `?? empty` passes `karac
check` and is refused by the MIR move check instead. This is kara
`B-2026-10-23-2`. The arm and the differential, which holds a copy of
it, are left as written.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the robot turned 90 degrees left or right, or moved k steps
of one unit, each step checked against the obstacles as listed, and the
squared distance taken at every point it reaches. It checks 1,700 walks:
1,500 of 1 to 10 commands among up to 12 obstacles within 3 or 4 squares
of the origin (the origin sometimes one of them) against the statement,
and 200 of up to 300 commands among up to 300 obstacles within 10 to 49
squares against the other properties. The ★ arm's distances sum to
3,518,695.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | four turns the same way, inserted anywhere, change nothing |
| P3 | the obstacles turned a quarter turn clockwise about the origin, and a right turn put first, give the same answer |
| P4 | the obstacles mirrored left to right, and every left turn swapped with a right turn, give the same answer |
| P5 | every move of more than 1 split into two moves gives the same answer |
| P6 | every obstacle listed twice, and obstacles added beyond the robot's reach, change nothing |

It prints `1700 walks, distances sum to 3518695, 50000 checks over 5
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a left turn taken as a right turn | P1 324, P4 402 |
| M2 | ★: the square the robot is on checked instead of the next | P1 467 |
| M3 | ★: south taken as north | P1 165, P3 491 |
| M4 | pairs: a left turn rotated the wrong way | P1 324, P4 402 |
| M5 | pairs: y stepped by dx | P1 1326, P3 1510, P4 400 |
| M6 | pairs: the next square checked with the axes swapped | P1 685, P3 905, P4 905 |
| M7 | facing: a left turn from west taken to north | P1 117, P2 91, P3 313, P4 411 |
| M8 | facing: a step south taken north | P1 165, P3 491 |
| M9 | facing: the distance measured as x^2 + xy | P1 1140, P3 1554, P4 796 |
| M10 | jump: an obstacle on the robot's own square stops it | P1 95, P3 37, P4 37, P5 11 |
| M11 | jump: the robot stops on the obstacle ahead | P1 340, P3 240, P4 240, P5 351 |
| M12 | jump: an obstacle at the end of a move down a line missed | P1 22, P3 111, P4 111, P5 148 |
| M13 | range: an obstacle at the end of a move north missed | P1 74, P3 174, P5 259 |
| M14 | range: moving south, the farthest obstacle in the way taken | P1 2, P3 65, P5 12 |
| M15 | range: moving east, the row looked up by x | P1 97, P3 579, P4 342, P5 188 |

P1 kills all fifteen. M1 and M4 are one fault in two arms, a left turn
going right, and fail the same walks; so are M3 and M8, a step south
going north. M2 never looks at the square ahead, so the robot walks
through every obstacle (and cannot leave an obstacle at the origin). The
robot only ever stands on an obstacle at the origin, so M10 goes wrong
only on walks where the origin is one. P6 kills none: each arm stores the obstacles in a set or a
sorted line, which a repeat leaves unchanged, and no mutation here
reaches a square out of the robot's reach.

## Verification

Every arm prints the same output as `robot_sim.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes the
★, pairs, facing and range arms and the bench program, and `karac run`
and a `karac build --mir` binary print the same output for those four
arms. `karac check` refuses the jump arm and the differential, and with
it `karac run` and `karac build --mir` (above, `B-2026-10-23-2`). The
release build is at kara `e3f5faf572` and the runtime archives at
`e903d5b111`, with no runtime change between them. Under `karac
__mir-run` the arms take 2 to 4 s each and the differential 17 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends refuse the ★, pairs and facing arms, the
differential and the bench program at a `*` on a `for` element, saying
the value is not a reference, where v2 yields a reference, and the jump
and range arms at `Map.get_mut`, which legacy does not have. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 20 lists of
10^4 commands and 20 lists of 10^4 obstacles, LeetCode's largest, the
obstacles crowded within 100 to 290 squares of the origin, built once;
then 600 walks, each pairing a command list with an obstacle list and
building its set of obstacles afresh, as LeetCode's function does,
summing the distances and a checksum. The set is a `Set` in Kāra, a
`HashSet` in Rust (both SipHash-1-3), a `map` in Go, a `set` in Python,
and in C, which has no hash set, an open-addressing table with a
multiplicative hash, cleared for each walk. Every implementation prints
`600 walks of 10000 commands among 10000 obstacles: distances sum to
653977757, checksum 353699406`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.25 to 0.32 s | 0.28 s |
| Rust (`rustc -O`) | 0.60 to 0.79 s | 0.62 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.64 to 0.83 s | 0.70 s |
| Go | 0.90 to 1.08 s | 0.98 s |
| Python | 9.5 s | |
| Kāra (`karac build --mir`) | 0.74 to 0.95 s | 0.82 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 873's does. Legacy refuses the bench program
(above), so it has no lane here.

v2 takes 1.2 times Rust's median time under overflow checks and 2.9
times C's. Under valgrind's cachegrind C runs 0.74 billion instructions,
Rust with overflow checks 4.29 billion and v2 5.21 billion. Under
callgrind 69% of v2's are in the set's runtime calls: 2.02 billion in
`karac_hash_word`, 0.99 billion in `karac_mir_map_find_hv` and 0.58
billion in `karac_mir_map_insert_hv`. Rust inlines its hashing and
lookups into `main` (76% of its instructions) and spends another 22% in
the table's rehashing as the set grows. C's cheap hash, and a table
sized once for all walks, account for its lead. The comparison with C
and Rust waits until after M4.
