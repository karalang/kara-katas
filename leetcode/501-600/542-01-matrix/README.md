# 542. 01 Matrix

Given an `m x n` binary matrix `mat`, return the distance of the
nearest `0` for each cell. The distance between two cells sharing a
common edge is 1.

```
mat = [[0,0,0],[0,1,0],[0,0,0]]  ->  [[0,0,0],[0,1,0],[0,0,0]]
mat = [[0,0,0],[0,1,0],[1,1,1]]  ->  [[0,0,0],[0,1,0],[1,2,1]]
```

**Constraints:** `1 <= m, n <= 10^4`; `1 <= m * n <= 10^4`;
`mat[i][j]` is either `0` or `1`; there is at least one `0` in `mat`.

## Approaches

Every arm is `fn update_matrix(mat: Vec[Vec[i64]]) -> Vec[Vec[i64]]`.

| file | mechanism |
|---|---|
| `update_matrix.kara` ★ | breadth-first search from every 0 at once over a `VecDeque[(i64, i64)]`, the four steps in an array |
| `update_matrix_dp.kara` | two passes of dynamic programming: top-left to bottom-right from the cells above and to the left, then back from the cells below and to the right |
| `update_matrix_layers.kara` | the same search one layer at a time, each layer of cells in its own `Vec` |
| `update_matrix_sweeps.kara` | every 1 started at m + n and lowered to one more than its smallest neighbour, sweep after sweep, until a sweep changes nothing |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 10 lines: both examples, one cell, one row,
one column and a 0 in a corner, each with its answer; then a checksum
over the answers for 300 random grids of 1 to 12 by 1 to 12 with 1s at
30, 70 or 95 in 100 in turn; and last three grids of 10,000 cells (the
problem's most): 100 by 100 with 1s at 99 in 100, 100 by 100 all 1 but
one corner, and 10,000 by 1 all 1 but the top, each with its largest
distance (33, 198 and 9,999) and a checksum. `update_matrix.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
for each cell, the smallest `|dr| + |dc|` to any 0, found by looking at
every 0. Each arm is held to the properties below on 1,000 random grids
of 1 to 10 by 1 to 10, with 1s at 30, 70 or 95 in 100 in turn and one
random cell set to 0.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | 0 exactly on the 0s, neighbours apart by at most 1, and every cell above 0 next to one exactly 1 lower |
| P3 | the grid transposed gives the answer transposed |
| P4 | the grid mirrored left to right gives the answer mirrored |
| P5 | every 1 is at least 1 away, and no cell more than m + n - 2 |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the step to the right left out | P1 591, P2 557, P3 744, P4 711, P5 241 |
| M2 | ★: a neighbour given two more than the cell | P1 965, P2 965, P5 215 |
| M3 | dp: the cell above taken without the step to it | P1 835, P2 835, P3 897, P5 835 |
| M4 | dp: the cell to the right left out of the second pass | P1 588, P2 588, P3 751, P4 711, P5 210 |
| M5 | layers: the search stopped after the first layer | P1 653, P2 653, P5 653 |
| M6 | layers: each layer given one more than its distance | P1 965, P2 965, P5 56 |
| M7 | sweeps: the cell below left out | P1 604, P2 604, P3 751, P5 247 |
| M8 | sweeps: every 1 started at 2, not m + n | P1 411, P2 411 |
| E1 | ★: the four steps in another order | 0 |
| E2 | dp: unknown cells started at m n + 1, not m + n | 0 |
| E3 | layers: the next layer copied, not moved | 0 |
| E4 | sweeps: a change noticed with `!=`, not `<` | 0 |

P2 alone kills every mutant: a distance field is pinned down by its
0s, by neighbours never more than 1 apart, and by each positive cell
having a neighbour one lower, so any wrong answer breaks one of them.
P3 and P4 see only the edits that treat directions unevenly (M1, M3,
M4, M7). M4 breaks the transpose and the mirror, but M3 keeps the
mirror: dropping the step from the cell above is the same mistake in
the grid mirrored left to right. M8 is the only edit P5 misses, since
capping every distance at 2 keeps them all in range. E2 shows that the
dynamic programming arm needs only some value larger than any distance.

## Verification

Every arm prints the same output as `update_matrix.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `20000 checks, 0 failures` on the first two and runs clean under
the third. `karac check` passes on every arm, the differential and the
bench program.

The frozen legacy backends: `karac run --interp`, `karac run` and
`karac build` stop every arm and the differential at type checking, on
the harness's `*x` over `row.iter()` of a `Vec[i64]` ("unary '*'
requires 'ref T' ... found 'i64'"). The bench program stops at
`update_matrix(all[t])`, a `Vec` taken out of a `Vec` by index
(E_INDEX_MOVE_NON_COPY). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random 100 by 100 grids
(the problem's 10,000 cells), from half ones to 88 in a hundred, once;
then 50 times over every grid is answered, one row of the answer
picked by the round and the grid is summed, and one cell goes into the
checksum. Every implementation prints `20 grids, 50 times each: row sum
94249, checksum 125677597`, the Kāra program under `karac __mir-run`
included (44.5 s).

Rust uses a `VecDeque<(i64, i64)>` as the Kāra program does, Python a
`deque`, Go a slice of pairs with a moving head, and C a flat grid with
a ring of cell indexes. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.17 to 0.19 s |
| Rust (`rustc -O`) | 0.19 to 0.20 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.20 to 0.22 s |
| Go | 0.53 to 0.55 s |
| Python | 5.05 to 5.18 s |
| Kāra (`karac build --mir`) | 0.41 to 0.43 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`2649217dc8`. Under `karac __mir-llvm-run` the program prints the same
line in 2.4 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about twice Rust's, and a third of it is the queue.
Under callgrind, `karac_mir_deque_push` and `karac_mir_deque_pop` take
17% of the instructions each and `memcpy` another 10%. The same program
with a `Vec` and a head index in place of the `VecDeque` runs in 0.27 to
0.29 s (kara B-2026-10-13-36, below).

## Compiler findings

kara B-2026-10-13-36 (open), filed from this kata: `VecDeque`'s
`push_back` and `pop_front` on the v2 compiled backend are calls into
the runtime that wrap the index with an integer `%` and copy the
element with a `memcpy` call of a size passed at run time. About a
third of the ★ arm's time in the bench goes there.
