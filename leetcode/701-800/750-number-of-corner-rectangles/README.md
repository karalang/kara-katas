# 750. Number Of Corner Rectangles

`grid` is an m x n grid of 0s and 1s. A corner rectangle is four
distinct 1s on the grid that form an axis-aligned rectangle; only the
corners need to be 1. Return the number of corner rectangles.

```
grid = [[1,0,0,1,0],[0,0,1,0,1],[0,0,0,1,0],[1,0,1,0,1]]  ->  1
grid = [[1,1,1],[1,1,1],[1,1,1]]                          ->  9
grid = [[1,1,1,1]]                                        ->  0
```

**Constraints:** 1 <= m, n <= 200; every cell is 0 or 1; at most
6,000 cells are 1.

## Approaches

A rectangle is fixed by two rows and two columns, so every arm counts,
for pairs of rows or pairs of columns, how often the other pair repeats,
and adds k(k - 1) / 2 for a pair that recurs k times.

| file | mechanism |
|---|---|
| `count_corner_rectangles.kara` ★ | for each pair of rows, count the k columns where both have a 1 and add k(k - 1) / 2; O(m^2 x n) |
| `count_corner_rectangles_colpairs.kara` | walk the rows keeping, in an n x n table, how many earlier rows have a 1 in both of each pair of columns; each pair of 1s in a row adds that count, then raises it |
| `count_corner_rectangles_bits.kara` | the ★ arm with each row packed into 64-bit words, so that `&` and `count_ones` give k a word at a time |
| `count_corner_rectangles_map.kara` | the column-pairs count kept in a `Map[(i64, i64), i64]` of the pairs that occur, turned into rectangles at the end |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 14 lines: the three LeetCode examples; a
single column of 1s, a single 0, a 2 x 2 of 1s, a checkerboard and two
separate 2 x 2 blocks; a 50 x 50 grid of 1s; random grids of 200 x
200 with 5% of their cells 1, 100 x 100 with 50%, and 30 x 200 and 200 x
30 with 70%; and 300 random grids of up to 8 x 8, with the total of
their rectangles and a checksum. `count_corner_rectangles.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every two rows and every two columns and counts the choices
whose four corners are 1. 3,000 random grids are checked, each of 1 to
7 rows of 1 to 7 cells, every cell 1 with a chance of 20 to 90 in
100; they hold 33,088 rectangles in all.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the grid transposed gives the same answer |
| P3 | a row of 0s put in at a random place gives the same answer |
| P4 | the first row added again at the end gives the answer, plus the answer less the answer without the first row (the rectangles the first row makes with the others, now made again by its copy), plus one for each pair of the first row's 1s |

It prints `3000 grids (33088 rectangles in all), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a row paired with itself | P1 2245, P2 2372 |
| M2 | ★: k squared over two, not k choose two | P1 1463, P2 899, P4 1770 |
| M3 | ★: a column counted when either row has a 1 | P1 2011, P2 1645, P3 2245 |
| M4 | colpairs: this row counted before it is looked up | P1 2245, P2 2372 |
| M5 | colpairs: a column paired with itself | P1 2231, P2 2372, P4 2562 |
| M6 | colpairs: the last column never listed | P1 1187, P2 1205, P4 1227 |
| M7 | bits: the zeros counted, not the ones | P1 2554, P2 2779, P3 3000, P4 3000 |
| M8 | bits: the first word skipped | P1 1463, P4 1770 |
| M9 | bits: neighbouring rows never paired | P1 1271, P2 1185, P3 540, P4 955 |
| M10 | map: every count left at one | P1 1463, P4 1770 |
| M11 | map: k - 1 rectangles for a pair seen k times | P1 896, P2 963, P4 1218 |
| M12 | map: the first column paired with itself | P1 1640, P2 2030, P4 1144 |
| E1 | ★: k choose two written another way | 0 |
| E2 | colpairs: one more unused count | 0 |
| E3 | bits: a spare word for a width of 64 | 0 |

P1 kills all twelve. M1 and M4 fail exactly the same checks, since
pairing a row with itself and counting a row before looking it up both
add, for every row, one rectangle for each pair of its own 1s. M8 and
M10 both count nothing at all, so they fail on exactly the 1,463 grids
that hold a rectangle; M2 fails P1 on those same grids, since k squared
over two differs from k(k - 1) / 2 only once some pair recurs. P2 sees
most edits, since every arm treats rows and columns differently, so an
error that depends on one of them changes under transposition. P3 sees
only the edits that make a row of 0s matter: M3, which counts a column
where either row has a 1; M7, which counts 0s; and M9, which skips
neighbouring rows, so that the new row changes which rows are
neighbours. P4 misses M1, M3 and M4. The extra self-pairs of M1 and
M4 cancel out of its sum, and M3 happens to keep the relation as well.
E1 writes k(k - 1) / 2 another way; E2 adds a count that is never read;
E3 adds a word that is always 0 for a width of 64.

## Verification

Every arm prints the same output as `count_corner_rectangles.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`1a5c083e3a`, whose last compiler change is `4655692faa`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★, colpairs and bits arms and the
bench program: each of those arms prints the same output under the
legacy interpreter, `karac run`, `karac build` and an auto-par build.
They refuse the map arm and the differential at type checking, at a `*`
over a map's `iter()` (`*k` over the counts), since legacy gives those
by value where v2 gives references. Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes a 200 x
200 grid with each cell 1 or 0 at even odds once (about 20,000 1s, more
than the 6,000 LeetCode allows, to give the count more work), and in
each of 100 rounds draws 50 random cells afresh and counts the
rectangles. Every implementation prints `100 grids of 200 x
200: 2430432898 rectangles in all, checksum 253276430`, the Kāra program
under `karac __mir-run` included (in 85 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.27 to 0.30 s |
| Rust (`rustc -O`) | 0.29 to 0.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.80 to 2.89 s |
| Go | 2.80 to 2.93 s |
| Python | 12.5 to 12.7 s |
| Kāra (`karac build --mir`) | 2.66 to 2.97 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
5.7 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 2.86 s,
level with Rust under overflow checks (2.83) and with Go (2.83), and ten
times C (0.29) and Rust without overflow checks (0.31). The slow
programs do not run many more instructions: under valgrind's cachegrind
v2 runs 5.0 billion and Rust 4.8 billion, against C's 2.4. The likely
difference is branches. The inner test, `grid[a][c] == 1 and grid[b][c]
== 1` on random cells, goes either way at even odds; C and unchecked
Rust can count it without a branch, where a checked `k += 1` keeps one
that the processor then mispredicts about half the time (inferred from
the times and counts, not read from the generated code). That is the
equal-safety tie BENCHMARKS.md describes: Kāra checks integer overflow
by default, and against Rust with overflow checks on it is level. The
legacy build of the same program ran 2.74 to 3.02 s, a median of 2.86 s
in the interleaved runs, so v2 takes as long as legacy, inside M2's
limit of twice legacy; new katas' benches are outside M2's frozen set in
any case. The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
