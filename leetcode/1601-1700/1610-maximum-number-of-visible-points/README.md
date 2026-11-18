# 1610. Maximum Number of Visible Points

You are given an array `points`, an integer `angle`, and your `location`,
where `location = [posx, posy]` and `points[i] = [xi, yi]` both denote
**integral coordinates** on the X-Y plane.

Initially, you are facing directly east from your position. You
**cannot move** from your position, but you can **rotate**. In other
words, `posx` and `posy` cannot be changed. Your field of view in
**degrees** is represented by `angle`, determining how wide you can see
from any given view direction. Let `d` be the amount in degrees that you
rotate counterclockwise. Then, your field of view is the **inclusive**
range of angles `[d - angle/2, d + angle/2]`.

You can **see** some set of points if, for each point, the **angle**
formed by the point, your position, and the immediate east direction
from your position is **in your field of view**.

There can be multiple points at one coordinate. There may be points at
your location, and you can always see these points regardless of your
rotation. Points do not obstruct your vision to other points.

Return *the maximum number of points you can see*.

```
points = [[2,1],[2,2],[3,3]],       angle = 90, location = [1,1]  ->  3
points = [[2,1],[2,2],[3,4],[1,1]], angle = 90, location = [1,1]  ->  4
points = [[1,0],[2,1]],             angle = 13, location = [1,1]  ->  1
```

**Constraints:** `1 <= points.length <= 10^5`; `points[i].length == 2`;
`location.length == 2`; `0 <= angle < 360`;
`0 <= posx, posy, xi, yi <= 100`.

## Approaches

Every arm takes each point's direction from the location in degrees,
`(dy as f64).atan2(dx as f64).to_degrees()`, sorts the directions, and
doubles the list with every direction 360 more, so that a view across
the 180 degree line is one run. A view as wide as `angle` that sees the
most can be turned until its first edge is on some point, so the answer
is the longest run spanning at most `angle`, plus the points at the
location.

Two directions a whole number of degrees apart can round to either side
of it: `(1, 2)` and `(-1, 3)` seen from the origin are 45 degrees apart,
and their directions differ by `45.00000000000001`, while the same two
360 further round differ by exactly `45.0`. An arm that slides its window
over the whole doubled list then counted both as seen while an arm that
starts each view in the first half did not, so every arm reaches `1e-9`
past `angle`, which takes such a pair as the exact answer does.

| file | mechanism |
|---|---|
| `visible.kara` ★ | the directions sorted with `sort_by(f64.total_cmp)` and doubled, then a window slid along the whole list, its back moved on while the span exceeds `angle`. O(n log n) |
| `visible_search.kara` | the directions by `filter` and `map` from an iterator chain, doubled with `extend`; for each first edge in the first half, `partition_point` finds the first direction past it. O(n log n) |
| `visible_scan.kara` | a `View` struct built by `View.new` (a `match` on `(dx, dy)` counting `(0, 0)` as at the location), then each first edge in the first half tried and the directions after it counted one by one. O(n^2) in the worst case |
| `visible_solution.kara` | LeetCode's Rust template (`Vec<Vec<i32>>` by value, `sort_by(\|a, b\| a.partial_cmp(b).unwrap())`, a sliding window, `ans.max(..)`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (a view of 0 degrees down a line of points, every point at the
location, and four points round the location with a view of 180), then
the points, the count visible and a checksum for 3000 problems of up to 6
points with coordinates from 0 to 4, 300 of up to 1000 points to 100, and
3 of up to 10000 points to 100. `visible.py` mirrors the ★ arm, writing
`to_degrees` out as `x * (180 / pi)` since `math.degrees` divides by
`pi / 180` and can round differently, and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the view's first edge on each point's direction in turn, and
every point counted whose direction is at most `angle` further round
counterclockwise, one behind the first edge taken 360 further round. It
checks 3000 problems of 1 to 8 points and a location with coordinates
from 0 to 4, and an angle that half the time is one of 0, 45, 90, 180 and
270, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every point and the location moved by (7, 3) leave the answer |
| P3 | the points reversed leave the answer |
| P4 | an angle one degree wider (at most 359) sees at least as many |
| P5 | one more point at the location is seen as one more |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 80751082, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property. Before the arms
reached `1e-9` past `angle` it printed 6 failures, one problem on which
the ★ and template arms saw 5 and the other two 4: the pair of directions
above.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M3 is the one P5 kills on every
problem: the point added at the location is never counted.

Two first tries at M7 were equivalent and were replaced: the scan arm's
directions taken as `atan2(dx, dy)`, which mirrors every direction and
so leaves every count, and its count started one place on, which counts
the first edge all the same.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each window counted one short | P1 2980, P6 2980 |
| M2 | ★: the list doubled with 180 more, not 360 | P1 1912, P6 1912 |
| M3 | ★: points at the location not counted | P1 480, P5 3000, P6 480 |
| M4 | search: the view a degree narrower and its far edge open | P1 474, P6 474 |
| M5 | search: only the first half of the first edges tried | P1 825, P6 825 |
| M6 | scan: the view half as wide | P1 1118, P6 1118 |
| M7 | scan: no view past the 180 degree line | P1 441, P6 441 |
| M8 | template: the directions not sorted | P1 820, P3 713, P6 820 |
| M9 | template: no answer above 3 | P1 1410, P6 1410 |
| M10 | ★: the directions sorted largest first | P1 1018, P6 1018 |

## Benchmarks

The bench makes 20 problems of 100000 points from 0 to 100, a location and an angle, all of it first. Then: directions by atan2 sorted and doubled, then a sliding window. Every implementation prints `20 problems of 100000 points from 0 to 100: 1437962 visible, checksum 485993477`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.175 s |
| Rust (`rustc -O`) | 0.178 s |
| Go | 0.208 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.209 s |
| Kāra (`karac build`) | 0.213 s |
| C (`clang -O3`) | 0.241 s |
| Python | 2.1 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (0.156 s and 0.208 s on one run).

## Verification

All four arms print the same output as `visible.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5bb1708545`.

## Writing it

The ★ arm wrote `let mut here = 0`, counted with `+= 1` and returned
beside an `i32`, and `karac fix` typed it `let mut here: i32 = 0`. The
search and scan arms were written in Kāra and checked as written. The
differential's literal reading did the same with two counts, and
`karac fix` typed both. Its harness first picked an angle as
`[0, 45, 90, 180, 270][k]` in one branch of an `if` whose other branch is
an `i32`, and that was refused: an array literal indexed where it is
written keeps `i64` elements whatever the index's result must be, even
under `let a: i32 = [0, 45][k]`, while the same literal bound first and
then indexed is fixed by the use (B-2026-11-18-12). The list is bound first.

The Rust template took one `karac fix` of 13 edits, among them `struct Solution;`
to `struct Solution {}`, the `<..>` types to `[..]`, `Vec::new()` to
`Vec.new()`, `for p in &points` to `for p in ref points`, `&&` to `and`,
`let mut same = 0` typed `i32`, and `Solution::` to `Solution.`. It then
checks and agrees with no hand edit.
