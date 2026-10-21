# 836. Rectangle Overlap

An axis-aligned rectangle is given as a list `[x1, y1, x2, y2]`, where
`(x1, y1)` is its bottom-left corner and `(x2, y2)` its top-right
corner; its top and bottom edges are parallel to the x axis and its left
and right edges to the y axis. Two rectangles overlap if the area of
their intersection is positive; two that only touch at a corner or along
an edge do not overlap. Given two rectangles `rec1` and `rec2`, return
`true` if they overlap, otherwise `false`.

```
rec1 = [0,0,2,2], rec2 = [1,1,3,3]  ->  true
rec1 = [0,0,1,1], rec2 = [1,0,2,1]  ->  false
rec1 = [0,0,1,1], rec2 = [2,2,3,3]  ->  false
```

**Constraints:** `rec1.length == rec2.length == 4`, `-10^9 <= rec1[i],
rec2[i] <= 10^9`, and each rectangle has a positive area.

## Approaches

Every arm reads the two rectangles as their spans on the two axes; a
pair of spans overlaps in more than a point when each starts before the
other ends.

| file | mechanism |
|---|---|
| `is_rectangle_overlap.kara` ★ | the two projections: the overlap's left edge is the larger left edge and its right edge the smaller right edge, likewise bottom and top, and the rectangles overlap when left is below right and bottom below top. O(1) |
| `is_rectangle_overlap_apart.kara` | the four ways to be apart: the rectangles fail to overlap exactly when one lies wholly left of, right of, below or above the other, touching allowed, and overlap when none holds. O(1) |
| `is_rectangle_overlap_area.kara` | the area of the intersection: its width and height clamped at zero and multiplied, positive when the rectangles overlap. Coordinates within 10^9 in size keep the product below 4 * 10^18. O(1) |
| `is_rectangle_overlap_intervals.kara` | intervals as a struct: each rectangle a pair of `Interval`s with an `overlaps` method, and the rectangles overlap when both pairs do. O(1) |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 14 lines: LeetCode's three examples; nine more
(one rectangle inside the other both ways round, a cross whose corners
lie outside each other, a shared corner, a shared edge above and one
below, two identical rectangles, and two of LeetCode's greatest size,
one overlapping a corner square of the other and one sharing the edge `x
= 0` with it); and two runs of 3,000 random pairs, one with corners near
the origin and short sides, so that touching and overlapping are both
common, and one across LeetCode's whole range, each with its count of
overlapping pairs and a checksum. `is_rectangle_overlap.py` mirrors the
★ arm and its output is byte-identical.

The bench and the random pairs draw their large coordinates from two or
three draws of the 15-bit generator, since one draw stops at 32,767.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the area of the intersection, worked out without any reading
of spans. The four x and four y coordinates of the two rectangles cut
the plane into cells, each wholly inside or wholly outside each
rectangle, and the area is the sum of the areas of the cells inside
both. Its 1,600 cases come in four kinds of 400: small rectangles near
the origin; a rectangle and a copy of it moved by at most its own width
and height, so the two often share just an edge or a corner; rectangles
anywhere in LeetCode's range, up to its corners; and a rectangle against
one whose span on each axis lies inside, around or past its own, which
builds crosses and nestings. 548 of the cases overlap.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the two rectangles swapped give the same answer |
| P3 | both mirrored left to right give the same answer |
| P4 | both transposed, x and y exchanged, give the same answer |
| P5 | both turned half a turn about the origin give the same answer |

It prints `1600 cases, 548 overlapping, 32000 checks over 4 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: x shadows that only touch counted as overlapping | P1 205, P4 411 |
| M2 | ★: the overlap's left edge taken as the smaller left edge | P1 350, P4 720 |
| M3 | ★: the overlap's top read from the second rectangle's right edge | P1 235, P2 262, P3 366, P4 455, P5 530 |
| M4 | apart: touching on the left not counted as apart | P1 140, P2 205, P3 205, P4 273, P5 205 |
| M5 | apart: lying above not tested | P1 147, P2 370, P4 276, P5 370 |
| M6 | apart: below compared top to top | P1 366, P2 443, P4 250, P5 249 |
| M7 | area: a negative width or height not clamped at zero | P1 151 |
| M8 | area: width plus height, not times | P1 720 |
| M9 | area: the overlap's bottom taken as the lower bottom | P1 370, P4 720 |
| M10 | intervals: only one end compared | P1 557, P2 912, P3 535, P5 912 |
| M11 | intervals: the y interval ending at the x end | P1 349, P3 454, P4 683, P5 597 |
| M12 | intervals: each x interval compared with the other's y interval | P1 475, P3 515 |

P1 kills all twelve. M7 and M8 keep every symmetry of the problem and
only P1 sees them: both answer wrongly on whole classes of pairs, M8 on
every pair whose spans miss on one axis only and M7 on every pair whose
spans miss on both. P4, x and y exchanged, sees every edit that treats
one axis differently from the other (M1 to M6, M9, M11). It misses M10,
which compares one end the same way on both axes, and M12, which pairs
each rectangle's x interval with the other's y interval; transposing
both rectangles only swaps which pairing is wrong. P3, the mirror, sees
M12, and P2 sees the edits that treat the two rectangles differently (M3
to M6, M10).

M7 was first tried with only the width left unclamped. That is an
equivalent mutant: a negative width times a height clamped at zero is
never positive, so the answer never changes, and it survived every case.
Leaving both unclamped makes two spans that both miss multiply to a
positive area.

## Verification

Every arm prints the same output as `is_rectangle_overlap.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `7bb6d4db03`, and the runtime archives are
current with them. Under `karac __mir-run` each arm takes 0.2 to 0.3 s
and the differential 0.4 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run this kata: `karac run --interp`, `karac
run`, `karac build` and an auto-parallel build print the same output for
all four arms and the differential. Legacy `karac build` refuses the
bench program as moving a rectangle out of `rects[i]`, which v2's
borrowing parameters do not do. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 4,096
rectangles once in LeetCode's range, their corners anywhere and the
sides of rectangle `k` up to `2 * 10^9 >> (k % 8)`, so they run from the
size of the range down to a 128th of it. Round `s` of 100,000 tests each
rectangle `i` against rectangle `(i + s + 1) % 4096`, 409.6 million
tests in all, about 5% of them overlapping. Every implementation prints
`100000 rounds of 4096 pairs: 22213354 overlapping, checksum 545005043`,
the Kāra program under `karac __mir-run` included, in 880 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.81 to 0.94 s |
| Rust (`rustc -O`) | 1.21 to 1.77 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.24 to 2.55 s |
| Go | 2.57 to 3.20 s |
| Python | 220 to 236 s |
| Kāra (`karac build --mir`) | 2.58 to 3.05 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 2.83 s, against C's
0.88, Rust's 1.37 (2.51 under overflow checks) and Go's 2.84: 1.13 times
Rust's time under overflow checks, 3.2 times C's and about Go's. Under
valgrind's cachegrind C runs 12.3 billion instructions and 0.41 billion
branches, one a test, Rust 19.7 and 2.87 billion and v2 18.1 and 3.30
billion. v2 is the only one of the three to mispredict: 23.8 million
branches against about 0.1 million, most likely because it branches on
the second half of the `and` where C and Rust compute both comparisons
and branch once (not traced). Those cost perhaps a tenth of a second;
the rest of the gap to C is the round's index `(i + s + 1) % n` and the
two lists read through their headers on every test, which Rust pays too
and C, reading a flat array, does not (not traced). Built for
`x86-64-v3`, the target `karac build` uses, C takes 0.60 to 0.65 s and
Rust with overflow checks 2.54 to 2.81 s, against v2's 2.62 to 3.12 s in
the same five interleaved runs. Python takes about 230 s, about 260
times C's time. The comparison with C and Rust waits until after M4.

## Compiler findings

None on v2: every arm, the differential and the bench program pass
`karac check` and run on both v2 backends as written. The struct arm
first named its type `Span`, which `karac check` warns shadows a type of
that name in the prelude; it is named `Interval` instead.
