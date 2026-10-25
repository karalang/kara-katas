# 1001. Grid Illumination

There is a 2D `grid` of size `n x n` where each cell of this grid has a
lamp that is initially **turned off**.

You are given a 2D array of lamp positions `lamps`, where
`lamps[i] = [rowi, coli]` indicates that the lamp at `grid[rowi][coli]`
is **turned on**. Even if the same lamp is listed more than once, it is
turned on.

When a lamp is turned on, it **illuminates its cell** and **all other
cells** in the same **row, column, or diagonal**.

You are also given another 2D array `queries`, where
`queries[j] = [rowj, colj]`. For the `jth` query, determine whether
`grid[rowj][colj]` is illuminated or not. After answering the `jth`
query, **turn off** the lamp at `grid[rowj][colj]` and its **8 adjacent
lamps** if they exist. A lamp is adjacent if its cell shares either a
side or corner with `grid[rowj][colj]`.

Return *an array of integers* `ans`*, where* `ans[j]` *should be* `1`
*if the cell in the* `jth` *query was illuminated, or* `0` *if the lamp
was not.*

```
n = 5, lamps = [[0,0],[4,4]], queries = [[1,1],[1,0]]        ->  [1,0]
n = 5, lamps = [[0,0],[4,4]], queries = [[1,1],[1,1]]        ->  [1,1]
n = 5, lamps = [[0,0],[0,4]], queries = [[0,4],[0,1],[1,4]]  ->  [1,1,0]
```

**Constraints:** `1 <= n <= 10^9`; `0 <= lamps.length <= 20000`;
`0 <= queries.length <= 20000`; `lamps[i].length == 2`;
`0 <= rowi, coli < n`; `queries[j].length == 2`; `0 <= rowj, colj < n`.

## Approaches

A cell is lit when a lamp that is on shares one of its four lines: its
row, its column, its diagonal, on which row less column is the same,
or its anti-diagonal, on which row plus column is. The grid is far too
large to hold, but only the lines that hold lamps matter, so every arm
but one counts the lamps on each line, and a query reads four counts
and then takes up to nine lamps off them. A lamp listed twice is one
lamp, and is counted once. The arms differ in where the counts are
kept.

| file | mechanism |
|---|---|
| `grid_illumination.kara` ★ | counts per line in four hash `Map`s, one each for rows, columns, diagonals and anti-diagonals, and a `Set` of the lamps that are on, keyed `r n + c`; a query reads the four counts, then turns off each lamp in the 3 by 3 block around it and takes it off all four. O(lamps + queries) |
| `grid_illumination_sorted.kara` | the same counts in `SortedMap`s and the lamps in a `SortedSet`; a line whose count falls to 0 leaves its map, so a cell is lit exactly when one of its four lines is a key. O((lamps + queries) log lamps) |
| `grid_illumination_brute.kara` | every lamp asked: the lamps sorted with repeats dropped and a flag each for on; a query asks every lamp still on whether it shares a line with the cell, then turns off every lamp within one step of it. O(queries × lamps) |
| `grid_illumination_lines.kara` | one `Map` for every line: the four kinds of line in four ranges of keys, `kind × 4·10⁹ + value + 2·10⁹`, and a second `Map` of how many times each lamp was listed, whose lines count it once. O(lamps + queries) |
| `grid_illumination_compress.kara` | no hashing: the distinct lamps in a sorted list with an on flag each, and the rows, columns, diagonals and anti-diagonals that hold lamps in four more sorted lists with a count beside each, found by binary search. O((lamps + queries) log lamps) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines. The first ten are LeetCode's three
examples and seven more: a grid of one cell, lit and then dark; no
lamps at all; a lamp listed twice, turned off once; a lamp lit along
its diagonal from the far corner and turned off by a query beside it;
two lamps on one anti-diagonal, the first turned off by a query both
light; three lamps all turned off by the
first query; and two lamps in opposite corners of LeetCode's largest
grid, `n` = 10⁹, lighting its middle along a diagonal. Then totals over
random grids, each with its lamps and queries in a random window of
the grid, so that they share lines: 300 grids of up to 6 by 6 with up
to 6 lamps and queries, 3,000 of up to 30 with up to 40, 300 of 10⁶ to
10⁹ with up to 200 in a window of up to 30, and two each of 50 by 50
and 10⁹ by 10⁹ with up to 2,000. `grid_illumination.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally, on the grid itself: every lamp turned on in its cell,
and for each query the cell lit when a lamp that is on shares its row,
its column, its diagonal or its anti-diagonal, then every lamp in the
cell and the eight around it turned off. It checks 3,200 random grids,
made as the arms' random grids are: 3,000 of up to 8 by 8 with up to
10 lamps and queries against the statement, and 200 of 1,000 to 10⁹
with up to 100, in a window of up to 30 by 30, against the other
properties.

| | property |
|---|---|
| P1 | the statement's answers, on the first 3,000 grids |
| P2 | the grid transposed gives the same answers |
| P3 | the grid mirrored left to right gives the same answers |
| P4 | every lamp listed twice gives the same answers |
| P5 | the first half of the queries give the first half of the answers |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 grids, 26246 queries: 12123 lit, checksum 440000926,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (34.1 s)
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Twenty-eight edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`: twenty-five first, then three
more for compress, which had fewer than three kept. Fifteen are kept,
three to each arm, all fifteen are killed, and each fails the same
checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a repeated lamp counted again | P1 1268, P4 953, P6 1369 |
| M2 | ★: the diagonal read at row plus column | P1 305, P2 107, P3 653, P6 405 |
| M3 | ★: the row above never turned off | P1 716, P2 990, P6 826 |
| M4 | sorted: a line at 0 left in its map | P1 1999, P6 2134 |
| M5 | sorted: the row below never turned off | P1 686, P2 975, P6 799 |
| M6 | sorted: the column read at the row | P1 519, P2 958, P3 477, P6 642 |
| M7 | brute: a band turned off, not a block | P1 1105, P6 1288 |
| M8 | brute: no diagonal | P1 319, P3 714, P6 419 |
| M9 | brute: only the lamp's own column turned off | P1 1227, P2 942, P6 1355 |
| M10 | lines: the kinds of line keyed `kind × 10 + value`, too close | P1 20, P2 34, P3 38, P6 20 |
| M11 | lines: a lamp turned off stays listed | P1 216, P6 329 |
| M12 | lines: the diagonal asked as column less row | P1 293, P3 557, P6 393 |
| M13 | compress: a line holds one lamp at most | P1 548, P6 702 |
| M14 | compress: the column to the right never turned off | P1 695, P2 975, P3 1234, P6 809 |
| M15 | compress: a line lit only by two lamps | P1 2074, P6 2239 |

P1 and P6 kill all fifteen, P2 seven, P3 six, P4 one and P5 none.
Transposing a grid swaps rows with columns and turns each diagonal's
row less column round, leaving the anti-diagonals as they are, so P2
sees the edits that treat a row unlike a column: M3 and M5, which
leave a row of the block lit, M9, which turns off one column of it,
M14, one column short, M6, which reads the column at the row, and
M10, whose row keys run into its column keys at an offset of 10; and
M2, which counts each diagonal at row less column and asks it at row
plus column, and so turns the other way. Mirroring left to right
swaps the diagonals with the anti-diagonals and the left of a block
with its right, so P3 sees M8, which drops the diagonals, M12, which
asks them the wrong way round, and M2 again; M14, short on the right;
and M6 and M10. M12 asks every diagonal as column less row, which
transposing turns back the right way, so P2 cannot see it, and M8
loses the diagonals of a grid and of its transpose alike. M7, a band
three rows and three columns wide turned off where a block should be,
is the same in every direction, as are M4, M11, M13 and M15, which
miscount a line however it lies; those five fail only P1 and P6.

P4 lists every lamp twice, so every lamp is a repeated one, and it
sees only M1, which counts a repeat on its lines again, so that
turning it off once leaves them lit. M11 leaves a lamp listed once it
is off, and a later query beside it takes it off its lines again,
which can darken a line another lamp still lights; listing it twice
changes neither. P5 kills none: every arm, and every edit, answers
each query from the lamps and the queries before it, so the first
half of the queries is answered alike alone. The checks draw no random
number that depends on an answer, so every mutant sees the same grids
and their counts can be compared: M4 leaves a line lit for good once a
lamp has been on it, and fails 1,999 small grids, M15 needs two lamps
on a line, and fails 2,074.

Thirteen other edits were tried and set aside. Six failed exactly the
same checks as a kept one: sorted and lines counting a repeated lamp
again, and compress not dropping repeats, as M1; brute letting a lamp
that is off still light, and lines putting a lamp back on its lines
when it is turned off, which both leave a line lit for good, as M4;
and compress turning a lamp off a second time, as M11. Three were
sound but beyond three an arm: ★ not ruling out column -1, which is
the key of the last cell of the row above, and never lowering a row's
count; and sorted never turning off the column to the left. One
survived and is equivalent: brute keeping repeated lamps, whose copies
light together and are turned off together.

Three crashed with an index out of bounds, exit 101, at the same line
in both lanes, all in compress, whose binary search answers -1 for a
value it does not find, which every edit then uses as an index. Not
ruling out column -1 turns off the last lamp of the row above, if
there is one, and looks for column -1 among the columns; listing the
diagonals as row plus column leaves a lamp's own diagonal out of the
list it is counted in; and a missing value answered with its
neighbour's place turns off a lamp that is not there and looks up
lines no lamp is on, one of them past the end of its list. The bounds
check stops each one before any property is asked, so none is kept.

## Verification

Every arm prints the same output as `grid_illumination.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error;
the differential prints its line under all three. `karac check` passes
all five arms, the differential and the bench program. `karac run` and
a `karac build --mir` binary print the same output for every arm and
the differential. The release build is at kara `395f71ae05`, the
runtime archives rebuilt at `d867340a02`, whose runtime sources are
the same. Under `karac __mir-run` the arms take 2.5 s (★) to 10.7 s
(brute, which asks every lamp at every query), and the differential
34.1 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
grids of LeetCode's largest size, 10⁹ by 10⁹, once, each with
LeetCode's most lamps, 20,000, at random in a window of 100,000 by
100,000 cells at a random place in the grid, and 20,000 queries: the
even ones anywhere in the window and the odd ones on or beside a
random lamp. It runs the arm once on every grid and folds every answer
into a checksum. Every implementation prints `1 rounds over 20 grids
of 20000 lamps and 20000 queries: 253552 lit, checksum 950751119`.
Each call builds a fresh set of the lamps and four maps of counts:
`Set` and `Map` in Kāra, `HashSet` and `HashMap` in Rust, a `set` and
`dict`s in Python, built-in maps in Go, and in C a hand-written table
with linear probing and a multiplicative hash, whose entries keep
their slot when they fall to 0.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.191 to 0.285 s | 0.213 s |
| Rust (`rustc -O`) | 0.345 to 0.613 s | 0.404 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.351 to 0.603 s | 0.423 s |
| Go | 0.578 to 0.720 s | 0.642 s |
| Python | 5.2 s | |
| Kāra (`karac build --mir`) | 0.749 to 1.048 s | 0.878 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 6 times
Kāra's.

v2 took 2.08 times Rust's median time under overflow checks and 4.12
times C's. Under valgrind's cachegrind v2 ran 2,064 million
instructions and 293 million branches with 8.5 million mispredicted,
Rust with overflow checks 1,804 million, 148 million and 4.6 million,
and C 198 million, 33 million and 5.8 million. v2 spends 819 million
instructions in `karac_hash_word`, over 8.8 million calls, 93 a hash;
Rust's SipHash, the same function, is inlined into its map code. Both
spend about 320 million in glibc's allocator, and v2 126 million in
`memcpy` to Rust's 21 million. The cost of the hash call is the one
open rows B-2026-10-02-39 and B-2026-10-24-6 measured on katas 325
and 340, and inlining it is a lever the second names. v2 runs only
1.14 times Rust's instructions and takes twice its time; its extra
mispredicts and copies may be part of that, which was not traced. C's
table hashes with one multiply and holds its keys in one flat array,
and runs a ninth of Rust's instructions.
