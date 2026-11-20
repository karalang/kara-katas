# 1266. Minimum Time Visiting All Points

On a 2D plane there are `n` points with integer coordinates `points[i] =
[xi, yi]`. Return the minimum time in seconds to visit all the points in
the order given by `points`.

You can move according to these rules:

- In 1 second, you can either move vertically by one unit, move
  horizontally by one unit, or move diagonally `sqrt(2)` units (in other
  words, move one unit vertically then one unit horizontally in 1
  second).
- You have to visit the points in the same order as they appear in the
  array.
- You are allowed to pass through points that appear later in the order,
  but these do not count as visits.

```
points = [[1,1],[3,4],[-1,0]]  ->  7
points = [[3,2],[-2,2]]        ->  5
```

**Constraints:** `points.length == n`; `1 <= n <= 100`; `points[i].length
== 2`; `-1000 <= points[i][0], points[i][1] <= 1000`.

The arms are `fn min_time_to_visit_all_points(points: Vec[Vec[i64]]) ->
i64`.

## Approaches

| file | mechanism |
|---|---|
| `min_time_to_visit_all_points.kara` ★ | by neighbours: a diagonal step closes a unit of both gaps at once, so each pair of neighbours, read by `windows(2)`, costs the larger of its two gaps. O(n) |
| `min_time_to_visit_all_points_loop.kara` | by index: for each pair, the diagonal steps (the smaller gap) plus the straight ones (what is left of the larger) |
| `min_time_to_visit_all_points_zip.kara` | by pairs: the points zipped with themselves skipped by one, the larger gaps summed by a `fold` |
| `min_time_to_visit_all_points_walk.kara` | by walking: a cursor moves a second at a time, each coordinate a unit toward the next point by `signum` while it differs. O(total time) |
| `min_time_to_visit_all_points_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Vec<Vec<i32>>`, `windows(2)`, `std::cmp::max`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples (`7 5`); 2000
random walks of 1 to 100 points, half within 5 of the origin and half
across the whole box (`2000 random walks: 46039063 seconds, checksum
445779102`); and the constraints' top, 100 points from corner to corner
and 100 on a line (`198000 1980`). `min_time_to_visit_all_points.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the loop, zip and walk arms checked clean as first
written. The ★ arm took one fix: `windows(2)` returns a
`Vec[Slice[Vec[i64]]]`, not an iterator, and `karac fix` inserted the
`.into_iter()` before `.map`. The solution arm takes one round of fixes,
12 by `karac fix`'s count: `Vec<..>` to brackets, the same
`.into_iter()`, `std::cmp::max` to `max`, `struct Solution;` to `struct
Solution {}`, `::` to `.`, the closure's `|&c|` to `|c|`, and the
wrapper's `as i64`, a lossless widening Kāra does by itself, removed. No
gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a breadth-first search over the grid from each point to the
next, a second per move to any of the 8 cells around. 2000 random walks
of 1 to 12 points within 6 of the origin.

| | property |
|---|---|
| P1 | the statement read literally: the breadth-first search's time |
| P2 | the points visited in reverse take the same time |
| P3 | the points all shifted by the same random offset take the same time |
| P4 | each point's coordinates swapped take the same time |
| P5 | a point inserted anywhere never makes the walk shorter |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 walks: checksum 870554799,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the smaller gap, not the larger | P1 1814, P5 211, P6 7256 |
| S2 | ★: `windows(3)` | P1 1825, P2 1526, P6 7300 |
| L1 | loop: the first pair skipped | P1 1822, P2 1526, P6 1822 |
| L2 | loop: the diagonal steps not counted | P1 1808, P5 129, P6 1808 |
| Z1 | zip: zipped with the points skipped by two | P1 1753, P5 125, P6 1753 |
| Z2 | zip: the `y` gap read against `b`'s `x` | P1 1620, P2 1618, P3 1831, P4 1743, P6 1620 |
| W1 | walk: `y` moves only once `x` has arrived | P1 1731, P5 89, P6 1731 |
| W2 | walk: the second point skipped | P1 1623, P2 1416, P5 23, P6 1623 |
| O1 | solution: the two gaps added, not maxed | P1 1808, P6 1808 |
| O2 | solution: the `x` gap without `abs` | P1 1403, P2 1538, P4 1628, P6 1403 |

All ten are caught, every one by P1, the breadth-first search. The
symmetry properties P2 to P4 see only the edits that break a symmetry:
P2 a skipped pair or a window of the wrong size, P3 only Z2, the one
edit that mixes a coordinate with the other point's, and P4 the two whose
answer changes when `x` and `y` trade places (W1 walks the two
coordinates differently, but its total, the sum of the gaps, does not
change). P5, the triangle inequality, sees the
edits that undercount, and not O1, which overcounts: adding the gaps is
the Manhattan distance, also a metric.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the larger of the two gaps between neighbouring points, summed over
`windows(2)`) on 1000 random walks of 100 points from -1000 to 1000
built once, 3000 rounds; every answer folded into a checksum. Every
program prints `3000 rounds of 1000 walks of 100 points: checksum
352414226`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.792 to 1.996 s | 1.889 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.748 to 1.957 s | 1.845 s |
| Rust (`rustc -O`) | 0.732 to 0.866 s | 0.777 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.180 to 3.500 s | 3.266 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 3.141 to 3.457 s | 3.251 s |
| C (`clang -O3`) | 0.514 to 0.601 s | 0.532 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.529 to 0.586 s | 0.548 s |
| Go | 0.702 to 0.775 s | 0.726 s |
| Python | 53.65 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on takes about 1.8x Kāra's time. Kāra
takes about 3.5x C's time (1.845 s against 0.532 s); Kāra takes about
2.5x Go's time (1.845 s against 0.726 s). Python takes about 29x Kāra's
time. No profile was taken.
