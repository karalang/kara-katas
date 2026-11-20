# 1263. Minimum Moves to Move a Box to Their Target Location

A storekeeper is a game in which the player pushes boxes around in a
warehouse trying to get them to target locations.

The game is represented by an `m x n` grid of characters `grid` where
each element is a wall, floor, or box. Your task is to move the box
`'B'` to the target position `'T'` under the following rules:

- The character `'S'` represents the player. The player can move up,
  down, left, right in `grid` if it is a floor (empty cell).
- The character `'.'` represents the floor which means a free cell to
  walk.
- The character `'#'` represents the wall which means an obstacle
  (impossible to walk there).
- There is only one box `'B'` and one target cell `'T'` in the `grid`.
- The box can be moved to an adjacent free cell by standing next to the
  box and then moving in the direction of the box. This is a **push**.
- The player cannot walk through the box.

Return *the minimum number of **pushes** to move the box to the
target*. If there is no way to reach the target, return `-1`.

```
######
#T####
#..B.#      ->  3
#.##.#
#...S#
######

######
#T####
#..B.#      ->  -1
####.#
#...S#
######

######
#T..##
#.#B.#      ->  5
#....#
#...S#
######
```

**Constraints:** `1 <= m, n <= 20`; `grid` contains only `'.'`, `'#'`,
`'S'`, `'T'` and `'B'`; there is only one each of `'S'`, `'B'` and `'T'`.

The arms are `fn min_push_box(grid: Vec[Vec[char]]) -> i64`.

## Approaches

A position is the box's cell and the player's: at most 400 by 400 of
them. A step of the player costs nothing and a push costs one, so the
answer is a shortest path in a graph whose edges weigh 0 or 1.

| file | mechanism |
|---|---|
| `min_push_box.kara` ★ | a 0-1 BFS over (box, player) states in a `VecDeque`: a step to the front, a push to the back, and a state final the first time it leaves, kept in a flat `Vec[bool]` |
| `min_push_box_pushes.kara` | push by push: a level BFS over (box, player behind it) states in a `Set` of nested tuples, each push allowed when a second BFS finds the player can walk behind the box with the box as a wall |
| `min_push_box_astar.kara` | A*: states popped from a `PriorityQueue` by pushes so far plus the box's Manhattan distance to the target, the best pushes per state in a `Map`, the cells found by a closure that `return`s from inside its loops |
| `min_push_box_layers.kara` | layer by layer: the states reached with `k` pushes flooded by steps alone, every push out of the flood starting layer `k + 1`, the grid flattened by `flat_map` and its cells found by `position` |
| `min_push_box_solution.kara` | a Rust solution as LeetCode's Rust users write it (`(mut sx, mut sy, ..)`, `vec![vec![i32::MAX; m * n]; m * n]`, `as usize` casts, a relaxing 0-1 BFS), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples; 1000
random grids of 3 to 10 by 3 to 10, a cell in 8 a wall, the player, the
box and the target on three different cells (`1000 random grids: 1557
pushes, 591 stuck, checksum 950900614`, most of the stuck ones a box
against a wall); and the constraints' top, a 20 by 20 open floor with the
box a cell in from one corner and the target a cell in from the other, and two 20 by 20 grids a
cell in 10 a wall. `min_push_box.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★ and push-by-push arms checked clean as first
written. The A* and layered arms each declared a closure's return type,
`|want: char| -> Cell` and `|p: i64, d: i64| -> Option[i64]`: Rust
syntax, which check names and `karac fix` drops, the type inferred from
the body. The solution arm takes one round of fixes, 37 by `karac fix`'s
count: the `use std::collections::VecDeque` line removed, `Vec<..>` to
brackets, `let (mut sx, mut sy, ..)` to `let mut (sx, sy, ..)`, `&&` and
`!` to `and` and `not`, the `as usize` casts dropped or made `as i64`,
`vec![vec![i32::MAX; m * n]; m * n]` to `Vec.filled(m * n,
Vec.filled(m * n, i32.MAX))`, `VecDeque::new()` to `VecDeque.new()`, the
`&(dx, dy)` pattern to `(dx, dy)`, and `struct Solution;` and
`Solution::` to Kāra's. All five check clean.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the fewest pushes to every (box, player) state, from the
start's 0, relaxed by every step and every push until nothing changes,
and the answer the least over the states with the box on the target.
2000 random grids of 2 to 5 by 3 to 6, a cell in 6 a wall.

| | property |
|---|---|
| P1 | the statement read literally: the fewest pushes, relaxed to a fixed point |
| P2 | the grid transposed, the same answer |
| P3 | the grid mirrored left to right, the same answer |
| P4 | -1, or at least the box's Manhattan distance to the target |
| P5 | a free cell walled, no fewer pushes (-1 counting as none possible) |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 grids: checksum 719644554,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the
same checksum, by the mirror's BFS.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a step queued at the back, as a push is | P1 6, P2 1, P6 24 |
| S2 | ★: the player's step reads the column the wrong way | P1 453, P2 912, P6 1812 |
| P1 | push by push: the player walks through the box | P1 60, P6 60 |
| P2 | push by push: the player must stand ahead of the box, not behind | P1 1097, P6 1097 |
| A1 | A*: the estimate tripled, so it can overestimate | P1 1, P5 1, P6 1 |
| A2 | A*: ordered by the estimate alone, a greedy best-first search | P1 2, P5 1, P6 2 |
| L1 | layers: a step counted as a push | P1 426, P6 426 |
| L2 | layers: no step or push to the right | P1 390, P2 190, P3 241, P6 390 |
| O1 | solution: a step queued at the back | P1 5, P3 1, P6 5 |
| O2 | solution: left replaced by a second right | P1 327, P2 159, P3 241, P6 327 |

All ten are caught, every one by P1, the statement read literally, and
by P6. Four are caught only a handful of times: S1 and O1, which queue a
free step behind the pushes, and A1 and A2, which order A* wrongly. Each
still finds a way; it is only sometimes not the fewest pushes, which
takes a grid where the cheap way is not the first one met. P4 catches
none: no mutant answers below the box's distance. A first A2 kept the
cost a state was first reached at, never lowering it. It survived these
grids and the arm's own harness, but it is not equivalent: a state first
reached by a push can later be reached by steps alone with one push
fewer. It was replaced.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a 0-1 BFS over (box, player) states in a `VecDeque`, a step to the
front and a push to the back, each state final the first time it leaves)
on 100 random 20 by 20 grids, a cell in 10 a wall, built once, 20
rounds; every answer folded into a checksum. Every program prints `20
rounds of 100 grids of 20 by 20: 20620 pushes, checksum 1334488`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 2.292 to 2.477 s | 2.386 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 2.227 to 2.503 s | 2.374 s |
| Rust (`rustc -O`) | 1.938 to 2.248 s | 2.042 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.163 to 2.336 s | 2.249 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 2.072 to 2.300 s | 2.153 s |
| C (`clang -O3`) | 1.215 to 1.354 s | 1.244 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.210 to 1.409 s | 1.282 s |
| Go | 2.513 to 2.756 s | 2.633 s |
| Python | 120.03 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 5% ahead of Kāra (2.249 s
against 2.374 s), and the two ranges overlap. Kāra takes about 1.9x C's
time (2.374 s against 1.244 s); Kāra is about 10% ahead of Go (2.374 s
against 2.633 s). Python takes about 51x Kāra's time. No profile was
taken.
