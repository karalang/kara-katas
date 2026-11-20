# 1210. Minimum Moves to Reach Target with Rotations

In an `n*n` grid, there is a snake that spans 2 cells and starts moving
from the top left corner at `(0, 0)` and `(0, 1)`. The grid has empty
cells represented by zeros and blocked cells represented by ones. The
snake wants to reach the lower right corner at `(n-1, n-2)` and `(n-1,
n-1)`.

In one move the snake can:

- Move one cell to the right if there are no blocked cells there. This
  move keeps the horizontal/vertical position of the snake as it is.
- Move down one cell if there are no blocked cells there. This move keeps
  the horizontal/vertical position of the snake as it is.
- Rotate clockwise if it's in a horizontal position and the two cells
  under it are both empty. In that case the snake moves from `(r, c)` and
  `(r, c+1)` to `(r, c)` and `(r+1, c)`.
- Rotate counterclockwise if it's in a vertical position and the two
  cells to its right are both empty. In that case the snake moves from
  `(r, c)` and `(r+1, c)` to `(r, c)` and `(r, c+1)`.

Return the minimum number of moves to reach the target. If there is no
way to reach the target, return `-1`.

```
grid = [[0,0,0,0,0,1],
        [1,1,0,0,1,0],
        [0,0,0,0,1,1],
        [0,0,1,0,1,0],
        [0,1,1,0,0,0],
        [0,1,1,0,0,0]]    ->  11
grid = [[0,0,1,1,1,1],
        [0,0,0,0,1,1],
        [1,1,0,0,0,1],
        [1,1,1,0,0,1],
        [1,1,1,0,0,1],
        [1,1,1,0,0,0]]    ->  9
```

**Constraints:** `2 <= n <= 100`; `0 <= grid[i][j] <= 1`; it is
guaranteed that the snake starts at empty cells.

The arms are `fn minimum_moves(grid: Vec[Vec[i64]]) -> i64`. The two
Rust arms keep the method LeetCode gives Rust users, on `Vec<Vec<i32>>`,
inside `impl Solution`, and a short `minimum_moves` narrows the grid and
calls it.

## Approaches

The snake is its tail cell and whether it lies flat or upright, `2n²`
states. A move right or down takes the tail one column or one row on and
a turn leaves it where it is, so every route has `2n - 3` moves plus one
for each turn.

| file | mechanism |
|---|---|
| `minimum_moves_to_reach_target_with_rotations.kara` ★ | a breadth-first search over the states, a `Vec` and a head index for the queue and each state's distance in a flat array of `n * n * 2`. O(n²) |
| `minimum_moves_to_reach_target_with_rotations_levels.kara` | the search a level at a time: each level the states one move further, every state seen kept in a `Set[(i64, i64, bool)]`, and the levels counted until one holds the target |
| `minimum_moves_to_reach_target_with_rotations_sweep.kara` | no search: the cells in row-major order are a topological order of the states but for the two at one cell, which a turn joins both ways, so each cell's flat and upright distances come from the cell above and the cell to the left, and then each is offered the other's plus one when the 2 by 2 square there is free. O(n²) |
| `minimum_moves_to_reach_target_with_rotations_astar.kara` | A* over a `PriorityQueue`, ordered by moves so far plus the rows and columns left to the target's tail and one more when upright, a bound no move lowers by more than its cost; a state is settled when first taken. O(n² log n) |
| `minimum_moves_to_reach_target_with_rotations_deque.kara` | a Rust solution as LeetCode's Rust users write it (a `VecDeque<(usize, usize, bool, i32)>` drained by `while let Some((r, c, vertical, d)) = q.pop_front()`, the states seen in a `HashSet<(usize, usize, bool)>` through `seen.insert(s)`, and a closure `free` over `usize` cells), carried to Kāra by `karac fix` |
| `minimum_moves_to_reach_target_with_rotations_dist.kara` | another Rust solution (the distances in `vec![vec![[-1i32; 2]; n]; n]`, a fully qualified `std::collections::VecDeque::new()`, `usize` states with each bound tested as `c + 2 < n` before the index, and the answer read from the distances once the queue runs dry), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 15 lines: LeetCode's two examples; the empty 2
by 2 grid (`1`) and one with a cell under the start blocked (`-1`); the
empty 3 by 3 grid (`3`); three small grids, one needing a turn (`5`) and
one whose middle cell leaves no 2 by 2 square to turn in (`-1`); two
staircases of corridors, steps the snake runs flat along and drops down
upright, with a square to turn in at each corner (`9`, `17`); 1000 random
grids of 2 to 7 cells a side (`1000 small grids: 750 reached, 4368 moves
in all, checksum 459122407`); and four at the constraints' top, 100 by
100: empty (`197`), a tenth of the cells blocked (`197`), a fifth (`-1`),
and a staircase with steps 4 long (`243`, 46 turns).
`minimum_moves_to_reach_target_with_rotations.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, levels, sweep and astar arms check clean as
written. The deque arm takes one round of 25 fixes (among them the `use`
line dropped, `HashSet<(usize, usize, bool)>` to `Set[(i64, i64, bool)]`
and `VecDeque<..>` to `VecDeque[..]`, the closure's `|r: usize, c:
usize|` to `|r: i64, c: i64|`, `!vertical` to `not vertical`, and `&&`
to `and`), and the dist arm one round of 23 (among them `vec![vec![[-1i32;
2]; n]; n]` to `Vec.filled(n, Vec.filled(n, [-1i32; 2]))`,
`std::collections::VecDeque::new()` to `VecDeque.new()`, `(0usize, 0usize,
0usize)` to `(0, 0, 0)` and `Vec<(usize, usize, usize)>` to `Vec[(i64,
i64, i64)]`). Both outputs match.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the snake as its two cells, each move as the statement words
it, and a breadth-first search keeping every pair of cells reached in a
list. 2000 random cases: 2 to 6 cells a side with up to two in five
blocked, the snake's start cells free and the target's not always; the
target is reached in 1045 of them, and in 30 only through a turn.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | unreached, or at least `2n - 3` moves |
| P3 | a blocked cell cleared gives an answer no longer |
| P4 | a free cell blocked gives an answer no shorter |
| P5 | a target cell blocked gives -1 |
| P6 | a free row and column added: reached again, in at most 2 more moves |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 329604182,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, the same search over pairs of cells, gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: an upright snake never turned flat | P1 30, P7 150 |
| S2 | ★: a flat snake moved right when its head's own cell is free | P1 134, P5 365, P7 670 |
| L1 | levels: a turn's far corner never checked | P1 382, P5 957, P7 382 |
| L2 | levels: the target looked for upright | P1 1045, P7 1045 |
| W1 | sweep: a flat snake never moved down | P1 1045, P7 1045 |
| W2 | sweep: a turn from flat to upright only | P1 30, P7 30 |
| A1 | astar: the bound doubled | P6 2 |
| A2 | astar: the queue largest first | P1 702, P3 3, P4 31, P6 323, P7 702 |
| X1 | deque: a flat snake never turned | P1 30, P7 30 |
| X2 | deque: a new state queued at the front | P1 705, P3 10, P4 86, P6 638, P7 705 |
| D1 | dist: a flat snake moved right into a blocked cell | P1 245, P5 711, P7 245 |
| D2 | dist: the answer read upright | P1 1045, P7 1045 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. The counts below are from a Python reading of the cases. S1,
W2 and X1 lose a turn, one way or both, and fail the 30 cases whose
every route turns. L2 looks for the target upright, where it never is,
and W1 never moves a flat snake down, so neither reaches the last row,
and both fail the 1045 cases that are reached; so does D2, which reads
the answer from the upright distances. S2 and D1 let a flat
snake move right into a blocked cell, and L1 drops the far corner of
the 2 by 2 square from its test, so a turn, a flat snake's move down
and an upright one's move right all ignore that cell; each fails P5
more often than P1, since a blocked target cell is one more cell to
walk into. A2 takes the A* queue largest
first and X2 puts each new state at the front of the queue, so both
settle states by a longer route than the shortest, and P3, P4 and P6
catch some of those as well. A1 doubles the A* bound, which then
overestimates, and on these small grids it misleads the search just
twice, both on a grid grown by a row and a column (P6).

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a breadth-first search over the snake's states, its tail cell and
whether it lies flat or upright) on 24 grids of 100 by 100, the
constraints' most, drawn once: eight with a twentieth of the cells
blocked, eight with a tenth, four with a seventh, and staircases of
corridors with steps 3 to 6 long; then 40 rounds over the grids, every
answer folded into a checksum. Every program prints `40 rounds over 24
grids of 100 by 100: checksum 294628831`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.382 to 0.465 s | 0.415 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.399 to 0.552 s | 0.430 s |
| Rust (`rustc -O`) | 0.411 to 0.523 s | 0.461 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.415 to 0.668 s | 0.455 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.453 to 0.710 s | 0.493 s |
| C (`clang -O3`) | 0.167 to 0.223 s | 0.184 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.170 to 0.220 s | 0.182 s |
| Go | 0.663 to 0.846 s | 0.766 s |
| Python | 11.85 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` gives a different binary
here, with a loop its cost gate accepts compiled to run in parallel; its
median is 0.415 s, and its user time, 0.420 s, shows little of it
running on a second core. Kāra is about 5% ahead of Rust with overflow
checks on (0.430 s against 0.455 s), and the two ranges overlap. Kāra
takes about 2.3x C's time (0.430 s against 0.184 s); Go takes about 1.8x
Kāra's time. Python takes about 28x Kāra's time. No profile was taken.
