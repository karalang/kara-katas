# 2258. Escape the Spreading Fire

You are given a **0-indexed** 2D integer array `grid` of size `m x n`
which represents a field. Each cell has one of three values:

- `0` represents grass,
- `1` represents fire,
- `2` represents a wall that you and fire cannot pass through.

You are situated in the top-left cell, `(0, 0)`, and you want to travel
to the safehouse at the bottom-right cell, `(m - 1, n - 1)`. Every
minute, you may move to an **adjacent** grass cell. **After** your
move, every fire cell will spread to all **adjacent** cells that are
not walls.

Return *the **maximum** number of minutes that you can stay in your
initial position before moving while still safely reaching the
safehouse*. If this is impossible, return `-1`. If you can **always**
reach the safehouse regardless of the minutes stayed, return `10^9`.

Note that even if the fire spreads to the safehouse immediately after
you have reached it, it will be counted as safely reaching the
safehouse.

```
grid = [[0,2,0,0,0,0,0],[0,0,0,2,2,1,0],[0,2,0,0,1,2,0],[0,0,2,2,2,0,2],[0,0,0,0,0,0,0]]  ->  3
grid = [[0,0,0,0],[0,1,2,0],[0,2,0,0]]                                                    ->  -1
grid = [[0,0,0],[2,2,0],[1,2,0]]                                                          ->  1000000000
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`2 <= m, n <= 300`; `4 <= m * n <= 2 * 10^4`; `grid[i][j]` is `0`, `1`
or `2`; `grid[0][0] == grid[m - 1][n - 1] == 0`.

The fire's minute at every cell is one breadth-first search from all
the fires at once. A wait then either escapes or not, and a wait that
fails fails for every longer one, so the answer is the last wait that
escapes. The person may step onto a cell only while the fire is still
a minute away, since the fire spreads after the move, but onto the
safehouse in the very minute the fire arrives. A wait of `m * n` that
still escapes means the fire never cuts the way: by then it has
reached every cell it ever will.

## Approaches

| file | mechanism |
|---|---|
| `escape.kara` ★ | fire minutes in a `Vec.filled` grid by a `VecDeque` search from every fire over `const STEPS: Array[(i64, i64), 4]`; `escapes(grid, fire, wait)` a breadth-first search of the person, strict before the fire and `<=` at the safehouse; a binary search over the wait between 0 and `m * n` |
| `escape_formula.kara` | no search over the wait: a second breadth-first search for the person with no fire, and `slack` the fire's lead over the person at the safehouse; the answer `slack`, or `slack - 1` unless a closure `roomy` finds the cell above or left of the safehouse with more than `slack` to spare. O(mn) |
| `escape_struct.kara` | `enum Cell { Grass, Fire, Wall }` in a flat `Vec` of a `struct Field`; `neighbours`, `burn` and `escapes` take `ref self`; the binary search keeps `lo` escaping and narrows `hi` to `mid - 1` |
| `escape_iter.kara` | frontiers, not a queue: each next frontier the `flat_map` of `around` over the last, `filter`ed to grass not yet reached; the waits counted by `(1..m * n).take_while(..).count()`, no bisection |
| `escape_latest.kara` | backwards from the safehouse: the latest minute a person may stand on each cell and still get home, a widest path settled by a Dijkstra with `PriorityQueue.max_first()`; the start's latest minute is the answer |
| `escape_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` in, `i32` out, a `vec!` grid of fire minutes from `i32::MAX`, a closure `check(wait)` for the person, every neighbour through `as i32` and `as usize` casts, and the same binary search; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (fire beside the start; fire held back by a wall, answer 2; fire
that runs along the far side to the safehouse first; fire that comes
from behind and leaves no wait), each with its answer; then the count of trapped,
waiting and never-reached answers over 5000 grids of 2 to 11 by 2 to
11 with a wall in about 4 cells and one fire, with a checksum; then
three grids of the constraints' most cells, 2 * 10^4: 100 by 200 with
the fire behind a wall down the second column that opens beside the
start, so that it chases the person (98); 2 by 10^4 with the fire
under the start (0); and 300 by 66 as a winding corridor with the fire
sealed in a pocket (10^9). `escape.py` mirrors the ★ arm and its
output is byte-identical.

`karac fix` carries the template in one round of 39 edits: the `use
std::collections::VecDeque;` line deleted, `VecDeque` being in the
prelude; `Vec<Vec<i32>>` to `Vec[Vec[i32]]`, `[(i32, i32); 4]` to
`Array[(i32, i32), 4]`, both `vec![vec![..; n]; m]` to
`Vec.filled(m, Vec.filled(n, ..))`, `::` to `.` in `i32::MAX` and
`VecDeque::new()`, the `&` dropped from `for &(di, dj)`, `||` and `&&`
to `or` and `and`, `!` to `not`, the casts `as usize` to `as i64` and
the `0usize` suffixes dropped, the closure's `-> bool` removed, `let
(mut lo, mut hi)` to `let mut (lo, hi)` with the `0` typed `0i32`,
`struct Solution;` to `struct Solution {}`, and the adapter's `as i64`
on the `i32` answer dropped, since `i32` widens to `i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every wait from 0 to `m * n` the minutes are played out
on two grids of flags, the fire's cells and the cells the person may
be on. Each minute the person moves or stays onto grass the fire has
not reached, and is home if the safehouse is among them; then the fire
spreads and every person's cell it reaches is lost. No fire minutes,
no search. It checks 210 random grids of 2 to 6 by 2 to 6, a wall in
about 1 cell in 5, 3 or 2.5, and one fire; 30 of 7 to 9 by 4 to 9
where the fire winds through walled rows on the right while the person
comes down the left and along the bottom, the two ways meeting only
at the safehouse; 30 strips of 2 by up to 12 or up to 12 by 2 with one
or two fires; 30 of 3 to 6 by 3 to 7 where a wall down the second
column keeps the fire in the first until it comes round behind the
person; and 60 of 2 to 6 by 2 to 6 with the fire walled in on every
side but a corner. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the grid transposed: the same answer |
| P3 | a fire put on the first grass cell after the start, if it is not the safehouse: no later an answer (-1 below any wait, 10^9 above) |
| P4 | every fire made grass: -1 or 10^9, and 10^9 if the answer was not -1 |
| P5 | every fire made a wall: -1 or 10^9, 10^9 if the answer was not -1, and never above P4's |
| P6 | each arm agrees with at least three of the other five |

The second family is there because the best wait almost never meets
the fire at the safehouse by chance: in 394 random 3 to 6 by 3 to 6
grids with a wait, it happened twice. In that family it is every case,
so an arm that refuses the safehouse in the fire's own minute, or the
formula arm's `slack` always taken one less, fails P1 there.

The differential prints `360 cases (278 trapped, 67 with a wait, 15
never reached): checksum 942761422, 12960 checks over 6 arms: 0
failures` under every lane in Verification; the checksum of the literal
answers was checked against a Python reading that finds the fire's
minutes by relaxing every cell until nothing changes and tries every
wait by a depth-first search over (cell, minute). On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the safehouse needing the person first too | P1 28, P6 28 |
| M4 | ★: every wait taken for 10^9 | P1 67, P6 67 |
| M6 | ★: no step upward | P1 35, P2 76, P6 35 |
| M7 | formula: the slack never trimmed | P1 43, P6 43 |
| M10 | formula: only the cell above looked at | P1 28, P2 28, P6 28 |
| M11 | formula: a negative slack let through | P1 12, P3 12, P6 12 |
| M12 | struct: the last column joined to the next row | P1 33, P2 51, P6 33 |
| M14 | struct: a fire seen as grass | P1 244, P5 61, P6 244 |
| M15 | struct: the person setting off at minute 0 | P1 29, P6 29 |
| M19 | iter: the person stepping through fire | P1 5, P6 5 |
| M20 | iter: walls burning | P1 82, P6 82 |
| M21 | iter: home reached after the fire | P1 40, P6 40 |
| M23 | latest: no minute lost per step | P1 145, P6 145 |
| M25 | latest: the heap popping the smallest | P2 1 |
| M26 | latest: walls walked through backwards | P1 59, P6 59 |
| M28 | solution: the fire spreading one row only | P1 149, P2 66, P6 149 |
| M29 | solution: no 10^9 answer | P1 15, P4 259, P5 198, P6 15 |

P1 kills sixteen and P6 sixteen, P2 five, P5 two, and P3 and P4 one
each. Most edits change only the answer, so only the literal reading
and the other arms see them. P2 catches the edits that treat one
direction apart from the others: no step upward, only the cell above
the safehouse looked at, the last column joined to the next row, the
fire spreading along one row. P3 catches the formula arm letting a
negative slack through (M11), since one more fire can then raise the
answer. P4 and P5 catch the template's lost 10^9 (M29) and the struct
arm's fire seen as grass (M14), where a grid with no fire must answer
10^9 if any way leads home. The latest arm's min-first heap (M25) is
caught by P2 alone: it settles a cell before its best offer arrives,
which these grids show only once, transposed.

Of the thirty-one, fourteen were not kept, and none crashes, hangs or
differs between the backends. Every one fails as a kept one does: the
★ arm's cell entered with the fire (M2) as the iter arm's person
stepping through fire (M19); the ★ arm's fire through walls (M3) and
the struct arm's lost neighbour below (M16) as the iter arm's walls
burning (M20); the ★ and template arms' bisection returning the failing
end, the iter arm's fire minutes from 0 and one wait too many counted
(M5, M31, M17, M18) as the ★ arm's every wait taken for 10^9 (M4); the
formula arm's slack always trimmed, the struct arm's safehouse refused
at the fire's minute and the latest arm's safehouse minute one less
(M8, M13, M22) as the ★ arm's safehouse needing the person first (M1);
the formula arm's roomy at an equal lead and the latest arm's cell
entered with the fire (M9, M24) as its slack never trimmed (M7); the
template's person through walls (M27) as the latest arm's walls walked
backwards (M26); and the template's fires lit at minute 1 (M30) fails
in a way of its own, left out because its arm keeps two.

Seven edits of the first draft were replaced. Five were equivalent:
the ★ and template arms' wait allowed to meet the fire at the start
(once the fire stands on the start, every cell beside it burns the next
minute, and the safehouse is never beside the start), the ★ arm's
search capped one below `m * n`, the struct arm's bisection mid rounded
the other way, and the latest arm's 10^9 test at `m * n - 1`. One
looped forever (the struct arm's `hi = mid` under a mid that rounds
up), and one panicked out of bounds (the iter arm's rows wrapped at the
edge). The first run also showed that the best wait almost never meets
the fire at the safehouse in random grids: the ★ arm's `<=` made `<`
and the formula arm's slack always trimmed both survived, which is why
the differential has the family where the two ways meet only at the
safehouse.


## Verification

Every arm prints the same output as `escape.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the formula arm takes 2.0 s, the struct arm
2.2 s, the ★ arm 2.4 s, the latest arm 3.1 s, the template 5.3 s, the
differential 15 s, and the iter arm 72 s. The iter arm's time is the
100 by 200 chase: its waits are counted one at a time, 99 searches of
2 * 10^4 cells, each frontier a fresh chain of `flat_map`, `filter`
and `collect` that calls `around` for every cell, which builds a `Vec`
of up to four neighbours through `iter`, `filter`, `map` and
`collect`; compiled it takes 0.7 s.


## Benchmarks

The bench answers 300 grids of 2 * 10^4 cells, as 100 by 200, 200 by
100 and 125 by 160 in turn, each with a wall down the second column
below the first row, a wall in about 8 cells in 100 past it, and the
fire on a random row of the first column, so it comes round through
the gap at the top behind the person and the binary search runs its
full course, with the ★ arm in all five languages. Every
implementation prints `300 grids of 2 * 10^4 cells: 297 with a wait,
checksum 468121131`. The C mirror keeps the grid in one flat array
and reuses the queue between waits; the others allocate per search.

BENCHTAB
