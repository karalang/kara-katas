# 417. Pacific Atlantic Water Flow

An `m x n` island borders the Pacific on its top and left edges and the
Atlantic on its bottom and right edges. `heights[r][c]` is the height of
each cell. Rain flows from a cell to any of its four neighbours that is
no higher, and from an edge cell into the ocean it borders. Return every
cell from which rain can reach both oceans.

```
heights = [[1,2,2,3,5],
           [3,2,3,4,4],
           [2,4,5,3,1],
           [6,7,1,4,5],
           [5,1,1,2,4]]
-> [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
```

**Constraints:** `1 <= m, n <= 200`; `0 <= heights[r][c] <= 10^5`. Any
order of the cells is accepted; every arm here returns them in row-major
order.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `pacific_atlantic.kara` ★ | turn the flow around: the cells that drain into an ocean are those reached from its edge by stepping to neighbours no lower. A breadth-first search with a `VecDeque` from each ocean's edge marks them; the answer is every cell both mark | O(m n) | O(m n) |
| `pacific_atlantic_dfs.kara` | the same uphill searches by recursion, one call per cell | O(m n) | O(m n), recursion up to m n deep |
| `pacific_atlantic_stack.kara` | one grid of flags, bit 1 for the Pacific and bit 2 for the Atlantic, and one explicit stack of (row, column, bit) for both searches; the answer is every cell holding both bits | O(m n) | O(m n) |
| `pacific_atlantic_sweep.kara` | the flow as stated, downhill: a cell drains into an ocean if it touches its edge or a neighbour no higher drains into it. Sweep the whole grid until nothing changes | O((m n)^2) at worst | O(m n) |
| `differential.kara` | the four arms on 1,000 random grids, five properties, one of them a search downhill from every cell on its own | — | — |

Every arm prints the same 10 lines: the LeetCode example, eight edge
cases (one cell, a flat grid, one row, one column, a basin, a peak, a
spiral climbing inward, a cross of low cells between four peaks) with
every cell of the answer, and for 1,000 random grids of 1 to 12 by 1 to
12 cells with heights below a random limit of up to 10, so that
plateaus are common, the number of cells and a checksum.
`pacific_atlantic.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 1,000 random
cases makes a grid of 1 to 9 by 1 to 9 cells with heights below a
random limit of up to 8. Answers are compared as grids of marks, so the
order of the cells does not matter:

| | property |
|---|---|
| P1 | a cell is in the answer exactly when a search downhill from that one cell reaches a Pacific edge and an Atlantic edge |
| P2 | the grid transposed gives the answer transposed, since each ocean's two edges map onto each other |
| P3 | the grid turned half a turn gives the answer turned half a turn: the two oceans swap, and the answer needs both |
| P4 | every height `h` replaced by `3h + 7` changes nothing |
| P5 | the top-right and bottom-left corners touch both oceans, so they are always in the answer, and a flat grid's answer is every cell |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | bfs: water climbs only to strictly higher cells | P1 732, P5 788 |
| M2 | bfs: the left column is not a Pacific start | P1 617, P2 808, P3 690, P5 617 |
| M3 | dfs: the search never steps down a row | P1 557, P2 648, P3 624 |
| M4 | dfs: the bottom row is not an Atlantic start | P1 614, P2 803, P3 693, P5 614 |
| M5 | stack: the start cells are pushed without their bits | P1 561, P5 479 |
| M6 | stack: a cell with either bit counts | P1 637 |
| M7 | sweep: the grid is swept once | P1 614, P3 666, P5 607 |
| M8 | sweep: water never flows to the right | P1 568, P2 647, P3 641 |

No mutant fails P4: every arm and mutant compares heights only with
each other, which `3h + 7` keeps in order. M1 stops at plateaus, which
the flat grid of P5 is made of. M2, M3, M4 and M8 break the symmetry
between the oceans or the directions, which P2 and P3 see; M3 and M8
leave the corners alone, since a corner touches both oceans whatever
the search does. M6 answers the union of the two oceans' cells, not
their intersection, and only P1 sees it, since a union is as symmetric
as the right answer. M7's one row-major sweep carries water down and to
the right but never back up, so it differs from its half-turned self.

## Verification

All four arms print the same output as `pacific_atlantic.py` on every
backend: `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run`, `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. `karac check` passes on every file.
The differential prints `20000 checks, 0 failures` on all six. The
frozen legacy `karac build` warns that the ★ arm and the bench reuse
`heights` after passing it to `climb`, since it predates bare
parameters borrowing; they still build and run. Not filed.

The ★ arm marks its start cells with `for (r, c) in queue.iter() {
seen[r][c] = true; }`. The items are `ref (i64, i64)`, and a
destructured `Copy` part copies, so `r` and `c` are `i64` and take no
`*`. `karac check` also accepts `seen[*r][*c]`, which `karac __mir-run`
refuses: that split is already open as kara `B-2026-10-12-9`.

## Benchmarks

The bench program uses the ★ arm on one 200 x 200 grid (the problem's
limit) with a ridge along the anti-diagonal, rising three units a step
from the top-left and bottom-right corners plus noise of 0 to 2, so
that each search climbs to the ridge and covers half the grid. Each of
3,000 rounds digs a pit at a random cell, any height from 0 up to its
own level, and finds the answer again, so no compiler can hoist the
search out of the loop; it folds the number of cells and the last cell
into a total and a checksum. Every implementation prints `3000 rounds
on a 200x200 grid: 576052 cells, checksum 103984603`; a 30-round cut of
the Kāra program under `karac __mir-run` prints the same as the C
program cut the same way. As in the Kāra program, each call of the C
mirror allocates its own queues, marks and answer, and the Go mirror
uses a slice read from a moving head as its queue. Spot timings on a
shared 4-core container, three runs each (`bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.34 to 1.55 s |
| Rust (`rustc -O`) | 1.82 to 1.97 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.05 to 2.13 s |
| Go | 5.6 to 6.4 s |
| Kāra (legacy `karac build`) | 6.1 to 6.8 s |
| Python (a 30-round cut, 0.71 s, times 100) | about 70 s |

The Kāra program takes three times as long as the Rust one, which
holds the same `Vec` of `Vec`s and the same `VecDeque`; why has not
been looked into, and the legacy backend is frozen. The Kāra program
also prints the same line under `karac __mir-llvm-run` in 12.5 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark. The `karac build` time is the frozen legacy
backend.

## Compiler findings

No new findings. The `*` split above is kara `B-2026-10-12-9`.
