# 827. Making A Large Island

You are given an `n x n` binary matrix `grid`. You may change at most
one `0` to a `1`. Return the size of the largest island in `grid` after
that change. An island is a 4-directionally connected group of `1`s.

```
grid = [[1,0],[0,1]]  ->  3
grid = [[1,1],[1,0]]  ->  4
grid = [[1,1],[1,1]]  ->  4
```

**Constraints:** `n == grid.length == grid[i].length`, `1 <= n <= 500`,
`grid[i][j]` is `0` or `1`.

## Approaches

Every arm labels the islands once and records their sizes. A `0` turned
to a `1` joins it to the islands beside it, so the island it makes has 1
plus the sizes of the distinct labels among its four neighbours: an
island that touches the `0` on two sides is counted once. A grid with no
`0` is one island, the whole grid, and is the answer when nothing is
turned.

| file | mechanism |
|---|---|
| `largest_island.kara` ★ | a breadth-first search on a queue labels each island in a grid of labels and records its size; each `0` adds the sizes of the distinct labels around it, kept in a list of at most four. O(n^2) |
| `largest_island_dsu.kara` | union-find over the cells with path compression and union by size: every land cell joined to the land to its right and below, so each island is one set whose root holds its size; a `0` adds the sizes of the distinct roots around it. O(n^2 α(n^2)) |
| `largest_island_stack.kara` | the islands labelled 2, 3, ... in a copy of the grid itself, each by a depth-first search on an explicit stack, with a map from label to size. O(n^2) |
| `largest_island_iter.kara` | the ★ arm's labels, then a `max` over the `0` cells of 1 plus a `sum` over the distinct labels of the in-grid neighbours, gathered by `filter_map` into a `Set` |
| `differential.kara` | the four arms against the statement read cell by cell, four properties |

Every arm prints the same 13 lines: LeetCode's three examples; six small
grids (a single `0` and a single `1`; all water; a `0` ringed by land on
every side, joining one island to itself; four corner cells of a 3 by 3
grid, two of which a `0` on an edge joins; and four 2 by 2 islands with
a cross of water between them); three grids of LeetCode's largest size,
500 by 500, with land at random at 50% and 60%, and all water; and 300
random grids of up to 8 by 8, with a total and a checksum.
`largest_island.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: leave the grid as it is, or turn each `0` in turn to a `1`,
and measure every island of every grid that makes by a recursive flood
fill. Its 1,600 cases have grids of up to 7 by 7 and come in four kinds
of 400: land at 20% to 80%; mostly water, land at up to 20%; mostly
land, at 80% to 100%; and stripes and checks with one cell in ten
flipped, so that many islands lie one `0` apart.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the grid transposed gives the same answer |
| P3 | the grid mirrored left to right gives the same answer |
| P4 | one cell flipped: the answer does not fall when land is added, or rise when it is removed |

It prints `1600 cases, 25600 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an island beside the `0` on two sides counted twice | P1 791, P4 191 |
| M2 | ★: the grid with no `0` to turn left at 0 | P1 273, P4 393 |
| M3 | ★: the search never steps down | P1 963, P2 627, P4 131 |
| M4 | dsu: land joined only to its right | P1 870, P2 618, P4 189 |
| M5 | dsu: the size read at the neighbour, not at its root | P1 592, P2 351, P3 441, P4 9 |
| M6 | dsu: the turned cell itself not counted | P1 1327 |
| M7 | stack: the current cell marked instead of the one below it | P1 872, P2 492, P3 291, P4 8 |
| M8 | stack: the labels start at 1, the land's own value | never ends |
| M9 | stack: the neighbour to the left never looked at | P1 201, P2 192, P3 108 |
| M10 | iter: the labels gathered in a list, not a set | P1 791, P4 191 |
| M11 | iter: the answer with nothing turned dropped | P1 273, P4 393 |
| M12 | iter: the turned cell itself not counted | P1 1327 |

P1 kills eleven. M8 never ends and was stopped by the run's ten-minute
limit: a cell labelled 1 is still land, so two land cells side by side
push each other onto the stack for ever (a two-cell grid run alone hangs
too). M1 and M10, M2 and M11, and M6 and M12 are the same mistake in two
arms and fail the same cases. P2 and P3 see the edits that make an arm
depend on the direction it scans in: M3 and M4 lose the joins that run
one way, which transposing the grid turns into the other, and M5, M7 and
M9 differ under mirroring as well. P4 catches M2 and M11 more often than
P1 does: it fails when the grid is full, as P1 does, and also when the
flip fills it, since a full grid then scores 0.

## Verification

Every arm prints the same output as `largest_island.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release build
that runs `check` and `__mir-run` and the debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` are both at kara
`10d45bb347`, with the runtime archives built from that tree; the
mutation runs used the release build at `5cd642c474`.

Under `karac __mir-run` the ★, union-find and stack arms take 5 to 7 s
each and the iterator arm 26 s, with the same output.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy JIT (`karac run`), `karac build` and an auto-par build
print the same output for all four arms. The legacy interpreter (`karac
run --interp`) does not finish any arm within the lane's 60 s limit and
is still in the 500 by 500 grids when stopped, and does not finish the
differential either. `karac build` refuses the differential, whose `for
row in m.iter_mut()` it does not support, and its checker refuses the
bench program, which passes `grids[round % count]` to a bare parameter
and so, under legacy's rules, moves it out of an index. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 16
grids of 500 by 500, LeetCode's largest, with land at random at 55%,
just below the density at which one island spans the grid, once. Each of
200 rounds answers the next grid afresh: the labels, the sizes and the
queue are new each call. Every implementation prints `200 rounds of 16
grids: total 641207, checksum 681843343`, the Kāra program under `karac
__mir-run` included, in 362 s with the interpreter's step limit raised
by `KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, eight runs of each compiled
program and 13 of v2's, five of them interleaved, and three of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.13 to 2.31 s |
| Rust (`rustc -O`) | 3.24 to 3.51 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.25 to 3.52 s |
| Go | 3.95 to 4.19 s |
| Python | 44.6 to 48.7 s |
| Kāra (`karac build --mir`) | 3.88 to 4.25 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 3.94 s, against Rust's
3.40 (3.44 under overflow checks), C's 2.23 and Go's 4.03: 1.15 times
Rust's time under overflow checks, and 1.8 times C's. Under valgrind's
cachegrind v2 runs 18.7 billion instructions, against Rust's 13.6
billion and C's 4.2 billion. The programs differ in one place the
language forces: C keeps the labels seen around a `0` in a stack array
of four, where Rust, Go and Kāra push them onto a growable vector, which
allocates for each `0` beside land, and index every row through its own
bounds check. Most likely that is what puts the three behind C (not
traced). Built for `x86-64-v3`, the target `karac build` uses, C takes
2.24 to 2.49 s and Rust with overflow checks 3.38 to 3.73 s, against
v2's 3.97 to 4.24 s in the same five interleaved runs. Python takes 46
s, about 21 times C's time. The comparison with C and Rust waits until
after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench program run
on every v2 lane as written, and in the first spelling tried.
