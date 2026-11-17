# 2257. Count Unguarded Cells in the Grid

You are given two integers `m` and `n` representing a **0-indexed**
`m x n` grid. You are also given two 2D integer arrays `guards` and
`walls` where `guards[i] = [row_i, col_i]` and `walls[j] = [row_j,
col_j]` represent the positions of the `i`th guard and `j`th wall
respectively.

A guard can see **every** cell in the four cardinal directions (north,
east, south, or west) starting from their position unless
**obstructed** by a wall or another guard. A cell is **guarded** if
there is **at least** one guard that can see it.

Return *the number of unoccupied cells that are **not** guarded.*

```
m = 4, n = 6, guards = [[0,0],[1,1],[2,3]], walls = [[0,1],[2,2],[1,4]]  ->  7
m = 3, n = 3, guards = [[1,1]], walls = [[0,1],[1,0],[2,1],[1,2]]        ->  4
```

**Constraints:** `1 <= m, n <= 10^5`; `2 <= m * n <= 10^5`;
`1 <= guards.length, walls.length <= 5 * 10^4`;
`2 <= guards.length + walls.length <= m * n`; every position is in the
grid and all of them are distinct.

A walk from each guard in each direction marks what it sees and stops
at a guard, a wall or the edge. Stopping at a guard loses nothing: the
cells past it are the ones that guard sees itself in the same
direction. A walk can cross cells already seen, so the walks cost
O(guards * (m + n)); four sweeps of a flag along every row and column
cost O(mn) whatever the guards.

## Approaches

| file | mechanism |
|---|---|
| `unguarded.kara` ★ | a `Vec.filled` grid of marks (0 empty, 1 seen, 2 guard, 3 wall), and from every guard a `while` walk in each of `[(-1, 0), (1, 0), (0, -1), (0, 1)]` marking cells below 2; the empty cells counted by `filter` and `count` per row, summed |
| `unguarded_sweep.kara` | four sweeps and no walk: along every row from the left and from the right, and down every column from the top and from the bottom, a flag a guard raises and a wall lowers marks each empty cell passed while it is up |
| `unguarded_set.kara` | no grid: the guards and walls in a `Set[(i64, i64)]` of blocked cells, the walk's cells in a second set, and the count every cell less the two sets' sizes |
| `unguarded_struct.kara` | `enum Cell { Empty, Seen, Guard, Wall }` in a `struct Grid` of one flat `Vec` and its sizes; `look` (`mut ref self`) walks one direction until `blocks` says a guard or wall is in the way, `inside` and `count` take `ref self` |
| `unguarded_iter.kara` | iterator chains on lines: `seen_along` gives the cells a guard on one row or column sees by a `scan` from each end, the backward one `reverse`d, `zip`ped; columns gathered by `map` over the rows; the cells empty and unseen both ways counted by `filter` over `0..m * n` |
| `unguarded_solution.kara` | LeetCode's Rust template: `i32` sizes and `Vec<Vec<i32>>` in, `i32` out, a `vec!` grid of `u8`, a `const DIRS: [(i32, i32); 4]`, each walk kept going while `(0..m).contains(&r)`, and the free cells counted by `flatten().filter(..).count()`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four
more (a 1 by 1 grid holding the guard; a wall that hides the far end
of a row; two guards that see the whole row between them; a guard
boxed in by walls), each with its count; then the total over 2000
grids of 1 to 6 by 1 to 6 with 1 to 3 guards and up to 4 walls, with a
checksum; then the constraints' most cells, 10^5, as 1 by 10^5, 250 by
400 and 10^5 by 1, each with 2000 guards and 10000 walls.
`unguarded.py` mirrors the ★ arm and its output is byte-identical.

The harness goes below the constraints' least in three ways: the 1 by
1 grid, examples with no wall, and random grids with no wall or of one
cell. The statement reads the same there, and every arm answers it.

`karac fix` carries the template in one round of 25 edits:
`Vec<Vec<i32>>` to `Vec[Vec[i32]]`, `vec![vec![0u8; n as usize]; m as
usize]` to `Vec.filled(m, Vec.filled(n, 0u8))`, `&guards` to `ref
guards`, the `&` dropped from the `for` pattern and from the
`contains` arguments, `let (mut r, mut c)` to `let mut (r, c)`, `&&`
to `and`, `flatten()` to `flat_map(|v| v.iter())` with `|&&x|` made
`|x|`, and `struct Solution;` to `struct Solution {}`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every empty cell, every guard on its row or column is
asked whether all the cells strictly between them are free of guards
and walls; no walk and no marks. It checks 300 random grids of 1 to 6
by 1 to 6 with 1 to 3 guards and up to 4 walls; then 30 of one row or
one column of up to 20 cells; then 30 of 2 to 6 by 2 to 6 with half or
more of their free cells made walls. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the grid transposed: the same count |
| P3 | the grid mirrored left to right: the same count |
| P4 | a wall put on the first unguarded cell, if there is one: the count one less |
| P5 | every wall made a guard: no more than the count |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 549624905, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that floods
each guard's four rays over a set of cells. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no walk upward | P1 143, P2 191, P6 143 |
| M4 | ★: the walk begun on the guard | P1 277, P6 277 |
| M6 | ★: the last row never reached | P1 211, P2 199, P6 211 |
| M7 | sweep: no sweep from the right | P1 147, P2 191, P3 186, P6 147 |
| M8 | sweep: a wall not stopping the downward sweep | P1 27, P2 66, P4 9, P6 27 |
| M9 | sweep: the flag carried from row to row | P1 98, P2 114, P3 58, P4 46, P6 98 |
| M12 | set: the walk begun two cells out | P1 248, P4 33, P6 248 |
| M13 | set: the walls not blocking | P1 149, P4 221, P6 149 |
| M14 | set: the guards counted as unguarded | P1 360, P5 147, P6 360 |
| M18 | struct: no look to the right | P1 153, P2 204, P3 186, P6 153 |
| M19 | struct: column 0 outside | P1 219, P2 210, P3 159, P6 219 |
| M20 | struct: a seen cell made a wall | P1 45, P6 45 |
| M22 | iter: seen only from both ends | P1 276, P6 276 |
| M23 | iter: the backward sweep not turned round | P1 197, P3 170, P4 18, P6 197 |
| M25 | iter: each column read bottom up | P1 139, P2 171, P4 15, P6 139 |
| M30 | solution: the rows walked two at a time | P1 134, P2 179, P4 5, P6 134 |
| M31 | solution: every cell not seen counted | P1 360, P4 221, P6 360 |

P1 and P6 kill all seventeen, P2 nine, P4 eight, P3 five, and P5 one.
P2 and P3 catch the edits that treat one direction or one edge apart
from the others: a transposed or mirrored grid moves the cells they
miss. P4 catches the edits that count a wall or a cell that is not
empty, since a new wall then changes the count by other than one. P5
fails only the edit that counts the guards themselves (M14): more
guards can only see more, so the count cannot grow.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Two survive and are equivalent, for the reason
given at the top: the ★ arm's walk going on past a guard
(M2) and the struct arm's guards not blocking (M17) see only what the
guard passed sees itself. Six fail as a kept one does: the walls
counted in the sweep, set and struct arms (M10, M15, M21) as the
template's every-cell-not-seen (M31); the ★ arm's seen cells counted
(M5) as its walk begun on the guard (M4); the sweep arm's guard
lowering the upward flag (M11) as the ★ arm's walk never going up
(M1); and the template's never looking right (M29) as the struct
arm's (M18). Three fail alike as a group: the ★ arm's walk through
walls, the iter arm's walls not lowering the flag, and the template's
walls and guards marked seen (M3, M24, M27). The other three fail in
ways of their own and are left out because their arms keep enough: the
set arm's walk one column past the edge (M16), the iter arm's columns
ignored (M26), and the template's last column outside (M28). One more
edit, the set arm's walk drifting by its row step, looped forever and
was replaced by M15.

## Verification

Every arm prints the same output as `unguarded.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the set and struct arms take 0.6 s, the ★ arm
0.8 s, the sweep arm 1.2 s, the template 1.3 s, the iter arm 8.1 s,
and the differential 1.4 s. The iter arm's time is the 10^5 by 1
grid: 10^5 one-cell rows, each through two `scan`s, a `zip` and three
`collect`s.

## Benchmarks

The bench answers 300 grids of 10^5 cells, as 1 by 10^5, 250 by 400
and 10^5 by 1 in turn, each with 2000 guards and 10000 walls, with the
★ arm in all five languages. Every implementation prints `300 grids of
10^5 cells: checksum 796071834`. The C mirror keeps the grid in one
flat array cleared by `memset`; the others build a row vector per row,
10^5 of them for the 10^5 by 1 grid.

BENCHTAB
