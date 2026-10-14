# 576. Out of Boundary Paths

There is an `m x n` grid with a ball. The ball is initially at the
position `[startRow, startColumn]`. You are allowed to move the ball to
one of the four adjacent cells in the grid (possibly out of the grid
crossing the grid boundary). You can apply at most `maxMove` moves to
the ball. Given the five integers `m`, `n`, `maxMove`, `startRow`,
`startColumn`, return the number of paths to move the ball out of the
grid boundary. Since the answer can be very large, return it modulo
`10^9 + 7`.

```
m = 2, n = 2, maxMove = 2, startRow = 0, startColumn = 0  ->  6
m = 1, n = 3, maxMove = 3, startRow = 0, startColumn = 1  ->  12
```

**Constraints:** `1 <= m, n <= 50`; `0 <= maxMove <= 50`; `0 <= startRow
< m`; `0 <= startColumn < n`.

## Approaches

Every arm is `fn find_paths(m: i64, n: i64, max_move: i64, start_row:
i64, start_column: i64) -> i64`. A path ends at the move that takes the
ball out, so the paths out with k moves to spend from a cell are one for
each side that leads straight out and, for each neighbour inside, that
neighbour's paths with k - 1.

| file | mechanism |
|---|---|
| `find_paths.kara` ★ | forward: a grid of how many paths end at each cell after the moves so far; each move sends every cell's count to its four neighbours, those outside added to the answer; O(maxMove * m * n) |
| `find_paths_memo.kara` | the recurrence above by recursion from the start, each (row, column, moves left) kept in a `Map` once worked out |
| `find_paths_pull.kara` | forward over one flat `Vec` of m * n counts: each move, every cell's count times its sides on the edge is added to the answer, and each cell's new count is the sum of its neighbours' old ones |
| `find_paths_backward.kara` | the recurrence above bottom up: a table of layers, layer k the paths out from every cell with k moves, each built from the one before; the answer read from the last |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 13 lines: nine grids at the edges (the two
examples, no moves, one cell with one move and with 50, a row and a
column, and the middle of a 5 by 5 grid with one move too few to leave
and just enough), a total and checksum over 300 random cases of 1 to
10 by 1 to 10 with 0 to 12 moves, and the problem's largest, 50 by
50 with 50 moves from a corner, the middle and the middle of an edge,
where the counts wrap many times. `find_paths.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every sequence of 1 to `maxMove` moves,
each written as a number in base 4 with one digit for each move, is
played out from the start, and it counts when the ball is in the grid
before its last move and out after it. Each arm is held to the
properties below on 1,000 random cases of 1 to 4 by 1 to 4 with 0 to
6 moves, from a random cell.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | turning the grid on its side changes nothing |
| P3 | turning it half round, the start with it, changes nothing |
| P4 | one move more never gives fewer paths |
| P5 | one move more gives the sides straight out, plus each neighbour's paths inside |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the counts never carried to the next move | P1 606, P5 673 |
| M2 | ★: left twice and never right | P1 565, P2 674, P3 507, P5 650 |
| M3 | memo: a cell with no moves left counted as a way out | P1 940 |
| M4 | memo: a result stored under two moves more | P1 292, P2 79, P3 115, P4 11, P5 360 |
| M5 | pull: a corner's two sides counted once | P1 800, P5 706 |
| M6 | pull: the right edge one column early | P1 521, P2 624, P3 484, P5 507 |
| M7 | backward: the neighbours read from layer 0 | P1 647, P5 784 |
| M8 | backward: a side out counted twice | P1 839, P5 949 |
| E1 | ★: the skip tested with `< 0` | 0 |
| E2 | memo: a result stored under one move fewer | 0 |
| E3 | pull: the new count made non-negative again | 0 |
| E4 | backward: the neighbours taken in the other order | 0 |

P2 and P3 see only the mutants that treat the grid's sides unequally:
M2 never moves right, M6 puts the right edge in the wrong place, and
M4's wrong results depend on the order the recursion visits cells in,
which turning the grid changes. M4 is also the only one P4 sees: every
other mutant, wrong as its counts are, still counts more paths with more
moves. P5 sees every mutant but M3: M3 counts a path still in the grid
when the moves run out as one that left, a wrong start for the same
recurrence, and P5 checks only the recurrence. E2 is safe for a reason
worth stating: each move changes the row plus the column by one, so the
recursion reaches a cell only ever with an even number of moves left or
only ever with an odd number, and a result stored under one move fewer
is never looked up. Two moves more keeps the parity, which is why M4 is
not safe. E3 is safe because the counts are never negative, and
E4 because addition does not mind the order.

## Verification

The four arms print the same output as `find_paths.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and run
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends: the ★, pull and backward arms print the
right output under `karac run --interp`, `karac run` and `karac build`,
and under `KARAC_AUTO_PAR=1 karac build`. The memo arm and the
differential stop at type checking on `return *known;`: legacy's
`Map.get` gives the value where v2 gives a reference ("unary '*'
requires 'ref T' ... found 'i64'"). Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 5,000 cases of 30 to 50 by
30 to 50 with 30 to 50 moves (up to the problem's most), each from a
random cell, and answers each once. Every implementation prints
`5000 cases up to 50 by 50 and 50 moves: total 729716617, checksum
261856686`, the Kāra program under `karac __mir-run` included (611 s).

Every implementation makes a fresh grid of counts for each move, as the
Kāra arm does: a `Vec<Vec<i64>>` in Rust, a slice of slices in Go, a
`calloc`'d row at a time in C and a list of lists in Python. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.81 to 0.94 s |
| Rust (`rustc -O`) | 1.02 to 1.15 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.14 to 1.19 s |
| Go | 2.09 to 2.23 s |
| Python | 43.0 to 43.7 s |
| Kāra (`karac build`, legacy) | 1.09 to 1.24 s |
| Kāra (`karac build --mir`) | 1.57 to 1.90 s |

The legacy `karac build` builds this program, so `bench.sh` is the
`scripts/new-bench.sh` output as it stands; the `--mir` row is the
v2 compiled backend, timed by hand at kara `680733538b`. Under `karac
__mir-llvm-run` the program prints the same line in 7.2 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

The `--mir` row is about 1.6 times Rust's and 1.5 times the legacy
backend's on the same program. The cause is not measured.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
