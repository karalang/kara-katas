# 812. Largest Triangle Area

Given distinct points on the X-Y plane, return the area of the largest
triangle whose three corners are among them. Answers within 10^-5 of the
true area are accepted.

```
points = [[0, 0], [0, 1], [1, 0], [0, 2], [2, 0]]  ->  2.0
points = [[1, 0], [0, 0], [0, 1]]                  ->  0.5
```

**Constraints:** `3 <= points.length <= 50`, `-50 <= xi, yi <= 50`, and
all the points are unique.

## Approaches

Twice a triangle's area is the absolute cross product of two of its
sides, an integer for integer points. Every arm searches on that integer
and halves only the answer, so every answer is exact: a whole number or
a half.

| file | mechanism |
|---|---|
| `largest_triangle_area.kara` ★ | every triple of points. O(n^3) |
| `largest_triangle_area_hull.kara` | the convex hull by Andrew's monotone chain, then every triple of its corners. O(n log n + h^3) for h the corners |
| `largest_triangle_area_calipers.kara` | the hull, then rotating calipers: fix a corner i, walk a second corner j round the hull, and let the third corner k only advance, as the best k never moves back when j moves on. O(n log n + h^2) |
| `largest_triangle_area_iter.kara` | for each first corner, the `max` over second corners of the `max` over third corners, each a `map` over a range |
| `differential.kara` | the four arms against the shoelace area of every triangle, four properties |

The largest triangle has its corners on the hull: moving a corner that
is inside the hull away from the opposite side, as far as the hull
reaches, never makes the triangle smaller. The hull arms drop the points
that lie on an edge of the hull, so that every hull point is a corner.

Every arm prints the same 9 lines: LeetCode's two examples; three points
on a line; the four corners of the 100 by 100 square, whose best
triangle is half of it; five points with one inside the hull and one on
its edge; a kite stretched corner to corner across the board; LeetCode's
largest, 50 random points on the whole board; 50 points on one line; and
300 random rounds of 3 to 22 points, with a total area and a checksum.
`largest_triangle_area.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
itself: the area of every triangle by the shoelace formula, `|x1 (y2 -
y3) + x2 (y3 - y1) + x3 (y1 - y2)| / 2`, the largest of them. Its 1,600
cases have 3 to 12 distinct points and come in four kinds of 400: points
anywhere in a 9 by 9 square; points on the edge of a square, so that the
hull has points along its edges; points on one line with one or two off
it or none (134 of these cases have every point on the line); and points
near a circle, so that most points are hull corners.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the same answer for the points reversed, rotated by one and shifted by (3, -2) |
| P3 | the same answer for the points turned a quarter round, (x, y) to (-y, x) |
| P4 | four times the answer for the points with their coordinates doubled |

It prints `1600 cases (134 with every point on one line), 25600 checks
over 4 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no second corner next to the first | P1 619, P2 669, P3 669, P4 669 |
| M2 | ★: the signed area, not its size | P1 690, P2 646, P3 646, P4 646 |
| M3 | ★: a cross product with a wrong side | P1 1537, P2 1533, P3 1537, P4 1533 |
| M4 | hull: a corner that turns left by a cross product of 1 dropped | P1 77, P2 77, P3 68 |
| M5 | hull: the upper chain left out | P1 1466, P2 1466, P3 1466, P4 1466 |
| M6 | hull: the points not sorted | P1 176, P2 165, P3 165, P4 165 |
| M7 | calipers: a cross product with a wrong side | P1 1334, P2 1334, P3 1453, P4 1334 |
| M8 | calipers: the last corner never a third corner | P1 331, P2 331, P3 336, P4 331 |
| M9 | calipers: the second corner stops one short | P1 491, P2 491, P3 494, P4 491 |
| M10 | iter: no third corner next to the second | P1 614, P2 593, P3 593, P4 593 |
| M11 | iter: an empty range of third corners worth 1 | P1 134, P2 134, P3 134, P4 134 |
| M12 | iter: the first point never a first corner | P1 585, P2 585, P3 585, P4 585 |

P1 kills all twelve. M4 is the one P4 cannot see: doubling the points
multiplies every cross product by 4, so none is 1 any more. M11 is seen
only on the 134 cases with every point on a line, the only ones whose
answer is 0.

Six more edits leave every answer right and are not counted. In the hull
arm, keeping the points on the hull's edges, or never popping the second
point of a chain, gives the triple search more points, never fewer
corners; building the chains to turn right builds the same hull
clockwise. In the calipers arm, keeping the edge points, stopping the
third corner at a tie, or starting it over for each second corner each
still finds the best k: the area along a straight edge changes in one
direction, and starting over only costs time.

## Verification

Every arm prints the same output as `largest_triangle_area.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`d0ad6409f5`, whose last compiler change is `c120cafada`; the release
build that runs `check` and `__mir-run` is at `f6f2efb14`, one parser
change behind it. The runtime archives were built after the last runtime
change, `45d6c491fc`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build run all four arms but
print a float with no fractional part without its `.0`: `2`, `0`, `5000`
where the mirror and every v2 lane print `2.0`, `0.0` and `5000.0`
(docs/library/core-types.md § Printing), so no arm's output matches. The
legacy build of the differential prints its 0-failure line, with a
warning that `points` is used after a move, legacy taking a bare
parameter as owned. Legacy refuses the bench program: it types the item
of `points.iter()` as a copied tuple and so refuses `*q`, and reads
`largest_triangle_area(sets[k])` as moving a `Vec` out of an index
(`E_INDEX_MOVE_NON_COPY`). Legacy is frozen, so all of this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 sets of 50
distinct points with coordinates from -50 to 50 are made once. Each of
60,000 rounds moves one point of the next set to a new place not already
taken and finds that set's largest triangle, every one of its 19,600
triples. Every implementation prints `60000 rounds of 50 points: total
area 250119942.0, checksum 981780837`, the Kāra program under `karac
__mir-run` included, in 896 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine; the three runs outside the interleaving shared the
machine with other work):

| | time |
|---|---|
| C (`clang -O3`) | 1.56 to 1.76 s |
| Rust (`rustc -O`) | 1.27 to 1.56 s |
| Rust (`rustc -O -C overflow-checks=on`) | 6.50 to 7.00 s |
| Go | 2.19 to 2.38 s |
| Python | 231.86 to 241.11 s |
| Kāra (`karac build --mir`) | 3.00 to 3.33 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 13.3 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 3.30 s,
against C's 1.67, Rust's 1.34 and Go's 2.21, and Rust under overflow
checks takes 6.75. The gap to C and Rust is the overflow checks: each
triple's twice-area takes two products, five subtractions and an `abs`,
and Kāra checks every one, where `clang -O3` and `rustc -O` let them
wrap. Under valgrind's cachegrind v2 runs 43.3 billion instructions and
11.9 billion branches, C 21.1 billion and 1.26 billion, Rust 20.3
billion and 1.34 billion; the extra branches are the checks, and they
are almost never mispredicted (0.6% of v2's branches, against C's 5.4%).
On the equal-safety footing, Rust with overflow checks on, Kāra takes
half Rust's time. Built for `x86-64-v3`, the target `karac build` uses,
C (`clang -O3 -march=x86-64-v3`) takes 1.44 to 1.54 s in five more
interleaved runs, where v2 took 2.91 to 3.21 s, and runs 13.8 billion
instructions; Rust with overflow checks (`-C target-cpu=x86-64-v3`)
takes 6.11 to 6.48 s. Legacy refuses the bench program (see
Verification), so there is no legacy timing to set v2 against. The
comparison with C and Rust waits until after M4.

## Compiler findings

The iterator arm was first written as one chain over the triples,
`(0..n).flat_map(|i| (i + 1..n).flat_map(|j| (j + 1..n).map(|k|
twice_area(points[i], points[j], points[k])))).max()`. `karac check` and
the MIR borrow checker refuse it: the inner closures read `i` and `j`,
the closures live on inside the iterators that the outer closures
return, and the checker captures `i` and `j` by `ref`, so the result
"borrows `i`, which this function owns" (E0509). core-semantics.md §9.1
moves a captured place in when it dies while the closure is still live,
and copies a `Copy` one, and §9.3 makes a closure inside a returned
value escaping, which also captures by move; Kāra has no `move` to ask
for it. That is filed as B-2026-10-20-34. The arm now takes a `max` per
corner, whose inner closures do not outlive their call, and is right on
every v2 surface; it goes back to the chain over the triples once the
row is fixed. Looking for another spelling found B-2026-10-20-35: a
helper returning `impl Iterator[Item = i64]` cannot be passed to
`flat_map`, and `.collect()` on one passes `karac check` and is then
refused by the MIR builder.
