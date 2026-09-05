# 317. Shortest Distance from All Buildings

A grid of `0` (empty land), `1` (building) and `2` (obstacle). Choose an empty
cell that minimises the **sum of walking distances to every building**, moving
up/down/left/right across empty land only — buildings and obstacles both block
the way. Return that minimum sum, or `-1` if no empty cell can reach every
building.

```
1 0 2 0 1
0 0 0 0 0      ->  7     stand at (1, 2): 3 + 3 + 1
0 0 1 0 0

1 0 0 0 1      ->  4     three cells tie
1 2 0          -> -1     the obstacle seals the only land off
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `shortest_distance.kara` ★ | one BFS per **building**, accumulate `total` and `reach` per cell | `O(B · R·C)` |
| `shortest_distance_from_empty.kara` | one BFS per **empty cell**, early exit once every building is seen | `O(E · R·C)` |
| `shortest_distance_pruned.kara` | in-place shrinking grid: the k-th wave may only enter cells stamped by all k−1 before it | `O(B · R·C)`, shrinking |
| `shortest_distance_relax.kara` | relaxation to a fixpoint (Bellman–Ford on the grid), no queue | `O(B · R·C · diameter)` |
| `differential.kara` | four arms, eleven properties, 2,267 grids | — |
| `bench/shortest_distance.kara` | 360×360 grid, 20 buildings, 30 relocation passes | — |

## Four ways to find the cell

**★ Search from the buildings.** The statement reads "for each empty cell, how
far to every building?", and that reading costs one BFS per empty cell — most of
the grid. Turn it around: one BFS per building, and there are a handful of
those. Each wave walks empty land only, deposits its depth into `total[cell]`
and bumps `reach[cell]`; the answer is the smallest `total` among empty cells
whose `reach` equals the building count. That `reach` test *is* the `-1` story:
a cell some building never reached has a total missing a term and must be
excluded, not compared. A building is a source, never a waypoint — wave A does
not pass through building B — and an obstacle is never entered at all.

**Search from the empty cells.** The literal reading, kept because it shares
nothing with the ★ arm that matters: no `reach` count, no accumulation across
sources, and an early exit the moment the wave has touched every building. A
cell whose wave dies first is not a candidate. `O(E · R·C)` against
`O(B · R·C)`, which on a mostly-empty grid is the difference between the number
of candidates and the number of targets.

**The shrinking grid.** Same direction as ★ but with no `reach` array and no
per-building reset: the grid is the visited mark. The k-th building's wave may
only enter cells holding `-k` — cells every earlier wave reached — and stamps
them `-(k+1)`. A cell one building cannot reach keeps its old value and is
invisible to every later wave, so the searchable region only shrinks, and a grid
with a walled-off building collapses to nothing instead of paying `B` full
sweeps. The depth rides in the queue as `(cell, depth)` rather than in a table.
The price is that it mutates its input, so it works on a copy.

**Relaxation to a fixpoint.** The oracle. Shortest distance from a source is the
unique `d` with `d(source) = 0` and `d(cell) = 1 + min over passable neighbours`
on every reachable empty cell. Start every empty cell at infinity, sweep the
grid lowering each cell to one more than its smallest neighbour, repeat until a
sweep changes nothing. It knows nothing about frontiers, waves, first arrivals
or visited marks — every place a BFS can be wrong — and it is exact, so on the
grids the harness generates it settles every case outright.

## The differential

2,267 grids: every `rows × cols` up to 7×7, obstacle densities of 0/15/30/50%,
one to four buildings, three seeds each; plus corridors with a building at each
end, a building walled into a ring, checkerboards of obstacles, and two rooms
joined by a single door. 1,382 are feasible, 885 return `-1`, 588 have exactly
one building. The oracle is complete, so P1 alone is a verdict on each grid; the
rest of the table is what the statement implies without any arm's help:

| property | what it checks | who it binds |
|---|---|---|
| P1 | relax oracle == ★ | ★ |
| P2 | from-empty == ★ | from-empty |
| P3 | pruned == ★ | pruned |
| P4 | **transpose invariance**: `solve(gridᵀ) == solve(grid)` | each arm |
| P5 | **flip invariance**: left-right and top-bottom mirrors | each arm |
| P6 | **Manhattan floor**: the answer is `-1` or ≥ the smallest sum of Manhattan distances from any empty cell | ★ |
| P7 | **walling one empty cell never helps** (2,115 cases): `-1` stays `-1`, otherwise the answer stays or grows or becomes `-1` | ★, two invocations |
| P8 | **clearing one obstacle never hurts** (1,398 cases): a finite answer stays finite and does not grow | ★, two invocations |
| P9 | **the witness realises the answer**: the argmin cell is empty land and an independent per-cell BFS from it sums to exactly the answer | ★ |
| P10 | **local optimality**: every empty neighbour of the witness (2,258 checked) costs at least the answer | ★ |
| P11 | **one building**: the answer is 1 if it has an empty neighbour, else `-1` | ★ |

P4 and P5 are isometries of the grid graph, so they bind every arm through
symmetry rather than through an oracle — a neighbour test that is right on
three sides, or an index mix-up invisible on square grids, shows up here even
in the oracle itself (see M12 below). P7 and P8 relate two invocations of the ★
arm on grids that differ in exactly one cell.

Green on `karac run`, `karac build`, the auto-par build and `--interp`,
byte-identical.

## Mutation testing

Content-anchored edits inside named function bodies, each compiled and run
through the full differential (AOT, `KARAC_AUTO_PAR=0`) under a 120-second
budget that reports a hang or a panic as a kill. Two controls (a local rename in
the ★ arm; the pruned arm's `walk -= 1` respelled) must stay silent.

| mutant | edit | outcome | fired |
|---|---|---|---|
| M1 | ★: `step` never bumps `reach` | killed | P1/P2/P3 1,382, P11 531 |
| M2 | ★: accept cells reached by *any* building | killed | P1/P2/P3 962, P6 961, P7 255, P8 174, P9 962 |
| M3 | ★: waves pass through buildings | killed | P1/P2/P3 504, P9 579 |
| M4 | ★: row index divides by `rows` | killed — **panics** | `vec index out of bounds` in `step` |
| E5 | ★: min test `<` → `<=` | **equivalent** — silent, as predicted | — |
| E6 | from-empty: early exit removed | **equivalent** — silent, as predicted | — |
| M7 | from-empty: buildings skipped like obstacles | killed | P2 1,382, P9 1,382 |
| M8 | from-empty: building distance off by one | killed | P2 1,382, P9 1,382, P10 1,166 |
| M9 | pruned: wave enters anything `>= walk` | killed | P3 871 |
| M10 | pruned: accept partially reached cells | killed | P3 1,218, P4 127, P5 504 |
| M11 | pruned: `total` adds `depth`, not `depth + 1` | killed | P3 1,382 |
| M12 | oracle: right neighbour never relaxed | killed | P1 518, **P4 663, P5 550** |
| E13 | oracle: obstacle guard dropped on one side | **equivalent** — silent, **not predicted** | — |
| X14 | ★ returns the Manhattan floor | killed | P1/P2/P3 871, P9 871, P11 34 |
| C1 | ★: rename a local | control — silent | — |
| C2 | pruned: `walk -= 1` → `walk = walk - 1` | control — silent | — |

**The oracle can be wrong too, and the symmetry properties are what catch it.**
M12 breaks the relaxation arm — one of four neighbours never relaxed — and P1
fires, but so do P4 and P5 *on the oracle itself*: a right-blind sweep gives a
different answer on the mirrored grid. That is the whole case for invariance
properties in a harness that already has a complete oracle: they bind the oracle
as well as the arms under test, which agreement never can.

**A guard I wrote is dead code, and the harness proved it.** E13 deletes the
`grid[…] != 2` obstacle test from one side of the oracle's relaxation and nothing
fires. I expected a kill. It cannot fire: an obstacle — like a non-source
building — is never itself relaxed (`grid != 0` skips it), so its `d` stays at
infinity and `INF + 1 < best` is false whatever the guard says. The obstacle
guard is implied by the skip. The source file keeps the guard, because the
program reads better with the rule stated than with it implied, but the comment
now says which of the two is load-bearing. M13 became E13 when the run came
back, which is the correct direction for a prediction to be corrected in: the
harness knows, the author guesses.

**M4 is a kill by crash, and the harness must count it.** Dividing by `rows`
instead of `cols` computes a wrong row on every non-square grid; the wrong row
sends `step` one cell past the end of a 1×n corridor, and Kāra's checked
indexing panics before any property runs. A harness that only parsed property
lines would score that "no properties fired" — silent — which is the opposite
of the truth. It reports `PANIC` as a kill, as it reports `HANG` (#316's M8).

X14 is the consistent-mirror probe: with the ★ arm replaced by the Manhattan
floor, P2 and P3 fire only because the other arms are *right*; strip them and
it is P1, P9 (the witness's true cost is not the floor) and P11 (a walled-in
single building has floor 2, not `-1`) that carry it.

## Benchmark

`build-once + punch`: a 360×360 grid generated once — 20% obstacles, then 20
buildings dropped on empty cells reachable from the top-left corner, so no
building starts walled off — and 30 passes. Each pass **relocates one
building** (the pass's turn in the site list) to the first empty cell at or
after an index drawn from the running checksum, runs the ★ arm, folds the
answer into the checksum, and moves the building back so the grid does not
drift. All five mirrors use the same flat `i64` grid, the same array queue and
the same per-pass `seen` stamp in place of a per-building reset, and agree on
`checksum 937035897`.

**The first punch was a dud, and the sink said so.** The first design walled
one empty cell per pass — the #316 shape. The sink was fine and every mirror
agreed, but a debug print showed all 30 passes returning the same answer,
3,249: one wall among 100,000 open cells never moves the minimum. A punch the
optimiser cannot hoist is not the same as a punch the workload can feel.
Relocating a building shifts every pass's answer (3,379 … 3,545 across the
run), so each pass now measures a different problem of the same size.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each, box otherwise idle. σ is 1–3% on every lane except Rust's default
build (5.4%) and Go's (10.3%) — canonical Apple-silicon numbers await an idle
run on the owner's machine ([#313's methodology note](../313-super-ugly-number/#a-methodology-note-because-the-first-version-of-this-table-was-wrong)).

| | mean | vs kara |
|---|---:|---:|
| c (`-O3`) | 1097 ms ± 13 | 0.80× |
| c (`-O3 -march=x86-64-v3`) | 1117 ms ± 27 | 0.81× |
| **kara** (codegen, seq) | **1379 ms ± 29** | **1.00×** |
| rust (`-O`) | 1459 ms ± 79 | 1.06× |
| rust (`-O -C overflow-checks=on`, equal safety) | 1478 ms ± 50 | 1.07× |
| rust (equal safety + matched ISA) | 1491 ms ± 30 | 1.08× |
| go | 2630 ms ± 270 | 1.91× |

**The four compiled lanes are two bands, and the split is not about safety.**
C is 20% ahead of everything else. Kāra, both Rust builds and the matched-ISA
twin land within 8% of each other — the Kāra-to-Rust gap of 5.8% is about one
σ of the Rust lane, so read those four rows as a tie rather than as Kāra
winning. Turning Rust's overflow checks on costs 1.3%, which is the tell: this
workload is not arithmetic-bound, so equalising safety barely moves it.

**What C has is the neighbour test.** The inner loop visits ~60 million cells
over the run and does four neighbour probes at each: load `grid[nb]`, load
`seen[nb]`, compare, and on a hit write four arrays and push. C indexes raw
`long long*` with no checks. Kāra, Rust and Go each bounds-check every one of
those loads against five separate arrays, and Kāra additionally overflow-checks
the `cell ± cols` arithmetic and the `total[nb] += d` accumulation. The checked
lanes cluster; the unchecked one is alone.

**Go's 10% σ is its allocator, not the box.** Every BFS call allocates five
`n`-element slices plus a growing queue, 600 times over the run, and Go is the
only lane that hands those to a GC. It is also the only lane whose system time
is a large fraction of its wall time.

Peak RSS is 7.3 MiB (C), 8.7 MiB (Rust), 10.9 MiB (Kāra) and 19.8 MiB (Go)
against a working set of about 5.2 MiB — the grid plus five `i64` tables. The
Kāra binary is 345 KiB, its compute floor plus the grid code; C's is 16 KiB,
Rust's 3.9 MiB and Go's 2.2 MiB.

## Compiler findings: nothing to file

Six sources — four arms, the differential and the bench mirror — checked clean
(zero diagnostics) on the first `karac check --output=json` of each. The four
arms and the differential are byte-identical across `karac run`, `karac build`,
the auto-par build and `--interp`, first time. The bench mirror is checked on
the first three, and against its C, Rust, Go and Python twins (all five mirrors
agree on `checksum 937035897`); its `--interp` leg is omitted deliberately, because at
the ratio measured below a 1.4-second binary is several hours of tree walking.
Nothing on the way needed `karac fix`. The surfaces this
kata leans on all held: a `VecDeque[(i64, i64)]` queue of tuples with
`let (cell, depth) = entry;` inside a `match` arm, a `mut ref Vec[i64]`
threaded from the caller through the BFS into a helper called from the arm
(`step`), `Vec[Vec[i64]]` and `Vec[(i64, i64)]` side by side in the demos with
`let (rows, cols) = dims[t];`, `if` as an expression (`let expect = if … { 1 }
else { -1 };`), and a `continue` inside a `while` loop nested in a `match` arm
inside a `loop`.

One measurement rather than a finding: the differential runs in **0.09 s** under
AOT, **0.86 s** under the JIT (nearly all of it compile), and **3 m 49.7 s**
under `--interp` — a tree-walk-to-native ratio of about **2,550×** on this
BFS-heavy, index-heavy code. That is what makes `--interp` the slow leg of the
A/B rule for any grid kata, and it is worth knowing before designing one: the
harness's 2,267 grids were sized against the interpreter, not the binary.
