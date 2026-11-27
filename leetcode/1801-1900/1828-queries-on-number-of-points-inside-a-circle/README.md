# 1828. Queries on Number of Points Inside a Circle

You are given an array `points` where `points[i] = [xi, yi]` is the
coordinates of the `i`th point on a 2D plane. Multiple points can have
the same coordinates. You are also given an array `queries` where
`queries[j] = [xj, yj, rj]` describes a circle centered at `(xj, yj)`
with a radius of `rj`. For each query `queries[j]`, compute the number
of points inside the `j`th circle. Points on the border of the circle
are considered inside. Return an array `answer`, where `answer[j]` is
the answer to the `j`th query.

```
points = [[1,3],[3,3],[5,3],[2,2]], queries = [[2,3,1],[4,3,1],[1,1,2]]                ->  [3,2,2]
points = [[1,1],[2,2],[3,3],[4,4],[5,5]], queries = [[1,2,2],[2,2,2],[4,3,2],[4,3,3]]  ->  [2,3,2,4]
```

**Constraints:** `1 <= points.length <= 500`, `0 <= xi, yi <= 500`, `1
<= queries.length <= 500`, `0 <= xj, yj <= 500`, `1 <= rj <= 500`, all
coordinates integers.

The arms are `fn count_points(points: Vec[Vec[i64]], queries:
Vec[Vec[i64]]) -> Vec[i64]`.

## Approaches

| file | mechanism |
|---|---|
| `count_points.kara` ★ | each query against each point, the point counted when its squared distance from the centre is at most the squared radius, so no root is taken and a point on the circle counts. O(n q) |
| `count_points_sorted.kara` | the points sorted by x once, so each query looks only at the band of points from `x - r` to `x + r`, found by `partition_point`, and tests the distance there. O(n log n + q (log n + b)), b the points in a band |
| `count_points_columns.kara` | the points counted into the 501 by 501 grid of their coordinates, each column summed from the bottom, so a query walks the columns from `x - r` to `x + r` and reads, in each, the points within the circle's height there, the largest `dy` with `dx * dx + dy * dy` at most `r * r`, found from an `f64` square root and corrected. O(V^2 + q r), V = 501 |
| `count_points_distinct.kara` | points given more than once merged first, into a `Map` from each place to how many points stand there, so each query tests each place once and adds its count, as one chain of `iter`, `filter`, `map` and `sum`. O(n + q d), d the distinct places |
| `count_points_solution.kara` | a Rust solution as LeetCode's Rust users write it (the ★ arm's test as `filter` and `count` over the points, with `pow(2)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples; five edges
on one set of points, a circle with points on its border, 3-4-5 from the
centre, and one just past it, a point at the centre, one place given
three times, a circle reaching past the grid's corner, and a circle
holding no point (`[4, 1, 3, 5, 0]`); the constraints' most, 500 points
and 500 queries of radius 500 all over the grid, and of radius 1, each
answer summed (`the most: 243134 4`); and 3000 random cases of 1 to 8
points and 1 to 5 queries, coordinates from 0 to 10 and radii from 1 to
6 (`3000 random cases: checksum 913892356`). `count_points.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: every arm and the harness check clean as first written.
The Rust solution takes 16 fixes by `karac fix`'s count, and its diff
is: `struct Solution {}` added above the `impl`; `Vec<Vec<i32>>` and
`Vec<i32>` to `Vec[Vec[i32]]` and `Vec[i32]`; `Solution::` to
`Solution.` at the harness's 6 calls; and the harness's `as i64` on each
count folded into the checksum taken off, an `i32` widening without a
cast. `(p[0] - x).pow(2)`, `.count() as i32` and the closures over `q`
and `p` are Kāra as they stand. The solution takes `Vec[Vec[i32]]`s, so
its harness builds its points and queries as `i32`s. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each query walks every whole place of the square around its
circle, keeps the places inside or on the circle, and counts the points
standing at each. It runs 2000 random cases of 1 to 8 points and 1 to 5
queries, coordinates from 0 to 10 and radii from 1 to 6. Each arm meets
six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | one count to a query, each from none to every point |
| P3 | the points and the circles moved together give the same counts |
| P4 | a circle made wider never holds fewer points |
| P5 | everything mirrored in the line `x = y` gives the same counts |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 507898321, 60000 checks over 5 arms: 0 failures`,
under `karac run`, `karac build` and `karac __mir-llvm-run`, and under
`karac __mir-run` with its step budget raised. The columns arm fills a
501 by 502 table for every case, about 10^9 cell updates over the 2000
cases, which runs past the interpreter's default budget of 4 * 10^10
steps: under the default `karac __mir-run` stops with `step limit
exceeded`, and with `KARAC_MIR_MAX_STEPS=1000000000000` it prints the
same line in 12 minutes. Python, over the same cases, gives the same
checksum.

## Mutation testing

Ten edits to the differential, each run under `karac __mir-llvm-run`
only, as the interpreter takes 12 minutes a run here, two to each arm.
Each is killed, and not by a crash. The columns arm's first edit was
first to stop the square root's upward correction one short on a square;
an `f64` square root of a square up to 250000 is exact, so the
correction never runs, and the edit survived as an equivalent. It now
leaves out the circle's last column.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a point on the circle left out | P1 566, P6 2264 |
| M2 | ★: each point's height measured from the centre's x | P1 1456, P3 1311, P5 1561, P6 5824 |
| M3 | sorted: the band started at the centre | P1 1210, P5 1250, P6 1210 |
| M4 | sorted: the band's last column left out | P1 138, P5 276, P6 138 |
| M5 | columns: the circle's last column left out | P1 138, P5 276, P6 138 |
| M6 | columns: each column's top place left out | P1 732, P5 733, P6 732 |
| M7 | distinct: every place counted once, however many stand there | P1 83, P6 83 |
| M8 | distinct: the height's square taken with the width | P1 1436, P3 1145, P5 1513, P6 1436 |
| M9 | solution: the radius's square taken one radius short | P1 797, P6 797 |
| M10 | solution: the width taken unsquared | P1 1672, P5 1764, P6 1672 |

## Benchmarks

The bench builds one list of 1000 points and one of 1000 queries of
radius 1 to 500 once and makes 200 calls of the ★ arm on runs of 250 to
499 points and 250 to 499 queries, each run's start and lengths drawn
from the checksum so far. Each call copies its runs, as the arm takes
its lists by value. It checks clean as first written. Every
implementation prints `200 calls: checksum 103242281`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.14 s against Rust's 0.04 s (0.14 s with overflow checks
on), C's 0.03 s and Go's 0.06 s; Python takes 4.4 s.
