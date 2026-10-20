# 807. Max Increase to Keep City Skyline

A city is an `n` by `n` grid of buildings, `grid[r][c]` the height of
the building in row `r` and column `c`. The skyline seen from the left
or the right is the tallest building of each row, and from the top or
the bottom the tallest of each column. Any building may be made taller,
by any amount, as long as the skyline from all four sides stays the
same. Return the most floors that can be added in all.

```
grid = [[3,0,8,4],[2,4,5,7],[9,2,6,3],[0,3,1,0]]  ->  35
grid = [[0,0,0],[0,0,0],[0,0,0]]                  ->  0
```

**Constraints:** `n == grid.length == grid[r].length`, `2 <= n <= 50`,
and `0 <= grid[r][c] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `max_increase.kara` ★ | find the tallest of each row and of each column in one pass over the grid; each building can grow to the smaller of its row's and its column's tallest, and the buildings do not limit one another, so add up those headrooms. O(n²) |
| `max_increase_iter.kara` | the same with iterators: each row folded to its tallest, each column index mapped to the tallest of the rows at that index, and the headrooms summed by mapping over rows and columns |
| `max_increase_transpose.kara` | build the grid turned on its diagonal, so that its rows are the columns, and find both maxima with one function that takes the tallest of each row |
| `max_increase_scan.kara` | for each building walk its row and its column for their tallest, keeping nothing between buildings. O(n³) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 7 lines: LeetCode's two examples; `[[5]]`, one
building, which can never grow; `[[1, 2], [3, 4]]`, where only the 1 can
rise, by one; 50 by 50 with every building 100 tall, LeetCode's largest,
which has no room; 50 by 50 with only the diagonal built, to 100, where
each of the other 2,450 buildings can rise to 100; and 300 random grids
of 1 to 10 a side with heights from 0 to 100, with the floors added in
all and a checksum. `max_increase.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition by
trying: raise one building by one floor and keep it if the skyline from
the four sides is unchanged, sweeping the grid until no building can
grow, and return the floors added and the city it ends with. Its 1,600
cases have 1 to 5 a side and come in four kinds of 400: heights from 0
to 9; heights from 0 to 2, so that the tallest ties often; mostly empty,
with a few buildings 5 to 9 tall; and one row or one column of heights
from 0 to 9 with the rest 0.

| | property |
|---|---|
| P1 | the definition's answer |
| P2 | the grid turned on its diagonal, and the grid with its rows in the other order, give the same answer |
| P3 | every building made the same number of floors taller gives the same answer, and every building twice as tall gives twice it |
| P4 | the city the definition ends with has no room left |

It prints `1600 cases (18793 floors), 4 arms, 25600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | star: the rows' maxima taken down the columns | P1 862, P2 865, P4 862 |
| M2 | star: the taller of the two skylines taken | P1 1165, P4 1165 |
| M3 | star: every row's maximum started at 1 | P1 495, P2 481, P3 495, P4 495 |
| M4 | iter: every column's maximum taken from the first column | P1 1078, P2 976, P4 1078 |
| M5 | iter: each row's buildings added up rather than the tallest taken | P1 470, P2 456, P3 809, P4 633 |
| M6 | iter: the first row left out | P1 648, P2 729 |
| M7 | transpose: the grid not turned | P1 861, P2 865, P4 861 |
| M8 | transpose: the column limit read at the row's index | P1 831, P2 956, P4 831 |
| M9 | transpose: the last row left out | P1 652, P2 728 |
| M10 | scan: the column's maximum read along the row | P1 861, P2 865, P4 861 |
| M11 | scan: each building's height read on the diagonal | P1 1197, P2 1079, P4 1008 |
| M12 | scan: only the first i + 1 of each row and column scanned | P1 930, P2 1174, P4 447 |

P1 kills all twelve. P2 sees every edit but the ★ arm's taller of the
two maxima (M2), which, like the smaller, is the same whichever way the
grid is turned or its rows ordered. P3 sees only the two edits that do
not commute with adding a constant to every height and doubling it: the
row maxima started at 1 (M3), a floor a lifted grid no longer reaches,
and the rows added up rather than their tallest taken (M5), which grow
by `n` times the lift. Every other edit reads the wrong cell or the
wrong maximum, and goes wrong in the same proportion on the lifted and
doubled grids. P4 misses the two edits that leave out a row (M6, M9): in
a city with no room every row's headroom is 0, so the sum over the other
rows is still 0. One edit was replaced before this table: the iterator
arm reading each height across the diagonal, `grid[j][i]` for
`grid[i][j]`, is an equivalent mutant, since it subtracts the same
heights from the same sum in another order.

## Verification

Every arm prints the same output as `max_increase.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`ffb21df474`, which is its last compiler change. The runtime archives
were built after the last runtime change, `b03f2bc51f`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for all four arms and the differential, with a warning from the legacy
build that `grid` is used after a move, legacy taking a bare parameter
as owned rather than borrowed. For the same reason legacy refuses the
bench program at `max_increase_keeping_skyline(grids[r % 64])`, a move
out of an index; a copy with a `ref` parameter and the grid bound by
`ref` first builds and prints the same line, and the bench timing below
is of it. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 grids of 50
by 50, LeetCode's largest, with heights from 0 to 100, are made once.
Each of 300,000 rounds finds how much the next grid can grow. Every
implementation prints `300000 rounds of 50 x 50: 35605071847 floors in
all, checksum 254485605`, the Kāra program under `karac __mir-run`
included, in 1,297 s with `KARAC_MIR_MAX_STEPS` raised; at its default
of 40 billion steps the MIR interpreter stops the run after 1,044 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.29 to 1.46 s |
| Rust (`rustc -O`) | 1.74 to 1.95 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.81 to 2.12 s |
| Go | 2.05 to 2.34 s |
| Python | 211.01 to 218.47 s |
| Kāra (`karac build --mir`) | 2.12 to 2.31 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 10.2 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.25 s,
against C's 1.38, Rust's 1.80 (1.89 under overflow checks) and Go's
2.12. Under valgrind's cachegrind v2 runs 29.0 billion instructions and
6.96 billion branches, against Rust's 21.6 billion and 3.08 billion and
C's 13.5 billion and 1.57 billion. The legacy build of the copy ran 2.09
to 2.22 s, a median of 2.15 s in the interleaved runs, with 29.0 billion
instructions and 6.86 billion branches, so v2 takes 1.05 times legacy.
The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2.
