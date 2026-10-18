# 694. Number of Distinct Islands

You are given an m x n binary grid. An island is a group of 1's (land)
connected four-directionally (horizontally or vertically), and all four
edges of the grid are surrounded by water. Two islands are the same if
one can be translated (not rotated or reflected) to equal the other.
Return the number of distinct islands.

```
11000
11000
00011
00011   ->  1

11011
10000
00001
11011   ->  3
```

**Constraints:** 1 <= m, n <= 50; each cell is 0 or 1.

## Approaches

Every arm is `fn num_distinct_islands(grid: Vec[Vec[i64]]) -> i64`.

| file | mechanism |
|---|---|
| `num_distinct_islands.kara` ★ | a recursive depth-first search from each island's first cell in reading order, writing each step's direction and a mark each time it backs out of a cell; equal shapes give equal paths, and a `Set[String]` counts them; O(m n) |
| `num_distinct_islands_bfs.kara` | a breadth-first search collecting each cell's offset from the island's first cell, packed as 200 times the row offset plus the column offset; sorted, the offsets are the shape, and a `Set[Vec[i64]]` counts them; O(m n log(m n)) |
| `num_distinct_islands_unionfind.kara` | no hashing: union-find joins land neighbours, a pass in reading order lists each island's offsets already sorted, and the shapes are sorted and equal neighbours counted once; O(m n log(m n)) |
| `num_distinct_islands_picture.kara` | each island, found with an explicit stack, drawn in its bounding box as rows of `#` and `.` separated by `/`; a new drawing is looked up in the list of drawings so far; O(m n + k^2 s) for k islands of at most s cells |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 5 lines: the two LeetCode examples; a single
cell of water, a 50 by 50 grid of land and a 50 by 50 checkerboard; an L
beside its mirror image, an L beside itself turned, and three copies of
one L; and 200 random grids of up to 50 by 50 with 10 to 70 percent
land, the counts summed and put into a checksum.
`num_distinct_islands.py` mirrors the ★ arm and its output is
byte-identical. The sets are only counted, never walked, so no output
depends on their order.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: every land cell is
labelled with its own number, and each label is lowered to the least of
its land neighbours' until nothing changes, so each island ends with one
label. Two islands have the same shape when they have as many cells and
moving every cell of one by the step between their first cells lands on
a cell of the other; the answer counts the islands unlike every island
before them. 4,000 random grids of 1 to 12 by 1 to 12 are checked, with
20 to 70 percent land.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | a row of water added above and a column to the left change nothing |
| P3 | the mirror image, each row reversed, has as many distinct shapes |
| P4 | the grid twice side by side, water between, adds no new shape |

It prints `4000 grids, 4 arms, 64000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`. `karac check` refuses it, wrongly; see Compiler
findings.

## Mutation testing

Thirteen edits to the differential, each run under `karac __mir-run`:
twelve that change answers, four to the ★ arm, two to the breadth-first
arm and three to each of the others, and one that does not. All twelve
are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no mark for backing out of a cell | P1 42, P3 71 |
| M2 | ★: a step up written as a step down | P1 6, P3 7 |
| M3 | ★: every step written alike | P1 666, P3 243 |
| M4 | bfs: a column offset taken without its sign | P1 46, P3 8 |
| M5 | bfs: no step to the left | P1 1342, P3 1521 |
| M6 | unionfind: shapes told apart by size alone | P1 416, P3 226 |
| M7 | unionfind: the shapes left unsorted | P1 1590, P3 807, P4 2097 |
| M8 | unionfind: left and right neighbours never joined | P1 2530 |
| M9 | picture: rows not separated | P1 489, P3 6 |
| M10 | picture: a known drawing never found | P1 2373, P4 3909 |
| M11 | picture: only the bounding box drawn | P1 363 |
| M12 | ★: no step to the left | P1 1342, P3 1521 |
| E1 | bfs: the offsets left unsorted | 0 |

The three weakest kills are the ones the path arm is famous for:
dropping the back-out mark (M1), writing up as down (M2), and an offset
without its sign (M4) make two shapes collide only for particular pairs
of islands in one grid. With 1,000 grids of up to 10 by 10 they were
killed by 7, 1 and 3 failures, so the differential was raised to
4,000 grids of up to 12 by 12. P2 kills nothing, since every arm
measures from an island's own first cell and never from the grid's edge.
P3 catches most of them a second time, since the mirror image changes
which islands collide, and P4 only those whose count depends on how many
islands there are, not how many shapes. E1 is equivalent: a
breadth-first search from the first cell, trying its neighbours in a
fixed order, visits two islands of one shape in the same order, so their
unsorted offsets are already equal.

## Verification

Every arm prints the same output as `num_distinct_islands.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms and
the bench program; it refuses the differential, as B-2026-10-18-7 below
records. All with the compiler at kara `de50d67b07` for both the debug
build and the release build that runs `check` and `__mir-run`, with
runtime archives rebuilt after the last `runtime/src` change.

The frozen legacy backends refuse all four arms and the differential at
type checking: at `*b` over `row.bytes().iter()` in the harness, at `*r`
and `*c` over a destructured `(r, c)` from `cells.iter()`, since legacy
gives those items by value where v2 gives references, and at
`next_random(mut seed)` inside `random_grid`, whose `seed` is already a
`mut ref`: legacy wants the marker dropped, while on v2 the marked
forward is the spelling (kara B-2026-10-14-25). They build the bench
program as it is. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the union-find arm, the one that is the same
algorithm in all five languages; C has no set. It builds 40 grids of
50 by 50 once, with 30 to 60 percent land, then counts each grid's
distinct islands in each of 150 rounds, putting each count into a
checksum. Every implementation prints `150 rounds of 40 grids of 50 by
50: 389550 distinct islands counted, checksum 57554751`, the Kāra
program under `karac __mir-run` included (in 28 s).

Each implementation allocates its union-find array, its two tables of
first cells and its list of shapes afresh for each grid; C grows each
shape with `realloc` and sorts them with `qsort` and a comparison that
orders like `Vec[i64]`. Spot timings on a shared 4-core container, eight
runs of each compiled program, five of them interleaved, and two of
Python (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.42 to 0.57 s |
| Rust (`rustc -O`) | 0.45 to 0.52 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.45 to 0.56 s |
| Go | 0.73 to 0.80 s |
| Python | 4.8 to 5.0 s |
| Kāra (`karac build --mir`) | 0.49 to 0.64 s |
| Kāra, legacy (`karac build`) | 0.43 to 0.55 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` builds the same file, and
its row is above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 2.0 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is a little behind legacy, C and Rust here, about
1.1 times, and ahead of Go. The comparison with C and Rust waits until
after M4.

## Compiler findings

kara **B-2026-10-18-7** (open): `karac check` refuses the differential
with "value 'p' moved here, used again here" at its last loop, `for p in
0..4 { ... f"P{p + 1}: {fails[p]} failures | " ... }`, the report loop
every kata differential ends with. Earlier in the same `main`, each
grid's padded copy is built from a row named `p`, a `Vec[i64]`, in an
inner loop that has long ended; the loop's `p` then seems to be taken
for that `Vec`, so `p + 1` counts as a move. A five-line program with
nothing else in it shows the same, and `karac __mir-run` runs it
correctly. The differential keeps its natural spelling until the fix;
nothing in the kata works around it.
