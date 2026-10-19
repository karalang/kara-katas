# 803. Bricks Falling When Hit

A wall is an `m x n` grid of `1`s (bricks) and `0`s (empty cells). A
brick is stable if it is in the top row, or if one of the four bricks
next to it is stable. `hits[i] = (row, col)` erases the brick at that
cell, if there is one; bricks that are no longer stable then fall and
are erased at once. Return how many bricks fall after each hit, the hit
brick itself not counted.

```
grid = [[1, 0, 0, 0], [1, 1, 1, 0]], hits = [[1, 0]]          ->  [2]
grid = [[1, 0, 0, 0], [1, 1, 0, 0]], hits = [[1, 1], [1, 0]]  ->  [0, 0]
```

**Constraints:** `1 <= m, n <= 200`, `1 <= hits.length <= 4 · 10^4`, the
hit cells are all different, and `grid[i][j]` is `0` or `1`.

## Approaches

| file | mechanism |
|---|---|
| `hit_bricks.kara` ★ | union-find run backwards: knock out every hit brick, join the bricks left and the top row to a roof, then put the hit bricks back from the last hit to the first; the bricks a hit made fall are the ones putting it back joins to the roof. O((rows · cols + hits) · α) |
| `hit_bricks_flood.kara` | play the hits forward; after each one, flood from the top row through the bricks, and every brick not reached falls. O(hits · rows · cols) |
| `hit_bricks_local.kara` | play the hits forward; only bricks held up through the hit brick can fall, and each is joined to one of its four neighbours, so search each neighbour's group: if it reaches the top row it stays, and if not it falls |
| `hit_bricks_grow.kara` | the backward order with flooding in place of union-find: mark the bricks held up once the hits are knocked out, then put the hit bricks back; one put back in the top row or next to a held brick holds up everything not yet held joined to it, and all but itself are the bricks its hit made fall. Each brick is flooded once |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: LeetCode's two examples; a column of
four hit second from the top; a wall of two rows joined by one brick in
the middle, hit there; a hit on an empty cell and then on the only top
brick of a base; a ring hit at three of its top bricks, where only the
second hit brings anything down; a base held up by two top bricks, then
hit where it has already fallen; and 300 random walls of up to 8 by 8
cells, each with some of its cells hit in a random order, bricks and
empty cells alike, with how many bricks fell in all and a checksum.
`hit_bricks.py` mirrors the ★ arm and its output is byte-identical.

The random walls start with every brick stable: the harness takes away
any brick not held up from the top row before the hits. A brick that
started loose would be counted as falling at the first hit by the arms
that play the hits forward, and never by the ones that play them
backwards, and the arms do not agree there.

## Differential

`differential.kara` holds copies of the four arms and the definition. A
fallen brick held nothing up, so whether a brick still stands after hit
`k` turns only on the wall less the first `k + 1` hits: it stands while
a walk through those bricks reaches it from the top row. Each brick
falls at the first hit after which it is not reached, and is counted
there unless that hit was on the brick itself. The definition sweeps the
wall for reached bricks after each hit, without ever taking a fallen
brick away. Its 1,600 cases come in four kinds of 400, each with its
loose bricks taken away: walls of up to 7 by 7 with three cells in four
a brick; with two in four; with every cell a brick; and one or two
columns of up to 9 rows. Some of the cells are hit in a random order.

| | property |
|---|---|
| P1 | the definition's counts |
| P2 | the wall and the hits mirrored left to right give the same counts |
| P3 | one count a hit, none below zero, none for a cell empty at the start; the bricks that fell and those still standing at the end are all the bricks but at most one a hit |
| P4 | the second half of the hits, played on the wall the first half leaves, gives the second half of the counts |

It prints `1600 cases (3920 fell), 4 arms, 25600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: row 1 joined to the roof, not row 0 | P1 754, P3 118, P4 82 |
| M2 | ★: the hit brick counted among the fallen | P1 1357 |
| M3 | ★: a hit on an empty cell put back as a brick | P1 489, P3 359, P4 59 |
| M4 | flood: the flood never going up | P1 144, P3 3, P4 39 |
| M5 | flood: fallen bricks counted but left in the wall | P1 598, P3 399, P4 429 |
| M6 | flood: the first column's top brick not flooded from | P1 470, P2 567, P3 53, P4 166 |
| M7 | local: a group reaching row 1 taken as up | P1 564, P3 142, P4 82 |
| M8 | local: only the neighbour above searched | P1 804, P3 307, P4 137 |
| M9 | local: a fallen group left in the wall | P1 432, P3 249, P4 283 |
| M10 | grow: a brick put back next to any brick taken as held | P1 426, P4 283 |
| M11 | grow: the brick put back counted among the fallen | P1 1357 |
| M12 | grow: a brick put back in the top row not taken as held | P1 488, P3 141 |

P1 kills all twelve. P2 kills only the flood edit that does not start
from the first column, the one edit that treats left and right unlike.
P3 sees every edit but three: the two that count the hit brick among the
fallen (M2, M11), which only move each hit brick from the knocked-out
bricks to the fallen ones, as P3's count allows, and the grow edit that
takes a brick put back next to any brick as held (M10), whose totals
also stay in P3's range. P4 sees all but M2, M11 and the grow edit that
takes a brick put back in the top row as loose (M12).

## Verification

Every arm prints the same output as `hit_bricks.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`37548799f9`, which is its last compiler change. The runtime archives
were built after the last runtime change, `216d20e28a`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy compiler prints the same output for all four arms and
the differential, unchanged, under its interpreter (`karac run
--interp`), its JIT (`karac run`) and `karac build`, with warnings that
`grid` or `wall` is used after a move. An auto-par build
(`KARAC_AUTO_PAR=1`) of the flood arm prints wrong counts, the same on
each of three runs: `[0, 0]` becomes `[1, 0]` for LeetCode's second
example, and the random walls give 2810 falls where the rest give 1180.
The differential's auto-par build reports `P1: 876 failures | P3: 283
failures | P4: 581 failures`. Legacy refuses the bench program at
`hit_bricks(walls[r % 8], all_hits[r % 8])`, a move out of an index,
legacy taking a bare parameter as owned rather than borrowed; a copy
with `ref` parameters and the wall and hits bound by `ref` first builds
and prints the same line, and the bench timing below is of it. Legacy is
frozen and auto-par is opt-in, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 8 walls of 200
by 200 cells, LeetCode's largest, are made once, three cells in four a
brick and the loose bricks taken away, each with 20,000 of its cells,
bricks and empty alike, to hit in a random order. Each of 500 rounds
counts the falls for the next wall. Every implementation prints `500
rounds of 20000 hits: 11561383 bricks fell, checksum 740642802`, the
Kāra program under `karac __mir-run` included (in 184 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.73 to 0.92 s |
| Rust (`rustc -O`) | 1.27 to 1.56 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.19 to 1.52 s |
| Go | 1.64 to 1.88 s |
| Python | 26.85 to 26.86 s |
| Kāra (`karac build --mir`) | 1.67 to 1.86 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 4.6 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.72 s,
against C's 0.81, Rust's 1.46 (1.30 under overflow checks) and Go's
1.71. Under valgrind's cachegrind v2 runs 10.8 billion instructions and
2.61 billion branches, against Rust's 5.17 billion and 1.46 billion and
C's 2.42 billion and 503 million. The legacy build of the copy ran 1.43
to 1.74 s, a median of 1.51 s in the interleaved runs, with 9.95 billion
instructions and 2.05 billion branches, so v2 takes 1.14 times legacy.
v2 and legacy each make 60 million indirect branches, 120,000 a round,
where Rust and C make under a million in all; this was not traced to its
source. The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2.
