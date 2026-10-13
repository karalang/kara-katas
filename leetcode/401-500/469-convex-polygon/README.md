# 469. Convex Polygon

You are given an array of points on the X-Y plane `points` where
`points[i] = [xi, yi]`. The points form a polygon when joined
sequentially. Return `true` if this polygon is convex and `false`
otherwise. You may assume the polygon formed by the given points is
always a simple polygon: exactly two edges intersect at each vertex,
and edges otherwise don't intersect each other.

```
points = [[0,0],[0,5],[5,5],[5,0]]          ->  true
points = [[0,0],[0,10],[10,10],[10,0],[5,5]]  ->  false
```

**Constraints:** `3 <= points.length <= 10^4`; `-10^4 <= xi, yi <= 10^4`;
all the given points are unique.

## Approaches

Every arm is `fn is_convex(points: Vec[(i64, i64)]) -> bool`, and
borrows the points. Everything is in integers: a cross product of two
edges says which way the walk turns, and 0 means straight on.

| file | mechanism |
|---|---|
| `convex_polygon.kara` ★ | the cross product of each edge with the next; the polygon is convex when the turns that are not straight all go the same way. O(n) |
| `convex_polygon_halfplane.kara` | the plain reference: for every edge, all the vertices lie on one side of the line through it, or on it. O(n²) |
| `convex_polygon_hull.kara` | build the convex hull with Andrew's monotone chain, keeping the points along its edges (a chain gives up a point only on a strict right turn), and check that every vertex is on it. O(n log n) |
| `convex_polygon_directions.kara` | orient the polygon counterclockwise by the sign of its area and list the edge directions: going round a convex polygon they only turn left, so in angle order from the positive x axis they wrap past it once, and at most one edge comes before the edge ahead of it. Directions are compared by half-plane, then by cross product. O(n) |
| `differential.kara` | the four arms on 1,500 random polygons, five properties |

Every arm prints the same 12 lines: the two LeetCode examples, a
triangle both ways round, a square with points along its edges, an
arrow, a hexagon, an L shape, a thin wedge, a polygon with three
collinear vertices, one with its middle vertex bent in by one unit, and
for 300 random polygons (3 to 40 edges, half of them then with one
edge pushed in) how many are convex and a checksum of the answers in order.
`convex_polygon.py` mirrors the ★ arm and its output is byte-identical;
it divides with a helper because Kāra's integer division rounds toward
zero and Python's floors.

The random polygons are made in integers. A convex one is random edge
vectors and the one that closes them, laid end to end in angle order;
parallel vectors leave collinear vertices, and the coordinates are
doubled so every edge has a midpoint on the grid. A dent replaces one
edge with two, through a point part of the way from the edge's midpoint
toward the centre. That point is used only when it lies strictly inside
the polygon, which keeps the polygon simple; otherwise the midpoint
itself is, and the polygon stays convex.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random polygons, half of them small (3 to 8 edges before a
dent).

| | property |
|---|---|
| P1 | a polygon built convex is convex, and one with an edge pushed in to a point strictly inside is not |
| P2 | starting from another vertex keeps the answer |
| P3 | going round the other way keeps it |
| P4 | a quarter turn with a scale and a shift keeps it, and so does a mirror image |
| P5 | a new vertex at the middle of an edge keeps it |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a straight vertex counts as a right turn | P1 783, P3 343, P4 343, P5 947 |
| M2 | ★: the turn at the first vertex is not looked at | P2 77, P3 89 |
| M3 | half-plane: a vertex on the line counts as left of it | P3 850, P4 850 |
| M4 | half-plane: the side test mixes up the edge's two ends | P1 780, P3 98, P4 98, P5 5 |
| M5 | hull: the chains drop points along an edge | P1 343, P5 507 |
| M6 | hull: one vertex off the hull is let through | P1 650, P5 131 |
| M7 | directions: the step from the last edge back to the first is not counted | P1 650, P2 515, P3 597, P4 595 |
| M8 | directions: two wraps are let through | P1 650 |

The generated polygons go round counterclockwise, so the mutants that
only go wrong clockwise need P3's reversal or P4's mirror image: M3
fails exactly the 850 convex cases there, since every edge's own ends
lie on its line and count as left of it. M2 is blind to P1 because the
dent is never the first vertex; turning the start (P2) or the direction
(P3) moves it there. A dent makes exactly one reflex vertex and so
exactly two wraps, which is why M6, M7 and M8 all fail the same 650 P1
cases, the dents pushed strictly inside.

A first M4, which skipped the first edge's half-plane, survived, and it
is an equivalent mutant: at a reflex vertex of a simple polygon both
edges that meet there have vertices on both sides of their lines, so a
non-convex polygon always fails at least two edges and skipping one
never changes the answer. It was replaced.

## Verification

All four arms print the same output as `convex_polygon.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends the ★, half-plane and directions arms
match under `karac run --interp`; LLJIT and `karac build` stop in the
legacy code generator on the harness's index into an array literal
("Index operator applied to non-array type"). The hull arm and the
differential stop on every legacy backend at `on_hull.insert(*p)`,
where the legacy type checker gives a loop over a `Vec` its items by
value and v2 by reference. Legacy `karac build` rejects the bench
program (see Benchmarks). Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 polygons of 50,000
vertices once: points on the parabola `y = x * x` at increasing `x`
(steps of 1 to 3), closed along the top, which makes them convex; every
other one has a dent, one vertex lifted just above the chord of its two
neighbours. Each of 20 rounds checks every polygon, so the convex ones
are read in full and the dented ones up to the dent. Every
implementation prints `20 rounds on 100 polygons of 50000 vertices:
1000 convex, checksum 53976483`, the Kāra program under
`karac __mir-run` included (in 67 s).

The legacy `karac build` rejects the bench program (it moves
`polygons[k]` out of the index, where v2 borrows it), so `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend. That edit is by hand, on top of the `scripts/new-bench.sh`
output.

Every mirror keeps the points as pairs in one array per polygon and
takes `% n` for the next two vertices, as the ★ arm does. Spot timings
on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.21 to 0.30 s |
| Rust (`rustc -O`) | 0.34 to 0.37 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.37 to 0.43 s |
| Go | 0.56 to 0.59 s |
| Python | 12.9 to 13.9 s |
| Kāra (`karac build --mir`) | 0.27 to 0.32 s |

The `--mir` row is timed at kara `aa6226e1fd`. Under
`karac __mir-llvm-run` the program prints the same line in 1.6 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

No new findings.
