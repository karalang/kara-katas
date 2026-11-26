# 1401. Circle and Rectangle Overlapping

You are given a circle represented as `(radius, xCenter, yCenter)` and
an axis-aligned rectangle represented as `(x1, y1, x2, y2)`, where `(x1,
y1)` are the coordinates of the bottom-left corner, and `(x2, y2)` are
the coordinates of the top-right corner of the rectangle.

Return `true` if the circle and rectangle are overlapped otherwise
return `false`. In other words, check if there is any point `(xi, yi)`
that belongs to the circle and the rectangle at the same time.

```
radius = 1, center (0, 0), rectangle (1, -1) to (3, 1)    ->  true    they share (1, 0)
radius = 1, center (1, 1), rectangle (1, -3) to (2, -1)   ->  false
radius = 1, center (0, 0), rectangle (-1, 0) to (0, 1)    ->  true
```

**Constraints:** `1 <= radius <= 2000`, `-10^4 <= xCenter, yCenter <=
10^4`, `-10^4 <= x1 < x2 <= 10^4`, `-10^4 <= y1 < y2 <= 10^4`.

Each arm is `fn check_overlap(radius: i32, x_center: i32, y_center: i32,
x1: i32, y1: i32, x2: i32, y2: i32) -> bool`. A squared distance is at
most 2 * (2 * 10^4)^2 = 8 * 10^8, inside `i32`.

## Approaches

| file | mechanism |
|---|---|
| `check_overlap.kara` ★ | the rectangle's point nearest the center is the center clamped into the rectangle along each axis, by `clamp`, and the two overlap exactly when that point is within the radius, compared squared in integers. O(1) |
| `check_overlap_regions.kara` | the center against the rectangle grown by the radius, a rounded rectangle: inside the rectangle widened by the radius left and right, or heightened by it above and below, or within the radius of one of the four corners, asked by `any(..)` over an array of corner tuples. O(1) |
| `check_overlap_columns.kara` | column by column: the corners are whole numbers, so the rectangle's point nearest the center is a lattice point, and each whole x the rectangle and the circle share is tried, the circle there reaching `isqrt(r^2 - dx^2)` above and below the center. O(min(r, x2 - x1)) |
| `check_overlap_float.kara` | the distance in floating point: the center's gap to the rectangle along each axis, zero within that side's span, the two gaps joined by `hypot` and compared with the radius. O(1) |
| `check_overlap_solution.kara` | a Rust solution as LeetCode's Rust users write it (the nearest point by `i32::max(x1, i32::min(x_center, x2))`, and the squared distance against the squared radius), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and three
more, the circle inside the rectangle, reaching a corner and falling
short of it (`true false true true true false`); every center from -10
to 10 each way around the rectangle [-3, 2] x [-1, 4] for radii 1 to 6,
the number that overlap (`grid of 441 centers: 60 88 124 164 216 268`);
and 20000 random draws, radius up to 20 beside a rectangle within 50 of
the center or up to 2000 beside one within 2000, a draw with an empty
side skipped (`19802 random cases: 11637 overlap, checksum 905253295`).
`check_overlap.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, regions, columns and float arms check clean as
first written. The Rust solution takes 13 fixes by `karac fix`'s count:
`struct Solution;` to `struct Solution {}`, Rust's `i32::max` and
`i32::min` to `i32.max` and `i32.min`, and `Solution::` to `Solution.`.
A type-qualified call of a number's method, `i32.max(x1, ..)`, was then
refused as "no associated function 'max' on type 'i32'", though
design.md §9 makes `T.m(x, ..)` the call `x.m(..)`; that was
B-2026-11-26-3, fixed by 2099ac467c (B-2026-11-25-40), after which the
arm checks and its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: is there a point in the circle and the rectangle at once? The
corners and the center are whole numbers, so if any point is shared the
rectangle's point nearest the center is one, and it is a lattice point;
so every lattice point of the rectangle within the circle's bounding
square is tried. LeetCode's examples and ten edge cases (the center
inside, a corner touched exactly and missed by one, an edge touched and
missed, the largest circle with the whole plane and short of a corner,
the corners of the plane) and 1990 random cases of radius up to 50 with
the rectangle's corners within 100 of the center. The edge cases are a
`for` over an array of tuples, whose literals `karac fix` writes `1i32`
on the first tuple (B-2026-11-26-2).

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the whole picture turned half round about the origin gives the same answer |
| P3 | x and y swapped, a reflection in the diagonal, gives the same answer |
| P4 | a circle one wider still overlaps what this one did |
| P5 | the picture moved 7 right and 3 down gives the same answer |
| P6 | the ★ arm's answer |

All 55,210 checks pass on every arm (P4 applies to overlaps only, P5
within the plane): `2003 cases: checksum 812751162, 55210 checks over 5
arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac build`
and `karac __mir-llvm-run`. Python, with the ★ arm's clamp, gives the
same checksum, and 1033 of the 2003 cases overlap.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a circle only touching the rectangle taken as apart | P1 17, P6 68 |
| M2 | ★: the center clamped to the rectangle's left side only | P1 659, P2 493, P3 464, P6 2636 |
| M3 | regions: the band widened by the radius on the left only | P1 63, P2 122, P3 117, P6 63 |
| M4 | regions: the top right corner dropped, the bottom right one tried twice | P1 12, P2 35, P6 12 |
| M5 | columns: the circle's last column left out | P1 6, P2 9, P3 9, P6 6 |
| M6 | columns: a column whose span only touches the rectangle's top taken as missing it | P1 5, P2 10, P3 8, P6 5 |
| M7 | float: a gap to the right measured from the rectangle's left side | P1 234, P2 393, P6 234 |
| M8 | float: a gap of exactly the radius taken as apart | P1 17, P6 17 |
| M9 | solution: the nearest y clamped to the bottom side only | P1 657, P2 500, P3 464, P6 657 |
| M10 | solution: the squared radius taken as r(r + 1) | P1 3, P6 3 |

## Benchmarks

The bench draws 10^5 circles and rectangles near the origin and runs the
★ arm on all of them 1000 times, each round growing every radius by one,
the overlaps of each round counted into the checksum. Every
implementation prints `1000 rounds over 10^5 circles and rectangles:
checksum 721435955`.

BENCHTAB
