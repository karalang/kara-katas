# 1034. Coloring A Border

You are given an `m x n` integer matrix `grid`, and three integers
`row`, `col`, and `color`. Each value in the grid represents the color
of the grid square at that location.

Two squares are called adjacent if they are next to each other in any
of the 4 directions.

Two squares belong to the same connected component if they have the
same color and they are adjacent.

The border of a connected component is all the squares in the
connected component that are either adjacent to (at least) a square
not in the component, or on the boundary of the grid (the first or
last row or column).

You should color the border of the connected component that contains
the square `grid[row][col]` with `color`.

Return the final grid.

```
grid = [[1,1],[1,2]],               row = 0, col = 0, color = 3  ->  [[3,3],[3,2]]
grid = [[1,2,2],[2,3,2]],           row = 0, col = 1, color = 3  ->  [[1,3,3],[2,3,3]]
grid = [[1,1,1],[1,1,1],[1,1,1]],   row = 1, col = 1, color = 2  ->  [[2,2,2],[2,1,2],[2,2,2]]
```

**Constraints:** `1 <= m, n <= 50`; `1 <= grid[i][j], color <= 1000`;
`0 <= row < m`; `0 <= col < n`.

## Approaches

| file | mechanism |
|---|---|
| `color_border.kara` ★ | depth-first, by recursion: walk the component from `(row, col)` over neighbours of the same value, marking squares seen. A square with a neighbour off the grid or of another value is on the border and is painted in a copy, so the walk always reads the original values. O(m n) |
| `color_border_bfs.kara` | breadth-first with a `VecDeque`: each square is checked against its neighbours as it leaves the queue, and the border squares are painted once the walk is done. O(m n) |
| `color_border_mark.kara` | marking in place, with a stack: every value is at least 1, so a square of the component is marked in the copy by negating it. Then a marked square is on the border when a neighbour is off the grid or unmarked, and every marked square becomes `color` or its value again. O(m n) |
| `color_border_union.kara` | union-find over the whole grid: every pair of neighbours of the same value joined in a disjoint-set forest (path halving, union by size), then the squares in the start's set with a neighbour off the grid or in another set are the border. O(m n) near enough |
| `color_border_sweeps.kara` | sweeps until nothing changes: the component grows from the start alone, sweep after sweep over the grid, taking in every square of the same value beside one already in, until a sweep takes in nothing. A square in it with fewer than four neighbours in it is on the border. O(m n) per sweep |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 17 lines: the answers for eight grids,
LeetCode's three examples among them, and for a random 6 by 6 grid of
two colours; for 60 random grids of up to 30 by 30 with colours up to
1, 2, 3 and 1,000 each, the squares changed and a checksum; and the
same for four 50 by 50 grids (one colour, concentric rings from a
corner and from the centre, and a path winding through every row).
`color_border.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: two squares are joined when they are next to each other and
of one colour, the component is everything joined to `(row, col)` by a
chain of such pairs, found as the closure of that relation over every
pair of squares (Warshall's algorithm), and a square of it is on the
border when it is next to a square not in it or on the first or last
row or column. It checks 1,022 cases: every grid of up to 3 by 3
squares of colours 1 and 2 (682), each from a random square with a
random colour from 1 to 3, then 300 random grids of up to 6 by 6 and
40 of up to 30 by 30, with colours up to 1, 2, 3 or 9. The 988 grids
of at most 36 squares are searched in full. Each case is also asked
with the grid turned on its diagonal, turned upside down, and with
every colour and the new one raised by a random amount from 1 to 50.

| | property |
|---|---|
| P1 | the statement read literally, on grids of at most 36 squares |
| P2 | turning the grid on its diagonal turns the answer |
| P3 | turning the grid upside down turns the answer |
| P4 | raising every colour and the new one by `k` raises the answer by `k` |
| P5 | the answer has the grid's shape; a square changes only to `color` and only if it had the start's colour; the start, when on the grid's edge, takes `color` |
| P6 | each arm agrees with at least two of the other four |

The differential prints `1022 cases (988 searched in full): checksum
296680363, 30490 checks over 5 arms: 0 failures` under `karac
__mir-run` (2.9 s), `karac __mir-llvm-run` and `karac __mir-llvm-asan`
with no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`. Fifteen are kept, three to each arm. All
fifteen are killed, each fails the same checks under both backends,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the painted copy read for the border, not the grid | P1 31, P2 12, P3 5, P6 35 |
| M2 | ★: never looks right | P1 292, P2 394, P5 5, P6 303 |
| M3 | ★: the walk never goes up | P1 285, P2 406, P3 434, P6 296 |
| M4 | bfs: only a neighbour off the grid counts, and the last one looked at decides | P1 488, P2 495, P3 63, P5 226, P6 507 |
| M5 | bfs: squares in the last row never walked from | P1 479, P2 501, P3 594, P5 283, P6 487 |
| M6 | bfs: the colour of the top-left square, not the start's | P1 348, P3 407, P5 247, P6 363 |
| M7 | mark: never steps sideways | P1 422, P2 505, P6 435 |
| M8 | mark: the inside left marked | P1 65, P4 74, P5 74, P6 74 |
| M9 | mark: the walk stops after 40 squares | P2 8, P3 7, P4 8, P5 8, P6 8 |
| M10 | union: the second square joined, not its root | P1 126, P2 42, P3 200, P6 131 |
| M11 | union: the first column never joined down | P1 167, P2 281, P6 169 |
| M12 | union: every pair across joined, whatever the colour | P1 704, P2 427, P5 591, P6 730 |
| M13 | sweeps: never reached from the right | P1 266, P2 406, P6 276 |
| M14 | sweeps: a square with one neighbour outside not border | P1 173, P5 46, P6 181 |
| M15 | sweeps: three sweeps only | P1 28, P3 57, P6 34 |

P6 kills all fifteen, P1 fourteen, P2 eleven, P3 and P5 eight each,
and P4 two. P1 misses only the walk that stops after 40 squares (M9),
since no grid it searches has more than 36. P2 misses the edits that
go as wrong on the grid turned on its diagonal, such as taking the
top-left square's colour (M6), which the turn leaves in place, or a
square with one neighbour outside left unpainted (M14). P4 sees only the edits that
leave a value no colour can raise to: a negated mark left in the
answer (M8), and the 40-square walk (M9), which leaves its unvisited
neighbours marked. M1 is the trap the ★ arm's comment names: reading
the copy being painted, a neighbour already painted looks like
another colour. The checks draw random numbers for every case
whatever the answers, so every mutant sees the same cases and their
counts can be compared.

Fifteen other edits were tried and set aside, and one more was
replaced before it finished. Four change no answer and are
equivalent: the mark arm also counting a marked neighbour of another
colour as outside (every marked square holds the same mark), the mark
arm not marking the start square (a neighbour pushes it again and it
is painted the same), path halving jumping three levels, and the
union arm asking a neighbour's colour instead of its set (a neighbour
of the same colour is in the same set). Two crash under both backends
with an index out of bounds (exit 101): ★ never treating the bottom
and right edges as off the grid, and the union arm indexing the start
by the row count. The other nine were killed too, beyond three per
arm. Two fail exactly alike, `P1 421, P3 570, P5 309, P6 442`: bfs
walking from the top-left square too, and sweeps taking the top-left
square in from the start. Seven fail on their own: ★ painting the
inside too, and seeing every square before the walk; bfs painting the
inside and not the border, and painting at the transposed square;
mark counting only the grid's edge as border; sweeps taking in every
colour, and the row above wrapping round the grid. The replaced edit,
bfs never marking a square seen when it is queued, never ends: the
queue grew past 4.8 GB under `karac __mir-run` in two minutes, so it
was stopped and replaced by M5.

## Verification

Every arm prints the same output as `color_border.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. The differential prints its line under all three. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reported two things. The ★
arm passed `seen` and `out` to its `mut ref` parameters without the
call-site `mut` (E0218, four times); each came with a
machine-applicable edit, and `karac fix` wrote `mut seen, mut out` at
both calls. The union arm's methods were first written with Rust's
`mut self`, which is E0003 "'mut' is a reserved keyword and cannot be
used as an identifier", with no fix. I wrote Kāra's `mut ref self` by
hand, and the missing fix is kara `B-2026-11-01-5`. The bench program
read `let grid = grids[g];` (E_INDEX_MOVE_NON_COPY, with a
machine-applicable edit), and `karac fix` made it `ref grids[g]`.
Every file then checks clean. The release build is kara `6697158faf`,
with runtime archives rebuilt at that commit. Under `karac __mir-run`
the arms take 0.47 s (★, bfs) to 1.2 s (sweeps).

## Benchmarks

The bench builds 100 random 50 by 50 grids (LeetCode's largest), each
square colour 1 two times in three and 2 otherwise, so most starts land
in one large component, with 10 random starts and new colours from 1
to 3 for each grid, once in all five languages. Then it answers all
1,000 starts 20 times with the ★ arm, counting the squares changed and
folding their places into a checksum. Every call allocates its seen
marks and its copy of the grid: rows of `Vec`s in Kāra and Rust, rows
of slices in Go, lists in Python, and one block each in C. Every
implementation prints `100 grids of 50 by 50, 10 starts each, 20
rounds: 10000960 squares changed, checksum 416693405`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.481 to 0.524 s | 0.491 s |
| Rust (`rustc -O`) | 0.678 to 0.761 s | 0.728 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.708 to 0.870 s | 0.734 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.874 to 0.980 s | 0.906 s |
| Kāra (`karac build`) | 0.908 to 1.034 s | 0.951 s |
| Go | 1.243 to 1.354 s | 1.293 s |
| Python | 19.0 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(0.96 s real, 0.94 s user) and runs about as fast as the sequential
one.

Kāra took 1.23 times Rust's median time under overflow checks and 1.85
times C's. C keeps each grid in one block, where Kāra and Rust copy 50
rows of 50 per call.
