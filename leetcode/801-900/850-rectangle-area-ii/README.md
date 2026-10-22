# 850. Rectangle Area II

You are given axis-aligned rectangles, `rectangles[i] = [x1, y1, x2,
y2]` with `(x1, y1)` the bottom-left corner and `(x2, y2)` the top-right
one. Return the total area of the plane they cover, counting area
covered by two or more rectangles once, modulo `10^9 + 7`.

```
rectangles = [[0,0,2,2],[1,0,2,3],[1,0,3,1]]  ->  6
rectangles = [[0,0,1000000000,1000000000]]    ->  49   (10^18 mod 10^9 + 7)
```

**Constraints:** `1 <= rectangles.length <= 200`, every coordinate is
between 0 and `10^9`, `x1 <= x2` and `y1 <= y2`, so a rectangle can have
no area.

## Approaches

| file | mechanism |
|---|---|
| `rectangle_area.kara` ★ | compressed coordinates and a grid of cells: the rectangles' edges lie on at most `2n` distinct x values and `2n` distinct y values, which cut the plane into cells that each rectangle covers whole or misses; mark the cells each rectangle covers and add up the marked cells' areas. The union is at most 10^18, which an `i64` holds, so the remainder is taken once at the end. O(n^3) time, O(n^2) space |
| `rectangle_area_sweep.kara` | a sweep line with merged intervals: each rectangle opens at its left edge and closes at its right one, opening first where the two coincide; the area between two edges is their distance times the length of y covered by the rectangles open there, found by sorting the open intervals and merging those that overlap. O(n^2 log n) time |
| `rectangle_area_strips.kara` | one strip between neighbouring x values at a time: the rectangles covering a strip all span it from side to side, so its area is its width times the length of their y intervals put together, gathered with `filter` and `map`, sorted and merged. O(n^2 log n) time |
| `rectangle_area_segtree.kara` | a sweep line over a segment tree on the compressed y values: each node counts the open rectangles covering its whole range and keeps the covered length of its range, all of it when its count is positive and its children's otherwise, so opening or closing a rectangle touches O(log n) nodes. O(n log n) time |
| `differential.kara` | the four arms against the statement read literally on a small board, six properties |

Every arm prints the same 17 lines: LeetCode's two examples; nine more
(a unit square, a rectangle of no width beside one of no height, two
copies of one square, a square inside another, three unit squares
meeting at edges and a corner, a cross, a chain of three overlapping
squares, two strips of width 1 across the whole board meeting at its
corner, and two copies of the whole board); three sets of LeetCode's
most rectangles, 200: nested squares, rectangles apart in a grid, and
100 tall strips across 100 wide ones; 200 random rectangles with corners
up to 10^9 and 200 up to 60; and 300 random sets of up to eight
rectangles on boards up to 12 wide, with the sum of their areas and a
checksum. `rectangle_area.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally on a 12 by 12 board: a unit cell is covered when some
rectangle has `x1 <= x < x2` and `y1 <= y < y2`, and the area is the
number of covered cells. Its 1,600 cases come in four kinds of 400: one
to four rectangles anywhere; five to ten, so most cells are covered more
than once; one to six thin ones, one or two cells wide or of no width at
all; and a rectangle twice over with up to four more, most of them
sharing an edge with it. Their areas sum to 70,897.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the rectangles in reverse order give the same area |
| P3 | every rectangle turned a quarter about the board's centre gives the same area |
| P4 | every rectangle moved by the same random distance, up to `10^9 - 12` along each axis, gives the same area |
| P5 | one more rectangle never makes the area smaller |
| P6 | the area lies between the largest rectangle's area and the sum of all their areas |

It prints `1600 cases, areas sum to 70897, 38400 checks over 4 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a rectangle's last column of cells left out | P1 1533, P3 1225, P6 1061 |
| M2 | ★: every cell as wide as the first column | P1 1193, P3 1316, P5 223, P6 670 |
| M3 | ★: the top row of cells left out | P1 1322, P3 1233, P6 475 |
| M4 | sweep: overlapping intervals counted twice | P1 560, P3 597, P5 3 |
| M5 | sweep: an interval inside another counted as well | P1 479, P3 592, P5 85, P6 91 |
| M6 | sweep: a closing edge removing the first open interval with its bottom | P1 213, P3 417, P5 30, P6 55 |
| M7 | strips: a rectangle starting at the strip's left side left out | P1 1533, P3 1227, P6 1056 |
| M8 | strips: the gap between intervals counted | P1 567, P3 858, P6 308 |
| M9 | strips: the last strip left out | P1 1372, P3 1234, P6 529 |
| M10 | segtree: a leaf keeping its length once uncovered | P1 936, P3 1095, P5 77, P6 458 |
| M11 | segtree: a closing edge adding a rectangle again | P1 1234, P3 1245, P6 752 |
| M12 | segtree: a covered node one value short | P1 1533, P3 1190, P5 149, P6 1347 |

P1 kills all twelve, and P3 does too: turning the board swaps x and y,
so an edit that treats the two axes differently, as every one of these
does, gives a different area for most turned sets. P2 and P4 kill
nothing, and could not: every arm sorts its edges first, so the order of
the rectangles never reaches it, and every arm works from the
differences between coordinates, so a shift changes nothing. They stay
as guards against an arm that read the input in order or measured from
zero. P6 sees every edit but M4, whose double count can never pass the
sum of the areas, and P5 sees six (M2, M4, M5, M6, M10, M12), those
whose area can fall when a rectangle is added.

## Verification

Every arm prints the same output as `rectangle_area.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `b28f8bf975`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 0.3 to 2.5 s
and the differential 6.6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run the arms right with one exception: `karac
run`, `karac build` and a `KARAC_AUTO_PAR=1` build print the same output
for all four, and `karac run --interp` does for the sweep, strips and
segment-tree arms, but on the ★ arm it passes the 60 s limit after
printing its first lines right, as its grid holds up to 160,000 cells
for each set of 200 rectangles. `karac run --interp` and `karac build`
print the differential's `0 failures`. Legacy refuses the bench program
as moving a set out of an index, which v2's borrowing parameters do not
do. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the segment-tree arm in all five languages, since
the ★ arm's grid makes O(n^3) work of LeetCode's largest input. It draws
64 sets once, each of LeetCode's most rectangles, 200, with corners up
to 10^9: set `g` keeps its corners within `10^9 >> (g % 8)`, from the
whole board down to a corner of it, so the later sets overlap more. Each
of 8,000 rounds asks the next set. Every implementation prints `8000
rounds of 64 sets: areas sum to 4463457701000, checksum 258138411`, the
Kāra program under `karac __mir-run` included, in 369 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.58 to 1.80 s |
| Rust (`rustc -O`) | 1.12 to 1.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.09 to 1.37 s |
| Go | 1.63 to 1.84 s |
| Python | 16.8 to 17.2 s |
| Kāra (`karac build --mir`) | 1.33 to 1.69 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.43 s, against Rust's
1.22 (1.15 under overflow checks), C's 1.74 and Go's 1.74: 1.24 times
Rust's time under overflow checks, 0.82 times C's and 0.82 times Go's.
Under valgrind's cachegrind v2 runs the most instructions, 9.32 billion
against C's 7.04 billion and Rust's 6.97 billion, and the most branches,
1.75 billion against 1.07 and 0.94 billion, 123 million of them indirect
against C's 80 million and Rust's 0.9 million; it mispredicts 99
million, between Rust's 84 million and C's 131 million. C's indirect
branches are `qsort`'s calls to its comparators, and v2's are most
likely its sorts' comparisons too (not traced). Built for `x86-64-v3`,
the target `karac build` uses, C takes 1.53 to 1.67 s and Rust with
overflow checks 1.15 to 1.18 s, against v2's 1.39 to 1.50 s in the same
five interleaved runs. Python takes 16.9 s, about 10 times C's time. The
comparison with C and Rust waits until after M4.
