# 1637. Widest Vertical Area Between Two Points Containing No Points

Given `n` `points` on a 2D plane where `points[i] = [xi, yi]`, return
*the **widest vertical area** between two points such that no points are
inside the area.*

A **vertical area** is an area of fixed-width extending infinitely along
the y-axis (i.e., infinite height). The **widest vertical area** is the
one with the maximum width.

Note that points **on the edge** of a vertical area **are not**
considered included in the area.

```
points = [[8,7],[9,9],[7,4],[9,7]]                  ->  1
points = [[3,1],[9,0],[1,0],[1,4],[5,3],[8,8]]      ->  3
```

**Constraints:** `n == points.length`; `2 <= n <= 10^5`;
`points[i].length == 2`; `0 <= xi, yi <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `widest.kara` ★ | only the x values matter: collected, sorted, and the widest step taken over `windows(2)` with `map` and `max`. O(n log n) |
| `widest_set.kara` | the distinct x values in a `SortedSet`, walked in order with the previous one held in an `Option`. O(n log n) |
| `widest_buckets.kara` | linear time by pigeonhole: n values over a span s have some step of at least s / (n - 1), so with n - 1 buckets no wider than that, the widest step runs from one nonempty bucket's largest value to the next one's smallest. O(n) |
| `widest_solution.kara` | LeetCode's Rust template: the x values sorted with `sort_unstable` and folded over `windows(2)`. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples, two points on
one vertical line (0), two points `10^9` apart, and the widest gap at the
edge; then the widths summed and a checksum for 3000 random sets of up
to 6 points with coordinates up to 10, 300 of up to 1000 points up to
`10^9`, and 5 of up to 100000 points up to `10^9`. `widest.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for every pair of points with x values a < b, the area between
them holds no point when no point's x lies strictly between a and b, and
the answer is the widest such area. It checks 3000 random sets of 2 to 8
points, every other one with x from 0 to 5, so points share an x often,
the rest 0 to 1000. Every set is drawn before any arm answers.

| | property |
|---|---|
| P1 | the width is the statement read literally |
| P2 | the points in reverse order give the same width |
| P3 | every x mirrored to 1000 - x gives the same width |
| P4 | every x doubled doubles the width |
| P5 | the width is at most the span of the x values, and at least the span shared out over the n - 1 steps, rounded up |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 963574995, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Buckets one wider than the pigeonhole
bound (M8) are the subtlest: two values in one bucket can then be the
widest step, and 545 sets show it.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the x values left unsorted | P1 2177, P2 2602, P3 2602, P5 442, P6 2177 |
| M2 | ★: the narrowest step, not the widest | P1 2448, P5 2448, P6 2448 |
| M3 | ★: the y values, not the x | P1 2704, P4 2949, P5 2053, P6 2704 |
| M4 | set: the previous value never kept | P1 2959, P5 2959, P6 2959 |
| M5 | set: the last step, not the widest | P1 1370, P3 1806, P5 807, P6 1370 |
| M6 | buckets: a step measured from a bucket's smallest value | P1 765, P3 1172, P4 17, P6 765 |
| M7 | buckets: one bucket too few | panics on both backends: index out of bounds |
| M8 | buckets: each bucket one wider than the bound | P1 545, P3 55, P4 96, P5 545, P6 545 |
| M9 | template: every step one short | P1 2959, P4 2959, P5 938, P6 2959 |
| M10 | template: the last step never measured | P1 1174, P3 1142, P5 873, P6 1174 |

## Benchmarks

The bench draws 40 random sets of 100000 points, LeetCode's largest,
with x and y from 0 to `10^9`, all of them first as nested `Vec`s of two
(a `Vec<Vec<i32>>` in Rust, `[][]int32` in Go, lists in Python, and an
`int**` of two-int allocations in C, as LeetCode hands them over); then
each set's x values are copied out, sorted, and the widest step taken,
by the ★ arm in all five languages: Kāra's `sort`, Rust's `sort`, Go's
`slices.Sort`, Python's `sorted`, and C's `qsort`. Every implementation
prints `40 sets of 100000 points: widths sum to 5090199, checksum
753499183`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `widest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `SHA`.

## Writing it

The ★, set and buckets arms checked clean as first written: the ★ arm's
`xs.windows(2).into_iter().map(..).max().unwrap()` (`windows` returns a
`Vec` of slices, so it is consumed with `into_iter`), the set arm's
`if let Some(p) = previous`, and the buckets arm's `Vec[Option[i64]]`
updated through `map_or` and its `if let (Some(s), Some(l)) = (..)` over
a pair.

LeetCode's Rust template takes one `karac fix` of 11 edits: the types to
Kāra's brackets, `sort_unstable` to `sort`, `.into_iter()` after
`windows(2)`, and `Solution::` to `Solution.`. Its
`fold(0, |best, w| best.max(w[1] - w[0]))` kept its literal seed, which
the closure's `i32` result settles. The arm then checks and agrees with
no hand edit.
