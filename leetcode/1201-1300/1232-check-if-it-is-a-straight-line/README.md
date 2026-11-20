# 1232. Check If It Is a Straight Line

You are given an array `coordinates`, `coordinates[i] = [x, y]`, where
`[x, y]` represents the coordinate of a point. Check if these points make
a straight line in the XY plane.

```
coordinates = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]]  ->  true
coordinates = [[1,1],[2,2],[3,4],[4,5],[5,6],[7,7]]  ->  false
```

**Constraints:** `2 <= coordinates.length <= 1000`;
`coordinates[i].length == 2`; `-10^4 <= coordinates[i][0],
coordinates[i][1] <= 10^4`; `coordinates` contains no duplicate point.

The arms are `fn check_straight_line(coordinates: Vec[Vec[i64]]) ->
bool`. The two Rust arms keep the method LeetCode gives Rust users, on
`i32`, inside `impl Solution`, and a short `check_straight_line` converts
to it.

## Approaches

| file | mechanism |
|---|---|
| `check_if_it_is_a_straight_line.kara` ★ | the first two points fix a direction, and every point's offset from the first must be parallel to it: a cross product of zero, integers only, no division. O(n) |
| `check_if_it_is_a_straight_line_slopes.kara` | each offset from the first point reduced to a direction (divided by the gcd of its parts, turned to point right, or up when upright), the directions kept in a `Set[(i64, i64)]`: one line when the set holds one |
| `check_if_it_is_a_straight_line_triples.kara` | every three points in a row, by `windows(3)`, span no area; overlapping flat triples chain into one line since no two points are the same |
| `check_if_it_is_a_straight_line_fitted.kara` | the line through the first two points as `a x + b y = c`, and an `all` over the points |
| `check_if_it_is_a_straight_line_windows.kara` | a Rust solution as LeetCode's Rust users write it (the first point and the direction by tuple `let`s, `iter().skip(2).all(..)`), carried to Kāra by `karac fix` |
| `check_if_it_is_a_straight_line_loop.kara` | another Rust solution (an early `return true` for two points, the coordinates widened `as i64`, an index loop `for i in 2..n`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 7 lines: LeetCode's two examples, two points
(`true`), an upright line (`true`) and a level one with a point below it
(`false`), how many of 1000 random sets of 2 to 40 points are straight
and a checksum of the answers (`514`, `341130826`; half the sets have
one point moved off their line, and 14 of those are two points, still a
line), and 1000 points spread across `10^4`, on a line and with one
moved (`true, false`). `check_if_it_is_a_straight_line.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac run` and `karac build`, and under the AddressSanitizer
build.

The Mend loop: the ★ and fitted arms check clean as written. The slopes
arm was first written `let first = coordinates[0]`, a move out of an
index, which the fix borrows (`ref coordinates[0]`), and the triples arm
`coordinates.windows(3).all(..)`, which the fix makes
`windows(3).into_iter().all(..)`. The windows and loop arms take one
round of 4 fixes each (`struct Solution;` to `struct Solution {}` and
`Vec<Vec<i32>>` to `Vec[Vec[i32]]`), and check clean.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: no three of the points span a triangle of any area, every
triple tested, for up to 12 points. 2000 cases, a third with 2 to 12
points, a third with 13 to 100 and a third with 101 to 1000. Of every
four, two are on a line (a start, a direction of parts up to 10 and the
steps shuffled), one has a point moved off its line, and one is 2 to 6
points from a 6 by 6 grid, on a line only by chance.

| | property |
|---|---|
| P1 | the statement read literally (up to 12 points) |
| P2 | the points in another order give the same answer |
| P3 | the points moved together give the same answer |
| P4 | the points mirrored across the diagonal give the same answer |
| P5 | a straight line less its last point stays straight |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 cases: 1131 straight,
checksum 774523082, 72000 checks over 6 arms: 0 failures`, under `karac
__mir-run`, `karac run`, `karac build` and the AddressSanitizer build.
Python's answers for the same cases, every triple tested, give the same
count and checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the direction's parts swapped | P1 415, P6 5170 |
| S2 | ★: a point off the line on one side only | P1 186, P2 394, P4 710, P6 1705 |
| L1 | slopes: the direction never turned | P1 207, P2 157, P6 851 |
| L2 | slopes: the direction never reduced | P1 293, P2 19, P6 959 |
| T1 | triples: the third offset from the middle point | P1 281, P2 7, P4 14, P6 878 |
| T2 | triples: one flat triple enough | P1 329, P2 31, P5 61, P6 663 |
| F1 | fitted: the line's x coefficient turned | P1 403, P6 1000 |
| F2 | fitted: the constant from both points | P1 403, P6 1000 |
| W1 | windows: the third point skipped | P1 130, P2 60, P6 133 |
| W2 | windows: dx for dy | P1 344, P2 111, P4 250, P6 962 |
| O1 | loop: three points always a line | P1 107, P6 107 |
| O2 | loop: the last point never tested | P1 129, P2 49, P6 131 |

All twelve are caught, and P1, the statement read literally, catches
every one. A mutation of the ★ arm fails P6 on the five other arms. F1
and F2 fail the same 1000 cases: each makes the second point disagree
with the line through the first two unless that line is level or
upright, so every slanted set reads as bent. O1, three points always a
line, fails only the sets of three that are not, so only P1 and P6 see
it. The mutations that skip a point (W1 the third, O2 the last) and those
that test one side or one triple (S2, T2) answer by where the points sit
in the list, and P2, the points in another order, catches each of them;
P5, a straight line less its last point, catches T2 alone, whose one
flat triple may be the one the last point made. P4, the points mirrored,
catches S2, T1 and W2, which treat x and y unevenly. P3, the points
moved together, catches none: every arm tests offsets between points,
which a move leaves as they were.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, a cross product against the first two points, over 1000 random sets
of 1000 points on a line, every other set with its last point moved off
it, drawn once and each tested 200 times. Every program prints `1000
sets of 1000 points, 200 passes: 100000 straight`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.170 to 0.210 s | 0.197 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.476 to 0.558 s | 0.489 s |
| Rust (`rustc -O`) | 0.463 to 0.539 s | 0.497 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.483 to 0.561 s | 0.508 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.484 to 0.559 s | 0.500 s |
| C (`clang -O3`) | 0.173 to 0.359 s | 0.192 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.180 to 0.233 s | 0.184 s |
| Go | 0.363 to 0.484 s | 0.386 s |
| Python | 23.65 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` gives a different binary
here, with a loop its cost gate accepts compiled to run in parallel; its
median is 0.197 s, with 0.479 s of user time spread over the cores. Rust
with overflow checks on runs level with Kāra (0.508 s against 0.489 s),
and the two ranges overlap. Kāra takes about 2.5x C's time (0.489 s
against 0.192 s); Go is about 21% ahead of Kāra (0.386 s against 0.489
s). Python takes about 48x Kāra's time. No profile was taken.
