# 1779. Find Nearest Point That Has the Same X or Y Coordinate

You are given two integers, `x` and `y`, which represent your current
location on a Cartesian grid: `(x, y)`. You are also given an array
`points` where each `points[i] = [a_i, b_i]` represents that a point
exists at `(a_i, b_i)`. A point is valid if it shares the same
x-coordinate or the same y-coordinate as your location. Return the index
(0-indexed) of the valid point with the smallest Manhattan distance from
your current location. If there are multiple, return the valid point
with the smallest index. If there are no valid points, return `-1`. The
Manhattan distance between two points `(x1, y1)` and `(x2, y2)` is
`abs(x1 - x2) + abs(y1 - y2)`.

```
x = 3, y = 4, points = [[1,2],[3,1],[2,4],[2,3],[4,4]]  ->  2
x = 3, y = 4, points = [[3,4]]                          ->  0
x = 3, y = 4, points = [[2,3]]                          ->  -1
```

**Constraints:** `1 <= points.length <= 10^4`, `points[i].length == 2`,
and `1 <= x, y, a_i, b_i <= 10^4`.

The arms are `fn nearest_valid_point(x: i32, y: i32, points:
Vec[Vec[i32]]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `nearest_valid_point.kara` ★ | one pass, keeping the nearest valid point so far, replaced only by one strictly nearer, so that a tie keeps the smallest index. O(n) |
| `nearest_valid_point_first.kara` | the valid points filtered with their indices, and `min_by_key`, which keeps the first of several equal keys, picks the nearest. O(n) |
| `nearest_valid_point_pairs.kara` | each valid point as a (distance, index) pair, and the least pair, whose index breaks a tie in distance. O(n) |
| `nearest_valid_point_sorted.kara` | the valid points' indices sorted by distance with `sort_by_key`, which is stable, so that the first is the smallest index among the nearest. O(n log n) |
| `nearest_valid_point_solution.kara` | a Rust solution as LeetCode's Rust users write it (`i32::MAX`, `for (i, p) in points.iter().enumerate()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`2 0 -1`);
five edges, the location itself listed last, two valid points equally
near, only a point on the same row, a nearer point that is not valid,
and no valid point among several (`2 0 1 1 -1`); the constraints' most,
10000 points at random, 10000 on the location's column at random rows,
and 10000 copies of one valid point (`the most: 4526 7173 0`); and 3000
random cases of 1 to 20 points on a grid of side 1 to 6 (`3000 random
cases: checksum 442388143`). `nearest_valid_point.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★ and first arms check clean as first written. The
pairs arm was first written with `Some((_, i)) => *i as i32` on the
least pair; check named `i` an `i64`, copied out of the borrowed pair,
and `karac fix` dropped the `*`, 1 fix. The sorted arm was first written
with `points[*i]` in its `filter` and `sort_by_key` closures, which are
lent each index as a bare `i64`, and `karac fix` dropped the four `*`s,
4 fixes. The Rust solution takes one round of 10 fixes, and its diff is:
`struct Solution;` to `struct Solution {}`, `Vec<Vec<i32>>` to
`Vec[Vec[i32]]` in both signatures, `i32::MAX` to `i32.MAX`, `||` to
`or`, and `Solution::` to `Solution.`. Its `for (i, p) in
points.iter().enumerate()` and `i as i32` stay. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every point checked for a shared x or y, the least Manhattan
distance among the valid ones found, and the first valid point at that
distance returned, or -1. LeetCode's examples, the edges, and 1992
random cases of 1 to 12 points on a grid of side 1 to 6. Each arm meets
six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | -1 exactly when no point shares x or y, else the index of one that does |
| P3 | x and y swapped, in the location and every point, give the same index |
| P4 | everything moved by 1000 on both axes gives the same index |
| P5 | the location itself added at the end is the answer, unless a point already sits there |
| P6 | the ★ arm's answer |

`karac fix` dropped four `as i64` casts the `lossless_cast` lint found
widening implicitly in the differential's own checks, where an `i32`
answer indexes the points. All 60,000 checks pass on every arm: `2000
cases: checksum 101595864, 60000 checks over 5 arms: 0 failures`, under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, reading the statement the same way, gives the
same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a tie in distance won by the later point | P1 864, P5 986, P6 3456 |
| M2 | ★: only points on the same column taken as valid | P1 428, P2 222, P3 818, P6 1712 |
| M3 | first: the farthest valid point taken | P1 1442, P5 1804, P6 1442 |
| M4 | first: a point's y compared with the location's x | P1 429, P2 283, P3 698, P6 429 |
| M5 | pairs: the greatest pair taken | P1 1442, P5 1804, P6 1442 |
| M6 | pairs: the distance counted along x alone | P1 530, P3 820, P5 872, P6 530 |
| M7 | sorted: the valid points left in index order | P1 592, P5 1215, P6 592 |
| M8 | sorted: the last after the sort taken | P1 1442, P5 1804, P6 1442 |
| M9 | solution: the least distance so far never kept | P1 1253, P5 599, P6 1253 |
| M10 | solution: the y difference added without its absolute value | P1 409, P3 686, P5 556, P6 409 |

## Benchmarks

The bench builds 20 lists of 10000 points once, each coordinate from 1
to 100, and makes 20000 calls of the ★ arm, each location drawn from the
checksum so far. Every implementation prints `20000 calls over 20 lists:
checksum 461086630`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.43 s against Rust's 0.47 s (0.48 s with
overflow checks on), C's 0.23 s and Go's 0.35 s; Python takes 12.6 s.
